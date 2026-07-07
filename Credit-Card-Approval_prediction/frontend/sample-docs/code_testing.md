# Code Testing & Verification Plan

This document outlines the testing strategy, test suites, and instructions for running unit and integration tests.

---

## 1. Testing Strategy

The application uses Python's standard `unittest` framework to verify backend logic, database operations, and data transformations.

### 1.1 Preprocessing Validation
We test the `prepare_input_record` function in `app/preprocess.py` to ensure raw dictionary inputs from the web form are correctly transformed:
- **Test Case 1: Standard Input:** Verifies that ages and employment years are translated into negative days.
- **Test Case 2: Unemployed State:** Verifies that selecting "Unemployed" sets `DAYS_EMPLOYED` to `365243`, `EMPLOYED` to `False`, and `YEARS_EMPLOYED` to `0`.
- **Test Case 3: Column Alignment:** Verifies that the output DataFrame contains exactly 55 columns, filled with `0.0` for missing categories.

### 1.2 Routing and Inference Validation
We mock the Flask client to test endpoints in `main.py`:
- **Test Case 4: Dashboard Page:** Verifies that `GET /` returns HTTP 200.
- **Test Case 5: Predictor API:** Verifies that sending a valid JSON payload to `POST /predict` returns a decision and audit logs.

---

## 2. Test Suites Structure

All test scripts are located inside the `tests/` directory:

```dir
tests/
├── __init__.py
├── test_preprocess.py       # Unit tests for preprocessing transformations
└── test_routes.py           # Integration tests for Flask routing
```

---

## 3. Running the Test Suite

Run the following commands from the root directory of the project:

### Run All Tests
```bash
python -m unittest discover -s tests
```

### Run Preprocessing Tests Only
```bash
python -m unittest tests/test_preprocess.py
```

### Run Routing Tests Only
```bash
python -m unittest tests/test_routes.py
```

### Checking Code Coverage
To check test coverage, install the `coverage` library and run:
```bash
pip install coverage
coverage run -m unittest discover -s tests
coverage report -m
```
This generates a detailed code coverage report, helping you identify untested code paths.
