import pandas as pd
import joblib
import math
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score
)


BASE_DIR = Path(__file__).resolve().parent.parent

NORMAL_PATH = BASE_DIR / "data" / "rockyou.txt"
STRONG_PATH = BASE_DIR / "data" / "strong.txt"
MODEL_PATH = BASE_DIR / "model_rf_v2.pkl"
OUTPUT_PATH = BASE_DIR / "confusion_matrix_cyber_premium.png"


FEATURE_COLUMNS = [
    "length", "has_upper", "has_lower", "has_digit", "has_special",
    "count_upper", "count_lower", "count_digit", "count_special", "entropy"
]


def entropy(password):
    charset = 0

    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(not c.isalnum() for c in password):
        charset += 32

    if charset == 0:
        return 0.0

    return len(password) * math.log2(charset)


def label_password(password):
    password = str(password)

    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    diversity = sum([has_upper, has_lower, has_digit, has_special])

    if length < 8 or diversity <= 1:
        return "weak"
    elif length >= 12 and diversity >= 3:
        return "strong"
    else:
        return "medium"


def extract_features(passwords):
    rows = []

    for password in passwords:
        password = str(password)

        rows.append({
            "length": len(password),
            "has_upper": int(any(c.isupper() for c in password)),
            "has_lower": int(any(c.islower() for c in password)),
            "has_digit": int(any(c.isdigit() for c in password)),
            "has_special": int(any(not c.isalnum() for c in password)),
            "count_upper": sum(1 for c in password if c.isupper()),
            "count_lower": sum(1 for c in password if c.islower()),
            "count_digit": sum(1 for c in password if c.isdigit()),
            "count_special": sum(1 for c in password if not c.isalnum()),
            "entropy": entropy(password),
        })

    return pd.DataFrame(rows, columns=FEATURE_COLUMNS)


def read_password_file(path, limit=30000):
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    passwords = []

    with open(path, "r", encoding="latin-1", errors="ignore") as file:
        for line in file:
            password = line.strip()

            if password:
                passwords.append(password)

            if len(passwords) >= limit:
                break

    return passwords


print("Checking file paths:")
print("Normal/RockYou file:", NORMAL_PATH)
print("Strong file:", STRONG_PATH)
print("Model file:", MODEL_PATH)

normal_passwords = read_password_file(NORMAL_PATH, limit=30000)
strong_passwords = read_password_file(STRONG_PATH, limit=30000)

all_passwords = normal_passwords + strong_passwords

df = pd.DataFrame({"password": all_passwords})
df["label"] = df["password"].apply(label_password)

print("\nDataset distribution:")
print(df["label"].value_counts())

X = extract_features(df["password"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = joblib.load(MODEL_PATH)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:")
print(accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

labels = ["weak", "medium", "strong"]
cm = confusion_matrix(y_test, y_pred, labels=labels)


# ==============================
# PREMIUM CYBER VISUAL STYLE
# ==============================
cyber_cmap = LinearSegmentedColormap.from_list(
    "cyber_purple",
    [
        "#080014",
        "#190033",
        "#330066",
        "#5A00A8",
        "#9B2CFF",
        "#FF5CF7"
    ]
)

fig, ax = plt.subplots(figsize=(10, 7), dpi=160)
fig.patch.set_facecolor("#070014")
ax.set_facecolor("#0B021A")

# Soft gradient background
gradient = np.linspace(0, 1, 512)
gradient = np.vstack((gradient, gradient))
ax_bg = fig.add_axes([0, 0, 1, 1], zorder=-1)
ax_bg.imshow(
    gradient,
    aspect="auto",
    cmap=LinearSegmentedColormap.from_list(
        "bg",
        ["#05000F", "#16002F", "#2A005A", "#070014"]
    ),
    extent=[0, 1, 0, 1],
    alpha=1
)
ax_bg.axis("off")

im = ax.imshow(cm, interpolation="nearest", cmap=cyber_cmap)

ax.set_title(
    "PASSWORD STRENGTH CLASSIFIER",
    fontsize=20,
    fontweight="bold",
    color="#FF66F5",
    pad=22
)

ax.text(
    0.5,
    1.04,
    "Confusion Matrix Analysis",
    transform=ax.transAxes,
    ha="center",
    va="center",
    fontsize=12,
    color="#D8B4FE",
    fontweight="bold"
)

ax.set_xlabel(
    "PREDICTED LABEL",
    fontsize=12,
    fontweight="bold",
    color="#F5D0FE",
    labelpad=14
)

ax.set_ylabel(
    "TRUE LABEL",
    fontsize=12,
    fontweight="bold",
    color="#F5D0FE",
    labelpad=14
)

ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))
ax.set_xticklabels([label.upper() for label in labels], color="#F5D0FE", fontweight="bold")
ax.set_yticklabels([label.upper() for label in labels], color="#F5D0FE", fontweight="bold")

ax.tick_params(axis="both", colors="#F5D0FE", length=0)

for spine in ax.spines.values():
    spine.set_edgecolor("#FF5CF7")
    spine.set_linewidth(1.6)

# Grid lines
ax.set_xticks(np.arange(-.5, len(labels), 1), minor=True)
ax.set_yticks(np.arange(-.5, len(labels), 1), minor=True)
ax.grid(which="minor", color="#C084FC", linestyle="-", linewidth=1.2, alpha=0.45)
ax.tick_params(which="minor", bottom=False, left=False)

# Cell values
threshold = cm.max() / 2

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        value = cm[i, j]

        text_color = "#FFFFFF" if value > threshold else "#F0ABFC"

        ax.text(
            j,
            i,
            f"{value}",
            ha="center",
            va="center",
            color=text_color,
            fontsize=16,
            fontweight="bold"
        )

# Colorbar
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.ax.tick_params(colors="#F5D0FE")
cbar.outline.set_edgecolor("#FF5CF7")
cbar.outline.set_linewidth(1.2)

# Footer
fig.text(
    0.5,
    0.035,
    f"Accuracy: {accuracy:.2%}   |   Model: Random Forest V2   |   Dataset: RockYou + Strong Passwords",
    ha="center",
    fontsize=10.5,
    color="#E9D5FF",
    fontweight="bold"
)

fig.text(
    0.5,
    0.012,
    "Password Strength Analysis and Prediction for Cybersecurity",
    ha="center",
    fontsize=9,
    color="#C084FC"
)

plt.tight_layout(rect=[0.04, 0.07, 0.96, 0.94])
plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()

print(f"\nCyber premium confusion matrix saved to: {OUTPUT_PATH}")