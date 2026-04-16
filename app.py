import streamlit as st
import joblib
import pandas as pd
import math

from suggest import generate_stronger_passwords

# ===== CONFIG =====
st.set_page_config(page_title="Password Analyzer", page_icon="🔐", layout="centered")

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


# ===== FEATURE FUNCTIONS =====
def has_upper(pw):
    return int(any(c.isupper() for c in pw))


def has_lower(pw):
    return int(any(c.islower() for c in pw))


def has_digit(pw):
    return int(any(c.isdigit() for c in pw))


def has_special(pw):
    return int(any(not c.isalnum() for c in pw))


def count_upper(pw):
    return sum(1 for c in pw if c.isupper())


def count_lower(pw):
    return sum(1 for c in pw if c.islower())


def count_digit(pw):
    return sum(1 for c in pw if c.isdigit())


def count_special(pw):
    return sum(1 for c in pw if not c.isalnum())


def entropy(pw):
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


def extract_features(password):
    data = {
        "length": len(password),
        "has_upper": has_upper(password),
        "has_lower": has_lower(password),
        "has_digit": has_digit(password),
        "has_special": has_special(password),
        "count_upper": count_upper(password),
        "count_lower": count_lower(password),
        "count_digit": count_digit(password),
        "count_special": count_special(password),
        "entropy": entropy(password),
    }
    return pd.DataFrame([data], columns=FEATURE_COLUMNS)


# ===== MODEL SELECT =====
st.title("🔐 Password Strength Analyzer")
st.write("Analyze password security and compare different model versions.")

model_choice = st.selectbox(
    "Select model version:",
    ["V1", "V2"]
)

if model_choice == "V1":
    model = joblib.load("model_rf_v1.pkl")
    model_info = "Initial labeling strategy"
else:
    model = joblib.load("model_rf_v2.pkl")
    model_info = "Revised labeling strategy"

st.caption(f"Loaded model: {model_choice} — {model_info}")

password = st.text_input("Enter your password:", type="password")

if st.button("Check Strength"):
    if password == "":
        st.warning("Please enter a password.")
    else:
        features = extract_features(password)
        prediction = model.predict(features)[0]

        score = min(int(features["entropy"][0]), 100)

        st.subheader("🔎 Result")

        if prediction == "strong":
            st.success("✅ Strong Password")
        elif prediction == "medium":
            st.warning("⚠️ Medium Strength Password")
        else:
            st.error("❌ Weak Password")

        st.progress(score)
        st.write(f"**Entropy Score:** {round(features['entropy'][0], 2)}")

        with st.expander("📊 Detailed Analysis"):
            st.dataframe(features, use_container_width=True)

        if prediction in ["weak", "medium"]:
            st.subheader("💡 Suggested Stronger Passwords")

            suggestions = generate_stronger_passwords(password)

            labels = [
                "🔧 Based on your password",
                "🔄 Restructured version",
                "🎲 Random strong password"
            ]

            for label, suggestion in zip(labels, suggestions):
                st.write(label)
                st.code(suggestion)