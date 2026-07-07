# Application User & Operations Guide

This guide provides instructions on how to use the Credit Card Approval Prediction interface.

---

## 1. Homepage & Dashboard View

When you open the application at `http://localhost:5000`, the **Dashboard** is the default view.

### 1.1 Bento Grid Panels
The dashboard uses a Bento Grid layout to display high-level stats:
- **Processed Panel:** Shows the total number of applications processed by the system.
- **Approval Rate Panel:** Shows the percentage of approved applications.
- **Average Income Panel:** Shows the average income of applicants.

### 1.2 Decision History Log
At the bottom of the dashboard, the **Decision History Log** displays past applications in a scrollable table:
- It lists the timestamp, age, income, employment duration, and final decision (Approved/Denied) for each record.
- This table updates in real-time as new predictions are made.

---

## 2. Running a Prediction

To evaluate an applicant, navigate to the **Predictor** tab in the top navigation bar.

### 2.1 Form Sections
The form is split into three main sections:
- **Demographics:** Gender, Car Ownership, Realty Ownership, and Number of Children.
- **Financial Profile:** Annual Income, Income Source, Education Level, Family Status, and Housing Type.
- **Timeline Metrics:**
  - **Age (in Years):** Enter the applicant's age (must be 18 or older).
  - **Employment Status:** Select "Employed" or "Unemployed".
  - **Years of Employment:** If "Employed" is selected, enter the number of years. If "Unemployed" is selected, this field is hidden automatically.

### 2.2 Autofill Utility
To run a quick test:
1. Click the **Autofill Random** button.
2. The form fields will populate with randomized data.
3. Click **Evaluate Application** to submit the form.

---

## 3. Understanding the Risk Audit Report

After submitting the form, the page scrolls to the top of the predictor card, displays a short loading animation, and then reveals the **Risk Audit Report**:

- **Decision Badge:** Displays a green **Approved** or red **Denied** badge based on the model's prediction.
- **Audit Findings:** Explains the reasoning behind the decision based on predefined business rules:
  - **Income Stability:** Checks if the annual income is above or below baseline thresholds.
  - **Employment Check:** Evaluates whether the applicant has a steady employment history.
  - **Demographic Balance:** Analyzes features like housing type and family size to evaluate stability.
