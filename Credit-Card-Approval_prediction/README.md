# Credit Card Approval Prediction

A production-ready machine learning system built with Python, Flask, pandas, and scikit-learn to automate credit card application screening and predict applicant eligibility based on demographic attributes and historical repayment behaviors.

**Live Application:** [https://credit-card-approval-prediction-envs.onrender.com/](https://credit-card-approval-prediction-envs.onrender.com/)

---

## Technical Accomplishments & Work Done

We have refactored the codebase to transform it from a command-line script/notebook into a premium, interactive web application:

1. **Jinja2 Multi-Page Architecture (MPA)**:
   - Split the original Single-Page Application (SPA) layout into a clean, multi-page Flask application utilizing template inheritance.
   - Created `base.html` for global layout styling, Outfit typography, and custom navigation branding.
   - Developed modular child views: `index.html` (Dashboard & Bento widgets), `predict.html` (Interactive predictor), and `docs.html` (Technical specs and Exploratory Data Analysis gallery).

2. **User-Friendly Form Interface**:
   - Replaced raw, negative integer days (e.g. `DAYS_BIRTH`, `DAYS_EMPLOYED`) with intuitive fields: **Age (in Years)**, **Employment Status** (select dropdown), and **Years of Employment**.
   - Added client-side JavaScript listeners that dynamically hide and disable employment duration inputs if the applicant is flagged as "Unemployed".
   - Implemented automated translation on the Flask backend (`app/preprocess.py`) to convert years back to the model-expected negative days and sentinel values.

3. **Inline Card Loader & Custom Risk Audit Reports**:
   - Replaced full-screen modal popups with a seamless, inline state machine inside the form container.
   - Upon submission, the viewport auto-scrolls to the top of the card, hides the input fields, and displays an inline spinner with real-time status steps ("Analyzing demographic factors...", "Querying Random Forest model...").
   - Once computed, the card displays an detailed risk audit report containing bulleted list explanations detailing why the application was approved or denied (e.g., income benchmarks, career tenure check, dependency ratios).

4. **Branding & Responsive Layouts**:
   - Optimized the Bento Grid widgets to remain structured as a responsive 2-column layout on mobile screens rather than falling back to a single column.
   - Ensured table records (like past Decision Logs) remain scrollable inside a touch-friendly overflow container on smaller viewports.
   - Shortened header options and cleaned navigation brand tags to display a unified logo text: **"Credit Approval"**.

---

## Detailed Project Structure

```dir
credit-card-approval-prediction/
│
├── main.py                          # Flask application entrypoint and api router
├── README.md                        # Project technical documentation
│
├── app/                             # Python backend package
│   ├── __init__.py                  # Package initializer
│   └── preprocess.py                # Preprocessing pipeline and feature encoder
│
├── frontend/                        # Jinja2 HTML layout and page templates
│   ├── base.html                    # Global template layout and shared CSS
│   ├── index.html                   # Dashboard homepage bento grid
│   ├── predict.html                 # Predictor form and decision log views
│   ├── docs.html                    # Data schema and visual EDA gallery
│   ├── image.png                    # Raw vertical background image source
│   └── image copy.png               # Raw vertical form image source
│
├── static/                          # Static web assets served by Flask
│   └── assets/                      # Curated images and exported visualization charts
│       ├── image_landscape.png      # Landscape-oriented rotated backdrop
│       ├── image_copy.png           # Form background backdrop
│       └── chart_1.png to chart_39.png   # Visual EDA charts exported from training
│
├── models/                          # Serialized machine learning models and logged data
│   ├── random_forest.joblib         # Active deployed Random Forest classifier
│   ├── decision_tree.joblib         # Decision Tree classifier model
│   ├── xgboost.joblib               # XGBoost classifier model
│   ├── logistic_regression.joblib   # Logistic Regression classifier model
│   └── predictions/                 # Prediction logs database directory
│       └── prediction_summary.json  # Consolidated history of all evaluations
│
├── notebook/                        # Jupyter research notebooks
│   └── train_models.ipynb           # Model training and data exploration notebook
│
├── project documentation/           # Directory reserved for technical specifications
│   └── .gitkeep                     # Git tracking file
│
└── tests/                           # Testing and local script backups
```

---

## Running the Application

### 1. Train the Models
To retrain the classifiers and export the `.joblib` pipelines:
```bash
python notebook/train_models.py
```

### 2. Run the Web Interface
To start the Flask server locally:
```bash
python main.py
```
Open your browser and navigate to `http://127.0.0.1:5000` to interact with the dashboard, run automated predictions using the **Autofill Random** feature, and view the visual chart galleries.

### 3. Containerized Run (Docker)
To build and run the application inside a lightweight container:
```bash
# Build the Docker image
docker build -t credit-approval-app .

# Run the container
docker run -p 5000:5000 credit-approval-app
```