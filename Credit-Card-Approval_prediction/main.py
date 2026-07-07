import os
import json
from datetime import datetime
from pathlib import Path
import joblib
from flask import Flask, request, jsonify, render_template

# Local imports
from app.preprocess import prepare_input_record

app = Flask(__name__, template_folder='frontend')

# Paths setup
REPO_ROOT = Path(__file__).resolve().parent
MODEL_PATH = REPO_ROOT / "models" / "random_forest.joblib"
PREDICTIONS_DIR = REPO_ROOT / "models" / "predictions"
SAMPLE_DOCS_DIR = REPO_ROOT / "frontend" / "sample-docs"
PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_PATH = PREDICTIONS_DIR / "prediction_summary.json"


def get_sample_docs_dir():
    """Resolve the markdown source used by the project docs portal."""
    docs_dir = SAMPLE_DOCS_DIR
    if docs_dir.exists():
        return docs_dir

    # Case-insensitive fallback for Windows friendliness.
    for path in REPO_ROOT.iterdir():
        if path.is_dir() and path.name.lower() == "sample-docs":
            return path

    return docs_dir

# Load the model artifact globally on startup
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Trained Random Forest model not found at {MODEL_PATH}. "
        "Please run notebook/train_models.ipynb first to train the models!"
    )

print(f"Loading Random Forest model from {MODEL_PATH}...")
artifact = joblib.load(MODEL_PATH)
model = artifact["model"]
feature_columns = artifact["feature_columns"]
default_threshold = artifact.get("threshold", 0.6)

def build_reason(probability, decision, record):
    """Generates a detailed, human-friendly explanation based on applicant features."""
    reasons = []
    
    # Extract values safely
    try:
        income = float(record.get("AMT_INCOME_TOTAL", 0.0))
        is_employed = record.get("EMPLAYMENT_STATUS", "Employed") == "Employed"
        years_emp = float(record.get("YEARS_EMPLOYED_INPUT", 0.0)) if is_employed else 0.0
        children = int(record.get("CNT_CHILDREN", 0))
        fam_members = int(record.get("CNT_FAM_MEMBERS", 1))
    except Exception:
        income = 0.0
        is_employed = False
        years_emp = 0.0
        children = 0
        fam_members = 1

    if decision == "Approved":
        if income >= 120000:
            reasons.append(f"Strong annual income (${income:,.2f}) satisfies standard banking capital buffers.")
        else:
            reasons.append(f"Income of ${income:,.2f} is accepted under current risk appetite.")
            
        if is_employed:
            if years_emp >= 2.0:
                reasons.append(f"Stable career tenure ({years_emp:.1f} years) exhibits solid professional stability.")
            else:
                reasons.append(f"Active employment status (tenure: {years_emp:.1f} years).")
        else:
            reasons.append("Unemployed/retired profile with alternative source criteria validation.")
            
        if children <= 2 and fam_members <= 4:
            reasons.append(f"Acceptable dependency index ({children} children, {fam_members} family members).")
            
        if not reasons:
            reasons.append("Profile satisfies all general lending guidelines.")
            
        return " | ".join(reasons)
    else:
        if income < 120000:
            reasons.append(f"Annual income (${income:,.2f}) is below the default $120,000 threshold.")
        if is_employed and years_emp < 2.0:
            reasons.append(f"Employment length ({years_emp:.1f} years) does not satisfy the 2.0-year stability criteria.")
        if not is_employed:
            reasons.append("Non-active employment status indicates high risk of credit default.")
        if children > 2 or fam_members > 4:
            reasons.append(f"High family dependency count ({children} children, {fam_members} members) elevates default risks.")
            
        if not reasons:
            reasons.append("Credit score failed to meet secondary algorithmic criteria.")
            
        return " | ".join(reasons)

@app.route('/')
def home():
    """Render the dashboard interface."""
    return render_template('index.html', active_page='dashboard')

@app.route('/predictor')
def predictor():
    """Render the predictor interface."""
    return render_template('predict.html', active_page='predictor')

