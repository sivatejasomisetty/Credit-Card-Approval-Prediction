# Data Dictionary & Schema Documentation

This document provides a comprehensive breakdown of all variables used in the data pipeline, preprocessing scripts, and machine learning models for the Credit Card Approval Prediction project.

---

## 1. Demographic & Personal Attributes

### CODE_GENDER
- **Description:** Biological gender of the applicant.
- **Type:** Categorical (One-Hot Encoded on backend)
- **Values:** `M` (Male), `F` (Female)
- **Model Mapping:** Converted to dummy variables (`CODE_GENDER_M`).

### FLAG_OWN_CAR
- **Description:** Indicates whether the applicant owns an automobile.
- **Type:** Categorical
- **Values:** `Y` (Yes), `N` (No)
- **Model Mapping:** Converted to binary/dummy fields (`FLAG_OWN_CAR_Y`).

### FLAG_OWN_REALTY
- **Description:** Indicates whether the applicant owns real estate (house or property).
- **Type:** Categorical
- **Values:** `Y` (Yes), `N` (No)
- **Model Mapping:** Converted to binary/dummy fields (`FLAG_OWN_REALTY_Y`).

### CNT_CHILDREN
- **Description:** Total number of children associated with the applicant.
- **Type:** Integer
- **Range:** 0 to 20+

---

## 2. Financial & Employment Attributes

### AMT_INCOME_TOTAL
- **Description:** Annual income of the applicant, represented in USD or local currency.
- **Type:** Continuous (Float)
- **Validation:** Must be greater than 0.

### NAME_INCOME_TYPE
- **Description:** Category describing the applicant's primary source of income.
- **Type:** Categorical
- **Values:**
  - `Working`: Standard salaried employee.
  - `Commercial associate`: Business owner or self-employed associate.
  - `Pensioner`: Retired individual collecting pension.
  - `State servant`: Government employee.
  - `Student`: Currently enrolled student.

### NAME_EDUCATION_TYPE
- **Description:** Highest education level attained by the applicant.
- **Type:** Categorical
- **Values:**
  - `Higher education`: College degree or above.
  - `Secondary / secondary special`: Completed high school or vocational training.
  - `Incomplete higher`: Some university education but no degree.
  - `Lower secondary`: Completed middle school.
  - `Academic degree`: Post-graduate or research degree.

### NAME_FAMILY_STATUS
- **Description:** Marital status of the applicant.
- **Type:** Categorical
- **Values:** `Civil marriage`, `Married`, `Single / not married`, `Separated`, `Widow`.

### NAME_HOUSING_TYPE
- **Description:** Residential living arrangement.
- **Type:** Categorical
- **Values:** `House / apartment`, `Rented apartment`, `With parents`, `Municipal apartment`, `Co-op apartment`, `Office apartment`.

### OCCUPATION_TYPE
- **Description:** Industry category of the applicant's job.
- **Type:** Categorical
- **Values:** `Laborers`, `Core staff`, `Sales staff`, `Managers`, `Drivers`, `High skill tech staff`, `Accountants`, `Medicine staff`, `Security staff`, `Cooking staff`, `Cleaning staff`, `Private service staff`, `Low-skill Laborers`, `Waiters/barmen staff`, `Secretaries`, `HR staff`, `IT staff`, `Unknown`.

---

## 3. Pipeline Transformations & Engineering Features

### AGE (derived from AGE_YEARS)
- **Description:** Calculated age of the applicant.
- **Formula:** 
  $$\text{AGE} = \text{floor}\left(\frac{-\text{DAYS\_BIRTH}}{365.25}\right)$$

### YEARS_EMPLOYED (derived from YEARS_EMPLOYED_INPUT)
- **Description:** Number of years spent in the current job.
- **Formula:**
  $$\text{YEARS\_EMPLOYED} = \frac{-\text{DAYS\_EMPLOYED}}{365.25}$$
  *(Set to `0` if applicant is unemployed).*

### INCOME_EMPLOY_RATIO
- **Description:** Ratio of total income to employment length, measuring income stability.
- **Formula:**
  $$\text{INCOME\_EMPLOY\_RATIO} = \frac{\text{AMT\_INCOME\_TOTAL}}{\text{YEARS\_EMPLOYED}}$$
  *(If `YEARS_EMPLOYED` is 0, equals `AMT_INCOME_TOTAL`).*
