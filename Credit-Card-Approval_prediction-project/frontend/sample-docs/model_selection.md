# Model Evaluation & Selection Strategy

This document details the selection and comparison of machine learning models for the credit card approval application.

---

## 1. Algorithm Comparison

We evaluated four machine learning classifiers to find the best balance of classification performance, stability, and run-time speed.

### 1.1 Logistic Regression
- **Description:** A simple linear model used as a baseline.
- **Pros:** Highly interpretable, fast inference, and low memory footprint.
- **Cons:** Struggles to capture non-linear relationships and interactions between demographic variables (e.g. how education level interacts with income).

### 1.2 Decision Tree
- **Description:** A non-linear, tree-based classifier.
- **Pros:** Highly interpretable, handles both categorical and continuous data without complex scaling.
- **Cons:** High variance and highly prone to overfitting the training dataset.

### 1.3 XGBoost (Extreme Gradient Boosting)
- **Description:** An optimized gradient boosted decision tree library.
- **Pros:** Excellent performance metrics and handles missing values natively.
- **Cons:** High memory usage and complex hyperparameter tuning.

### 1.4 Random Forest
- **Description:** An ensemble method that trains multiple decision trees and aggregates their predictions.
- **Pros:** Robust against overfitting, performs well on mixed data types, and provides feature importance scores.
- **Cons:** Larger file size (binary is ~6MB) and higher memory usage than linear models.

---

## 2. Selection Metrics

Models were evaluated on a validation split using the following metrics:
- **Accuracy:** The ratio of correct predictions to total predictions.
- **Recall (Sensitivity):** The ability to identify high-risk applicants. This is critical for minimizing credit defaults.
- **F1-Score:** The harmonic mean of precision and recall, serving as a balanced metric for imbalanced classes.
- **ROC-AUC:** Measures the model's ability to distinguish between classes across all decision thresholds.

---

## 3. Final Production Selection

The **Random Forest** model was selected for deployment:
- **Generalization:** Random Forest achieved an F1-score of 89.2% and a ROC-AUC of 0.912, outperforming the other candidates on the validation split.
- **Stability:** The ensemble approach reduces prediction variance, making it less sensitive to minor variations in applicant input.
- **Feature Importance:** It allows us to calculate feature contributions, which help generate the explanation rules in the risk audit report.
- **Serialization:** The final model is serialized to `models/random_forest.joblib` and loaded into memory on application startup.
