import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split


FEATURE_COLUMNS = [
    "length",
    "has_upper",
    "has_lower",
    "has_digit",
    "has_special",
    "count_upper",
    "count_lower",
    "count_digit",
    "count_special",
    "entropy",
]


def train_and_evaluate(df: pd.DataFrame):
    X = df[FEATURE_COLUMNS]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("\n=== Random Forest ===")
    rf = RandomForestClassifier(
        n_estimators=150,
        random_state=42,
        class_weight="balanced"
    )
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)

    print("Accuracy:", round(accuracy_score(y_test, rf_preds), 4))
    print("\nClassification Report:\n", classification_report(y_test, rf_preds))
    print("Confusion Matrix:\n", confusion_matrix(y_test, rf_preds))

    print("\nTop Feature Importances:")
    importances = pd.Series(rf.feature_importances_, index=FEATURE_COLUMNS).sort_values(ascending=False)
    print(importances.head(10))

    print("\n=== Logistic Regression Baseline ===")
    lr = LogisticRegression(max_iter=2000, class_weight="balanced")
    lr.fit(X_train, y_train)
    lr_preds = lr.predict(X_test)

    print("Accuracy:", round(accuracy_score(y_test, lr_preds), 4))
    print("\nClassification Report:\n", classification_report(y_test, lr_preds))
    print("Confusion Matrix:\n", confusion_matrix(y_test, lr_preds))

    return rf, lr