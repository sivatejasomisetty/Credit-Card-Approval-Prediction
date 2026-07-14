# Risk Assessment & Mitigation Strategies

This document identifies potential technical, operational, and data risks associated with the deployment of the Credit Card Approval Prediction system, along with strategies to mitigate them.

---

## 1. Classification & Data Risks

### Risk 1: High Class Imbalance
- **Category:** Data Risk
- **Description:** The dataset contains far more approved applications than denied ones. A standard model might achieve high accuracy by simply predicting "Approved" for all applicants, failing to identify risky candidates.
- **Impact:** High. Leads to financial defaults and losses for the issuer.
- **Mitigation:** 
  - Apply class weighting (`class_weight='balanced'`) during Random Forest training to penalize misclassifications of the minority (denied) class.
  - Evaluate model performance using ROC-AUC and F1-score rather than simple accuracy to ensure balanced prediction capability.

### Risk 2: Preprocessing Pipelines Mismatch
- **Category:** Technical Risk
- **Description:** Preprocessing features differently during model training versus web form execution can cause index mismatches or invalid predictions.
- **Impact:** High. May result in model crashes or incorrect predictions in production.
- **Mitigation:**
  - Consolidate all preprocessing logic inside a unified file (`app/preprocess.py`).
  - Align columns explicitly using a saved feature index list to ensure that the input shape always matches the expected 55-column vector.

---

## 2. Infrastructure & Operations Risks

### Risk 3: Model Serialization Failures
- **Category:** Infrastructure Risk
- **Description:** The Flask server may fail to start or crash if the `.joblib` model binary is missing, corrupted, or incompatible with the installed scikit-learn version.
- **Impact:** High. Leads to system downtime.
- **Mitigation:**
  - Implement try-except blocks during application initialization in `main.py`.
  - Fall back to a standard decision tree model or log a clean, descriptive error message if the primary model cannot be loaded.
  - Pin the scikit-learn dependency version in `requirements.txt` to prevent runtime serialization mismatches.

### Risk 4: Incorrect Data Entry (Human Error)
- **Category:** Operational Risk
- **Description:** Users may enter invalid or out-of-bounds values in the predictor form, such as negative income values or unrealistic ages.
- **Impact:** Medium. Leads to strange model predictions or backend processing exceptions.
- **Mitigation:**
  - Implement frontend HTML form restrictions (e.g. `min="18"` and `max="100"` for age, `min="0"` for income).
  - Add backend validation in `main.py` to check ranges and return structured error messages for invalid inputs.