@app.route('/docs')
def docs():
    """Render the documentation specs interface."""
    return render_template('docs.html', active_page='docs')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict approval status for a single applicant."""
    try:
        record = request.json
        if not record or 'ID' not in record:
            return jsonify({"error": "Invalid input, missing Applicant ID"}), 400

        # Preprocess the record using our module
        features_df = prepare_input_record(record, feature_columns)
        
        # Calculate probability and make decision
        probability = float(model.predict_proba(features_df)[0, 1])
        prediction = int(probability >= default_threshold)
        decision_label = "Approved" if prediction == 1 else "Denied"
        reason = build_reason(probability, decision_label, record)

        # Log details
        result = {
            "timestamp": datetime.now().isoformat(),
            "applicant_id": record["ID"],
            "prediction": decision_label,
            "probability": round(probability, 4),
            "reason": reason,
            "input_data": {
                "AMT_INCOME_TOTAL": record.get("AMT_INCOME_TOTAL", 0.0),
                "NAME_INCOME_TYPE": record.get("NAME_INCOME_TYPE", "Unknown"),
                "NAME_EDUCATION_TYPE": record.get("NAME_EDUCATION_TYPE", "Unknown")
            }
        }

        # Save single run result
        single_path = PREDICTIONS_DIR / f"prediction_{record['ID']}.json"
        with single_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        # Append to consolidated history
        history = []
        if SUMMARY_PATH.exists():
            try:
                with SUMMARY_PATH.open("r", encoding="utf-8") as f:
                    existing = json.load(f)
                    if isinstance(existing, dict) and "predictions" in existing:
                        history = existing.get("predictions", [])
                    elif isinstance(existing, list):
                        history = existing
            except Exception:
                # If file is empty or corrupted, start fresh
                pass

        history.append(result)
        summary_payload = {
            "total_predictions": len(history),
            "latest_prediction": result,
            "predictions": history
        }
        
        with SUMMARY_PATH.open("w", encoding="utf-8") as f:
            json.dump(summary_payload, f, indent=2)

        return jsonify(result)

    except Exception as e:
        import traceback
        import sys
        print("Prediction exception occurred:", str(e))
        traceback.print_exc()
        sys.stdout.flush()
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route('/history_data', methods=['GET'])
def history_data():
    """Fetch past decisions history from predictions file."""
    if not SUMMARY_PATH.exists():
        return jsonify({"predictions": []})
    
    try:
        with SUMMARY_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            # return lists in reverse chronological order so latest is on top
            if isinstance(data, dict) and "predictions" in data:
                predictions = data["predictions"]
                return jsonify({"predictions": list(reversed(predictions))})
            return jsonify({"predictions": []})
    except Exception as e:
         return jsonify({"error": f"Could not read history log: {str(e)}"}), 500

@app.route('/portal')
def portal():
    """Render the project docs portal page."""
    return render_template('project_docs.html', active_page='portal')

@app.route('/api/project-docs/list', methods=['GET'])
def list_project_docs():
    """Dynamically compile a flat list of markdown files in the sample docs directory."""
    docs_dir = get_sample_docs_dir()
    if not docs_dir.exists():
        return jsonify({"folders": []})
    
    files = []
    for file_path in sorted(docs_dir.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() == '.md' and not file_path.name.startswith('.'):
            files.append({
                "name": file_path.stem.replace('_', ' ').title(),
                "relative_path": file_path.name
            })

    return jsonify({
        "folders": [
            {
                "name": "Sample Docs",
                "files": files
            }
        ] if files else []
    })

@app.route('/api/project-docs/file', methods=['GET'])
def get_project_doc_file():
    """Read and return the raw content of a specific markdown file from sample docs."""
    rel_path = request.args.get('path', '')
    if not rel_path or '..' in rel_path or rel_path.startswith('/') or rel_path.startswith('\\'):
        return jsonify({"error": "Invalid file path requested"}), 400
        
    docs_dir = get_sample_docs_dir()
    target_file = (docs_dir / rel_path).resolve()
    
    # Security check: ensure path is within the designated sample docs folder
    if not str(target_file).startswith(str(docs_dir.resolve())):
        return jsonify({"error": "Access denied"}), 403
        
    if not target_file.exists() or not target_file.is_file():
        return jsonify({"error": "File not found"}), 404
        
    try:
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
