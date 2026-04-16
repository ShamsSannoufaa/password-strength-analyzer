import math
import pandas as pd


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


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["length"] = out["password"].str.len()
    out["has_upper"] = out["password"].apply(lambda x: int(any(c.isupper() for c in x)))
    out["has_lower"] = out["password"].apply(lambda x: int(any(c.islower() for c in x)))
    out["has_digit"] = out["password"].apply(lambda x: int(any(c.isdigit() for c in x)))
    out["has_special"] = out["password"].apply(lambda x: int(any(not c.isalnum() for c in x)))

    out["count_upper"] = out["password"].apply(lambda x: sum(1 for c in x if c.isupper()))
    out["count_lower"] = out["password"].apply(lambda x: sum(1 for c in x if c.islower()))
    out["count_digit"] = out["password"].apply(lambda x: sum(1 for c in x if c.isdigit()))
    out["count_special"] = out["password"].apply(lambda x: sum(1 for c in x if not c.isalnum()))

    out["entropy"] = out["password"].apply(entropy_estimate)

    return out