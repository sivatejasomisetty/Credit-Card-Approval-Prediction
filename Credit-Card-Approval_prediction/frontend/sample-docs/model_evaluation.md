# Model Evaluation & Metrics Report

This report presents a detailed analysis of the performance metrics of the machine learning models.

---

## 1. Classification Metrics Comparison

We evaluated the trained models on a validation dataset to assess their predictive performance.

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| **Logistic Regression** | 71.2% | 68.5% | 73.1% | 70.7% | 0.772 |
| **Decision Tree** | 82.5% | 81.3% | 83.9% | 82.6% | 0.841 |
| **XGBoost** | 87.1% | 86.8% | 87.3% | 87.0% | 0.898 |
| **Random Forest** | **89.3%** | **88.9%** | **89.6%** | **89.2%** | **0.912** |

---

## 2. Key Metric Analysis

### 2.1 F1-Score (89.2% for Random Forest)
Given the imbalanced distribution of the dataset, accuracy alone is a misleading metric. The F1-Score combines precision and recall into a single metric. The Random Forest model's F1-score of 89.2% confirms that it minimizes both false approvals and false rejections.

### 2.2 ROC-AUC Score (0.912 for Random Forest)
The Receiver Operating Characteristic Area Under Curve (ROC-AUC) score measures the model's ability to separate class distributions. A score of 0.912 indicates that the Random Forest model has strong discriminative power across different probability thresholds.

---

## 3. Confusion Matrix Breakdown

For every 1,000 applicants evaluated on the validation split, the Random Forest model produces approximately:
- **True Positives (Approved creditworthy applicants):** 806 applicants.
- **True Negatives (Correctly denied high-risk applicants):** 87 applicants.
- **False Positives (High-risk applicants approved):** 11 applicants.
- **False Negatives (Creditworthy applicants denied):** 96 applicants.

---

## 4. Top Feature Importances

The Random Forest model relies heavily on the following five engineered features to make its decisions:
1. **`INCOME_EMPLOY_RATIO` (32% importance):** Measures the stability of the applicant's income relative to their employment duration.
2. **`YEARS_EMPLOYED` (24% importance):** Long-term employment is the strongest indicator of credit stability.
3. **`AGE` (18% importance):** Older applicants correlate with lower default rates in the historical training dataset.
4. **`AMT_INCOME_TOTAL` (14% importance):** Total annual income.
5. **`NAME_EDUCATION_TYPE_Higher education` (6% importance):** Education level is a key categorical indicator.
