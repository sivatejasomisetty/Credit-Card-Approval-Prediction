# Technical Development Notes

This document highlights the development challenges, design patterns, and engineering implementations of the credit card predictor application.

---

## 1. Demographic Translation Layer

### The Problem
The machine learning model expects age and employment tenure represented as a negative number of days before the current date (e.g. `DAYS_BIRTH = -12500` and `DAYS_EMPLOYED = -3000`). Expecting users to calculate and input negative days is impractical and error-prone.

### The Solution
We implemented a preprocessing translation layer inside `app/preprocess.py` to map intuitive inputs to their model equivalents.
- **Age Translation:**
  - The frontend form collects the applicant's age in positive years.
  - The backend preprocessor converts this to days using the formula:
    $$\text{DAYS\_BIRTH} = -\text{floor}(\text{AGE\_YEARS} \times 365.25)$$
- **Employment Translation:**
  - The frontend form collects employment duration in positive years.
  - The preprocessor converts this to:
    $$\text{DAYS\_EMPLOYED} = -\text{floor}(\text{YEARS\_EMPLOYED} \times 365.25)$$

---

## 2. Dynamic Unemployed State Management

To handle unemployed applicants correctly, we implemented state management across both the frontend and backend:

### 2.1 Frontend JavaScript State Handling
In `frontend/predict.html`, a change listener is registered to the employment status dropdown:
- If the status is set to "Employed", the "Years of Employment" input is shown and marked as required.
- If the status is set to "Unemployed", the "Years of Employment" input is hidden and its value is set to `0`.

### 2.2 Backend Preprocessor Mapping
In the training dataset, unemployed status is represented by the sentinel value `365243` in the `DAYS_EMPLOYED` column.
- Inside `app/preprocess.py`, the system checks:
  - If `EMPLAYMENT_STATUS` equals `"Unemployed"`, `DAYS_EMPLOYED` is set directly to `365243`.
  - The derived boolean flag `EMPLOYED` is set to `False` and `YEARS_EMPLOYED` is set to `0`.

---

## 3. Persistent Prediction Logging

To track historical performance and display prediction logs on the Bento dashboard homepage, we built a JSON-based database:
- **Location:** `models/predictions/prediction_summary.json`
- **Process Flow:**
  1. On each inference request, the inputs (income, age, employment, education) and the output decision (approved or denied) are structured as a dictionary.
  2. The system reads the existing JSON array, appends the new record, and writes the updated array back to disk.
  3. The homepage route parses this JSON file to render the **Decision History Log** table.
- **Safety Fallback:** If the file does not exist or is empty, the system returns an empty list, preventing page load failures.
