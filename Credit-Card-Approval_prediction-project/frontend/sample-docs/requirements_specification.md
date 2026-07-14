# Requirements Specification

This document details the functional, non-functional, and interface requirements for the automated Credit Card Approval Prediction system.

## 1. System Requirements

### 1.1 Functional Requirements (FR)
- **FR-1: User Inputs:** The system must collect applicant demographics and financial statistics, including gender, vehicle ownership, real estate ownership, income, family status, housing style, age, and employment tenure.
- **FR-2: Dynamic Fields:** The web form must dynamically update its inputs. If the user selects "Unemployed" as their employment status, the system must disable and hide the employment tenure field to prevent illogical input states.
- **FR-3: Automated Preprocessing:** The backend must automatically clean and format raw form data. This includes converting years to days, calculating financial metrics, one-hot encoding categorical features, and aligning columns to match the trained model's feature structure.
- **FR-4: Classification Execution:** The system must run the preprocessed record through the serialized Random Forest classifier to determine approval ("Approved" or "Denied").
- **FR-5: Risk Audit Log Generation:** The system must evaluate the applicant against predefined rule thresholds to output a detailed audit explaining the decision (e.g. assessing whether income meets stability bounds or if employment duration is insufficient).
- **FR-6: Persistent Logs:** The system must write a record of every prediction query, input value, and output decision to a persistent JSON-based log database for historical tracking.
- **FR-7: Static Analysis Gallery:** The interface must host and display training metrics, including data exploration charts, ROC curves, and correlation matrices.

### 1.2 Non-Functional Requirements (NFR)
- **NFR-1: Performance & Latency:** The end-to-end model inference, risk audit generation, database writing, and page rendering must take less than 1.5 seconds.
- **NFR-2: Responsiveness:** The web interface must adjust dynamically to standard device viewports, remaining fully readable on mobile phones, tablets, laptops, and desktops.
- **NFR-3: Security & Input Validation:** All input values must undergo backend validation to reject malformed payloads, negative income values, or unrealistic age values (e.g., age below 18 or above 100).
- **NFR-4: Maintainability:** The application must maintain a modular separation between frontend template views (`frontend/`), preprocessing utilities (`app/`), and main routing logic (`main.py`).

---

## 2. User Scenarios & Use Cases

### Use Case 1: Standard Application Assessment
- **Actor:** Underwriter or Applicant
- **Flow:**
  1. User navigates to the Predictor tab.
  2. User inputs demographic data and enters age (e.g. 34) and years employed (e.g. 8).
  3. User clicks the "Evaluate Application" button.
  4. System displays an inline loading spinner indicating feature alignment and model inference.
  5. The form container slides open to display a risk report with an "Approved" badge, along with a list explaining the decision.

### Use Case 2: Unemployed Applicant Assessment
- **Actor:** Underwriter or Applicant
- **Flow:**
  1. User navigates to the Predictor tab.
  2. User selects "Unemployed" under employment status.
  3. The interface immediately hides the "Years of Employment" field and sets the duration value to 0.
  4. User completes the form and submits.
  5. The backend maps employment duration to the database sentinel value `365243` and executes prediction.
  6. System displays the decision ("Denied") with audit logs highlighting the risk of unemployment.
