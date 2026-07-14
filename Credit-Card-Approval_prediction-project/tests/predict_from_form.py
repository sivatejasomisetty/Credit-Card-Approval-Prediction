import json
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = REPO_ROOT / "models" / "simple_credit_approval_model.joblib"
OUTPUT_DIR = REPO_ROOT / "models" / "predictions"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_PATH = OUTPUT_DIR / "prediction_summary.json"


def build_single_record():
    print("Enter applicant details for credit approval prediction")
    print("Type your own values for each field when prompted.")
    print("-" * 45)

    record = {}
    record["ID"] = input("Applicant ID: ").strip()
    record["CODE_GENDER"] = input("Gender (M/F): ").strip().upper()
    record["FLAG_OWN_CAR"] = input("Own car? (Y/N): ").strip().upper()
    record["FLAG_OWN_REALTY"] = input("Own realty? (Y/N): ").strip().upper()
    record["CNT_CHILDREN"] = int(input("Number of children: ").strip())
    record["AMT_INCOME_TOTAL"] = float(input("Annual income: ").strip())
    record["NAME_INCOME_TYPE"] = input("Income type: ").strip()
    record["NAME_EDUCATION_TYPE"] = input("Education type: ").strip()
    record["NAME_FAMILY_STATUS"] = input("Family status: ").strip()
    record["NAME_HOUSING_TYPE"] = input("Housing type: ").strip()
    record["DAYS_BIRTH"] = int(input("Days birth (negative values): ").strip())
    record["DAYS_EMPLOYED"] = int(input("Days employed (negative values): ").strip())
    record["FLAG_MOBIL"] = int(input("Mobile phone flag (0/1): ").strip())
    record["FLAG_WORK_PHONE"] = int(input("Work phone flag (0/1): ").strip())
    record["FLAG_PHONE"] = int(input("Phone flag (0/1): ").strip())
    record["FLAG_EMAIL"] = int(input("Email flag (0/1): ").strip())
    record["OCCUPATION_TYPE"] = input("Occupation type: ").strip()
    record["CNT_FAM_MEMBERS"] = int(input("Family members count: ").strip())
    record["DAYS_REGISTRATION"] = int(input("Days registration: ").strip())
    record["DAYS_ID_PUBLISH"] = int(input("Days ID publish: ").strip())

    return record


def prepare_input_record(record):
    df = pd.DataFrame([record])
    df["EMPLOYED"] = df["DAYS_EMPLOYED"] != 365243
    df["YEARS_EMPLOYED"] = df["DAYS_EMPLOYED"].apply(lambda x: max(-x / 365, 0) if x != 365243 else 0)
    df["INCOME_EMPLOY_RATIO"] = df.apply(
        lambda row: row["AMT_INCOME_TOTAL"] / row["YEARS_EMPLOYED"]
        if row["YEARS_EMPLOYED"] > 0
        else row["AMT_INCOME_TOTAL"],
        axis=1,
    )

    df["STATUS_MAX"] = 0
    df["STATUS_MIN"] = 0
    df["STATUS_MEAN"] = 0
    df["STATUS_LAST"] = 0
    df["STATUS_TREND"] = 0
    df["NUM_LATE_MONTHS"] = 0

    categorical_columns = df.select_dtypes(include=["object", "bool"]).columns.tolist()
    df = pd.get_dummies(df, columns=categorical_columns, dummy_na=False)
    return df


def build_reason(probability, decision):
    if decision == "Approved" and probability >= 0.8:
        return "Strong financial profile and low-risk indicators."
    if decision == "Approved":
        return "Moderate confidence approval based on available signals."
    if probability >= 0.8:
        return "High-risk pattern detected; strong reasons for denial."
    return "Mixed profile with notable risk signals; review recommended."


def predict_single_record():
    artifact = joblib.load(MODEL_PATH)
    model = artifact["model"]
    feature_columns = artifact["feature_columns"]

    record = build_single_record()
    features = prepare_input_record(record)
    features = features.reindex(columns=feature_columns, fill_value=0)

    probability = float(model.predict_proba(features)[0, 1])
    threshold = artifact.get("threshold", 0.6)
    prediction = int(probability >= threshold)
    label = "Approved" if prediction == 1 else "Denied"
    reason = build_reason(probability, label)

    result = {
        "timestamp": datetime.now().isoformat(),
        "applicant_id": record["ID"],
        "prediction": label,
        "probability": round(probability, 4),
        "reason": reason,
        "input_data": record,
        "summary": f"Applicant {record['ID']} -> {label} (probability {round(probability, 4)}) | {reason}",
    }

    output_path = OUTPUT_DIR / f"prediction_{record['ID']}.json"
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    history = []
    if SUMMARY_PATH.exists():
        with SUMMARY_PATH.open("r", encoding="utf-8") as f:
            existing = json.load(f)
            if isinstance(existing, dict) and "predictions" in existing:
                history = existing.get("predictions", [])
            elif isinstance(existing, list):
                history = existing

    history.append(result)
    summary_payload = {
        "total_predictions": len(history),
        "latest_prediction": result,
        "predictions": history,
    }
    with SUMMARY_PATH.open("w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)

    print("\nPrediction Result")
    print("-" * 45)
    print(f"Applicant ID: {record['ID']}")
    print(f"Decision: {label}")
    print(f"Approval probability: {probability:.4f}")
    print(f"Reason: {reason}")
    print(f"Saved to: {output_path}")
    print(f"Summary saved to: {SUMMARY_PATH}")


if __name__ == "__main__":
    predict_single_record()
