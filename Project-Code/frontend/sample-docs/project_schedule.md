# Project Schedule & Timeline

This document outlines the chronological schedule, project phases, task assignments, and verification dates.

---

## 1. Project Development Phases

### Phase 1: Research & Feasibility (Weeks 1 - 2)
- **Objective:** Evaluate the dataset, perform exploratory data analysis (EDA), and identify preprocessing requirements.
- **Key Tasks:**
  - Import the demographic and credit status datasets into a Jupyter notebook.
  - Profile features to identify missing values and outliers.
  - Determine label definitions: Applicants are flagged as high risk (0) or low risk (1) based on payment history trends and late months.
- **Deliverable:** Initial exploratory notebook showing data distribution plots.

### Phase 2: Pipeline Design & Prototyping (Weeks 3 - 4)
- **Objective:** Design the data pipeline to handle data preparation and feature alignment.
- **Key Tasks:**
  - Build preprocessing functions to clean occupation variables and convert years to days.
  - Standardize categorical features through one-hot encoding.
  - Implement dynamic input fields on the frontend to disable employment tenure if the applicant is unemployed.
- **Deliverable:** Feature engineering module (`app/preprocess.py`) and prototype input forms.

### Phase 3: Model Training & Selection (Weeks 5 - 6)
- **Objective:** Train, evaluate, and tune multiple machine learning models to identify the best production candidate.
- **Key Tasks:**
  - Train Logistic Regression, Decision Tree, XGBoost, and Random Forest models.
  - Evaluate model performance using Accuracy, Precision, Recall, F1-Score, and ROC-AUC metrics.
  - Implement class weight balancing to address class imbalance.
- **Deliverable:** Serialized model pipelines saved as `.joblib` objects in `models/`.

### Phase 4: Full-Stack Integration (Weeks 7 - 8)
- **Objective:** Integrate the frontend layout and backend routes into a cohesive application.
- **Key Tasks:**
  - Develop Flask routing pathways in `main.py`.
  - Design the responsive Bento Grid homepage dashboard (`frontend/index.html`) to display aggregated prediction statistics and logs.
  - Create the prediction form and inline loader status indicators (`frontend/predict.html`).
- **Deliverable:** Fully functional local web application.

### Phase 5: Verification & Deployment (Weeks 9 - 10)
- **Objective:** Validate system correctness through testing and deploy to production environments.
- **Key Tasks:**
  - Write unit tests for preprocessing transformations and prediction endpoints.
  - Containerize the application with a `Dockerfile`.
  - Deploy the system to cloud environments (e.g. Render).
- **Deliverable:** Containerized application running in production.
