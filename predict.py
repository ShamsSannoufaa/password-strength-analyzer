import math
import joblib
import pandas as pd

from suggest import generate_stronger_passwords


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


def has_upper(pw: str) -> int:
    return int(any(c.isupper() for c in pw))


def has_lower(pw: str) -> int:
    return int(any(c.islower() for c in pw))


def has_digit(pw: str) -> int:
    return int(any(c.isdigit() for c in pw))


def has_special(pw: str) -> int:
    return int(any(not c.isalnum() for c in pw))


def count_upper(pw: str) -> int:
    return sum(1 for c in pw if c.isupper())


def count_lower(pw: str) -> int:
    return sum(1 for c in pw if c.islower())


def count_digit(pw: str) -> int:
    return sum(1 for c in pw if c.isdigit())


def count_special(pw: str) -> int:
    return sum(1 for c in pw if not c.isalnum())


def entropy_estimate(pw: str) -> float:
    charset = 0

    if any(c.islower() for c in pw):
        charset += 26
    if any(c.isupper() for c in pw):
        charset += 26
    if any(c.isdigit() for c in pw):
        charset += 10
    if any(not c.isalnum() for c in pw):
        charset += 32

    if charset == 0:
        return 0.0

    return len(pw) * math.log2(charset)


def extract_single_password_features(password: str) -> pd.DataFrame:
    row = {
        "length": len(password),
        "has_upper": has_upper(password),
        "has_lower": has_lower(password),
        "has_digit": has_digit(password),
        "has_special": has_special(password),
        "count_upper": count_upper(password),
        "count_lower": count_lower(password),
        "count_digit": count_digit(password),
        "count_special": count_special(password),
        "entropy": entropy_estimate(password),
    }

    return pd.DataFrame([row], columns=FEATURE_COLUMNS)


def main() -> None:
    model = joblib.load("model_rf_v2.pkl")

    password = input("Enter a password: ").strip()

    if not password:
        print("Password cannot be empty.")
        return

    X_input = extract_single_password_features(password)
    prediction = model.predict(X_input)[0]

    print("\nPassword Strength:", prediction)

    if prediction in ["weak", "medium"]:
        print("\nSuggested stronger passwords:")
        for suggestion in generate_stronger_passwords(password, count=3):
            print("-", suggestion)


if __name__ == "__main__":
    main()