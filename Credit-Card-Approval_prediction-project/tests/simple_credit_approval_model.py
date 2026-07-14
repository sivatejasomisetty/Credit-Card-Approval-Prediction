import argparse
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data and eda"
MODEL_PATH = REPO_ROOT / "models" / "simple_credit_approval_model.joblib"


def build_feature_frame(application_record, credit_record, include_target=False):
    application_record = application_record.copy()
    credit_record = credit_record.copy()

    application_record["EMPLOYED"] = application_record["DAYS_EMPLOYED"] != 365243
    application_record["YEARS_EMPLOYED"] = application_record["DAYS_EMPLOYED"].apply(
        lambda x: max(-x / 365, 0) if x != 365243 else 0
    )
    application_record["INCOME_EMPLOY_RATIO"] = application_record.apply(
        lambda row: row["AMT_INCOME_TOTAL"] / row["YEARS_EMPLOYED"]
        if row["YEARS_EMPLOYED"] > 0
        else row["AMT_INCOME_TOTAL"],
        axis=1,
    )

    status_map = {"X": -1, "C": 0, "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
    credit_record["STATUS_NUM"] = credit_record["STATUS"].map(status_map).fillna(0)
    credit_record = credit_record.sort_values(["ID", "MONTHS_BALANCE"], ascending=[True, False])

    def get_trend(x):
        return x.diff().mean()

    agg_funcs = {"STATUS_NUM": ["max", "min", "mean", "last", get_trend]}
    features_credit_record = credit_record.groupby("ID").agg(agg_funcs)
    features_credit_record.columns = ["STATUS_MAX", "STATUS_MIN", "STATUS_MEAN", "STATUS_LAST", "STATUS_TREND"]
    features_credit_record.reset_index(inplace=True)
    features_credit_record["NUM_LATE_MONTHS"] = credit_record.groupby("ID")["STATUS_NUM"].apply(
        lambda x: (x > 0).sum()
    ).values

    df = application_record.merge(features_credit_record, on="ID", how="left")
    df[["STATUS_MAX", "STATUS_MIN", "STATUS_MEAN", "STATUS_LAST", "STATUS_TREND", "NUM_LATE_MONTHS"]] = df[
        ["STATUS_MAX", "STATUS_MIN", "STATUS_MEAN", "STATUS_LAST", "STATUS_TREND", "NUM_LATE_MONTHS"]
    ].fillna(0)

    if include_target:
        def make_target(row):
            income_ok = row["AMT_INCOME_TOTAL"] >= 120000
            employment_ok = row["YEARS_EMPLOYED"] >= 2
            credit_ok = row["STATUS_MAX"] <= 0 and row["STATUS_MIN"] <= 0 and row["STATUS_MEAN"] <= 0 and row["STATUS_LAST"] <= 0 and row["NUM_LATE_MONTHS"] <= 1
            family_ok = row["CNT_CHILDREN"] <= 2 and row["CNT_FAM_MEMBERS"] <= 4
            score = sum([income_ok, employment_ok, credit_ok, family_ok])
            return 1 if score >= 3 else 0

        df["TARGET"] = df.apply(make_target, axis=1)
        feature_frame = df.drop(columns=["ID", "TARGET"])
        target = df["TARGET"]
    else:
        feature_frame = df.drop(columns=["ID"])
        target = None

    feature_frame = feature_frame.fillna(0)
    categorical_columns = feature_frame.select_dtypes(include=["object", "category", "bool", "string"]).columns.tolist()
    feature_frame = pd.get_dummies(feature_frame, columns=categorical_columns, dummy_na=False)
    feature_frame = feature_frame.astype(float)

    return feature_frame, target


def prepare_data():
    application_record = pd.read_csv(DATA_DIR / "application_record.csv")
    credit_record = pd.read_csv(DATA_DIR / "credit_record.csv")
    feature_frame, target = build_feature_frame(application_record, credit_record, include_target=True)
    return feature_frame, target


def train_model(model_path=MODEL_PATH):
    X, y = prepare_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=2000, class_weight="balanced", solver="liblinear")
    model.fit(X_train, y_train)

    test_probabilities = model.predict_proba(X_test)[:, 1]
    threshold = 0.6
    predictions = (test_probabilities >= threshold).astype(int)
    accuracy = accuracy_score(y_test, predictions)

    joblib.dump({"model": model, "feature_columns": X.columns.tolist(), "threshold": threshold}, model_path)

    print("Model trained successfully.")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"Model saved to: {model_path}")


def predict_from_files(application_path, credit_path, model_path=MODEL_PATH):
    artifact = joblib.load(model_path)
    model = artifact["model"]
    feature_columns = artifact["feature_columns"]

    application_record = pd.read_csv(application_path)
    credit_record = pd.read_csv(credit_path)
    feature_frame, _ = build_feature_frame(application_record, credit_record, include_target=False)
    feature_frame = feature_frame.reindex(columns=feature_columns, fill_value=0)

    probabilities = model.predict_proba(feature_frame)[:, 1]
    threshold = artifact.get("threshold", 0.6)
    predictions = (probabilities >= threshold).astype(int)

    results = pd.DataFrame({
        "prediction": predictions,
        "probability": probabilities,
    })
    results["prediction_label"] = results["prediction"].map({1: "Approved", 0: "Declined"})
    return results


def main():
    parser = argparse.ArgumentParser(description="Train or predict credit card approval using the simple model")
    parser.add_argument("--predict", action="store_true", help="Run prediction instead of training")
    parser.add_argument("--applicant-csv", type=Path, help="Path to the applicant CSV file")
    parser.add_argument("--credit-csv", type=Path, help="Path to the credit history CSV file")
    parser.add_argument("--model", type=Path, default=MODEL_PATH, help="Path to the saved model file")
    args = parser.parse_args()

    if args.predict:
        if not args.applicant_csv or not args.credit_csv:
            raise ValueError("Both --applicant-csv and --credit-csv are required for prediction")
        results = predict_from_files(args.applicant_csv, args.credit_csv, args.model)
        try:
            print(results.to_string(index=False))
        except BrokenPipeError:
            sys.exit(0)
    else:
        train_model(args.model)


if __name__ == "__main__":
    main()
