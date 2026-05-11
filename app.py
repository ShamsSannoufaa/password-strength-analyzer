import streamlit as st
import pandas as pd
import joblib
import math
import html
from suggest import generate_stronger_passwords


st.set_page_config(
    page_title="Password Strength Analyzer",
    page_icon="lock",
    layout="wide",
    initial_sidebar_state="expanded"
)


FEATURE_COLUMNS = [
    "length", "has_upper", "has_lower", "has_digit", "has_special",
    "count_upper", "count_lower", "count_digit", "count_special", "entropy"
]


def entropy(password: str) -> float:
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


def extract_features(password: str) -> pd.DataFrame:
    row = {
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
    }

    return pd.DataFrame([row], columns=FEATURE_COLUMNS)


@st.cache_resource
def load_model(model_choice: str):
    if model_choice == "V1":
        return joblib.load("model_rf_v1.pkl")
    return joblib.load("model_rf_v2.pkl")


if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "password_value" not in st.session_state:
    st.session_state.password_value = ""

if "model_choice" not in st.session_state:
    st.session_state.model_choice = "V2"


with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-mark">
            <svg viewBox="0 0 24 24">
                <path d="M12 3L19 6V11C19 16 15.5 19.2 12 20.5C8.5 19.2 5 16 5 11V6L12 3Z"/>
                <path d="M12 8V13"/>
                <path d="M9.7 10.5H14.3"/>
            </svg>
        </div>
        <div>
            <div class="logo-title">CYBERSECURITY</div>
            <div class="logo-subtitle">INTELLIGENCE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="side-label">THEME</div>', unsafe_allow_html=True)

    theme = st.radio(
        "Appearance",
        ["Dark", "Light"],
        horizontal=True,
        index=1,
        label_visibility="collapsed"
    )

    st.markdown('<div class="side-separator"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="menu">
        <div class="menu-item active">
            <span class="menu-icon">01</span>
            <span>Dashboard</span>
        </div>
        <div class="menu-item">
            <span class="menu-icon">02</span>
            <span>About System</span>
        </div>
        <div class="menu-item">
            <span class="menu-icon">03</span>
            <span>Model Details</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="security-tip">
        <div class="tip-title">SECURITY TIP</div>
        <div class="tip-text">
            A strong password should be long, unique, and include uppercase,
            lowercase, numbers, and special characters.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-footer">
        © 2026 Security Intelligence<br>
        All rights reserved.
    </div>
    """, unsafe_allow_html=True)


if theme == "Dark":
    C = {
        "app": "#070707",
        "app2": "#101010",
        "sidebar": "#0d0d0d",
        "card": "#151515",
        "card2": "#111111",
        "text": "#f7f4ee",
        "muted": "#b8b2a8",
        "border": "rgba(212,175,55,0.24)",
        "gold": "#d4af37",
        "gold2": "#9b7416",
        "soft": "rgba(212,175,55,0.12)",
        "input": "#1e1e1e",
        "shadow": "0 24px 70px rgba(0,0,0,0.55)",
        "table": "#f7f4ee",
    }
else:
    C = {
        "app": "#fbfaf7",
        "app2": "#ffffff",
        "sidebar": "#ffffff",
        "card": "#ffffff",
        "card2": "#fffdf8",
        "text": "#111111",
        "muted": "#5f6673",
        "border": "rgba(184,135,19,0.25)",
        "gold": "#b88713",
        "gold2": "#8a640d",
        "soft": "rgba(184,135,19,0.10)",
        "input": "#ffffff",
        "shadow": "0 18px 48px rgba(16,24,40,0.08)",
        "table": "#111111",
    }


st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background:
        radial-gradient(circle at 12% 10%, {C["soft"]}, transparent 28%),
        radial-gradient(circle at 88% 16%, rgba(184,135,19,0.08), transparent 26%),
        linear-gradient(135deg, {C["app"]} 0%, {C["app2"]} 100%);
    color: {C["text"]};
}}

#MainMenu, footer {{
    visibility: hidden;
}}

[data-testid="stHeader"] {{
    background: transparent !important;
}}

[data-testid="stToolbar"] {{
    display: none !important;
}}

button[kind="header"] {{
    position: fixed !important;
    top: 16px !important;
    left: 16px !important;
    z-index: 999999 !important;
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: {C["card"]} !important;
    border: 1px solid {C["border"]} !important;
    border-radius: 13px !important;
    width: 44px !important;
    height: 44px !important;
    box-shadow: {C["shadow"]};
}}

.block-container {{
    max-width: 1320px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}}

[data-testid="stSidebar"] {{
    background: {C["sidebar"]};
    border-right: 1px solid rgba(0,0,0,0.06);
    box-shadow: 8px 0 30px rgba(15,23,42,0.04);
}}

[data-testid="stSidebar"] * {{
    color: {C["text"]} !important;
}}

.sidebar-logo {{
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 18px 0 50px 0;
}}

.logo-mark {{
    width: 37px;
    height: 37px;
    border: 1.5px solid {C["gold"]};
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: {C["soft"]};
}}

.logo-mark svg {{
    width: 22px;
    height: 22px;
    stroke: {C["gold"]};
    fill: none;
    stroke-width: 1.8;
}}

.logo-title {{
    color: {C["gold"]} !important;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 3px;
}}

.logo-subtitle {{
    color: {C["text"]} !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
    margin-top: 3px;
}}

.side-label {{
    color: {C["muted"]} !important;
    font-size: 12px;
    letter-spacing: 2.6px;
    font-weight: 900;
    margin-bottom: 14px;
}}

.side-separator {{
    height: 1px;
    background: {C["border"]};
    margin: 24px 0 26px 0;
}}

.menu {{
    margin-top: 20px;
}}

.menu-item {{
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 18px 18px;
    margin: 5px -16px;
    font-size: 15px;
    font-weight: 650;
    border-left: 4px solid transparent;
    border-radius: 0 14px 14px 0;
}}

.menu-item.active {{
    color: {C["gold"]} !important;
    background: linear-gradient(90deg, {C["soft"]}, transparent);
    border-left: 4px solid {C["gold"]};
    font-weight: 900;
}}

.menu-icon {{
    color: {C["gold"]} !important;
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 1px;
}}

.security-tip {{
    position: fixed;
    bottom: 90px;
    left: 26px;
    width: 230px;
    background: linear-gradient(145deg, {C["card"]}, {C["card2"]});
    border: 1px solid {C["border"]};
    border-radius: 17px;
    padding: 20px;
    box-shadow: {C["shadow"]};
}}

.tip-title {{
    color: {C["gold"]} !important;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 2px;
    margin-bottom: 10px;
}}

.tip-text {{
    color: {C["text"]} !important;
    font-size: 14px;
    line-height: 1.65;
}}

.sidebar-footer {{
    position: fixed;
    bottom: 25px;
    left: 26px;
    color: {C["muted"]} !important;
    font-size: 12px;
    line-height: 1.6;
}}

div[data-testid="stRadio"] label {{
    border: 1px solid {C["border"]};
    border-radius: 12px;
    padding: 10px 18px;
    background: {C["card"]};
    min-width: 100px;
    justify-content: center;
}}

div[data-testid="stRadio"] label:has(input:checked) {{
    border-color: {C["gold"]};
    background: {C["soft"]};
}}

.hero-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 32px;
    margin-bottom: 28px;
}}

.hero-title {{
    color: {C["text"]};
    font-size: 56px;
    line-height: 1.03;
    letter-spacing: -2.5px;
    font-weight: 900;
    margin-bottom: 18px;
}}

.hero-subtitle {{
    color: {C["muted"]};
    font-size: 17px;
    line-height: 1.85;
    max-width: 790px;
}}

.status-pill {{
    border: 1px solid {C["border"]};
    background: {C["soft"]};
    color: {C["gold"]} !important;
    padding: 12px 18px;
    border-radius: 13px;
    font-size: 13px;
    font-weight: 850;
    white-space: nowrap;
}}

.gold-dot {{
    width: 11px;
    height: 11px;
    background: {C["gold"]};
    border-radius: 999px;
    display: inline-block;
    margin-right: 10px;
}}

.gold-line {{
    height: 1px;
    background: linear-gradient(90deg, transparent, {C["gold"]}, transparent);
    margin: 28px 0 30px 0;
    opacity: 0.58;
}}

[data-testid="stVerticalBlockBorderWrapper"] {{
    background: linear-gradient(145deg, {C["card"]}, {C["card2"]}) !important;
    border: 1px solid {C["border"]} !important;
    border-radius: 22px !important;
    box-shadow: {C["shadow"]};
    padding: 10px !important;
    transition: transform 0.22s ease, box-shadow 0.22s ease;
}}

[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    transform: translateY(-2px);
}}

.card-title {{
    color: {C["text"]};
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 18px;
}}

.card-text {{
    color: {C["muted"]};
    font-size: 14px;
    line-height: 1.75;
    font-weight: 500;
}}

.result-badge {{
    display: inline-block;
    padding: 10px 20px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 1.2px;
    margin-bottom: 18px;
}}

.badge-weak {{
    color: #d92d20 !important;
    background: #fff1f1;
    border: 1px solid #ffd6d6;
}}

.badge-medium {{
    color: #b77900 !important;
    background: #fff7e5;
    border: 1px solid #f2daa4;
}}

.badge-strong {{
    color: #16864a !important;
    background: #ecfdf3;
    border: 1px solid #b9ebcf;
}}

.score-red {{ color: #dc2626 !important; }}
.score-orange {{ color: #f97316 !important; }}
.score-yellow {{ color: #ca8a04 !important; }}
.score-green {{ color: #16a34a !important; }}

.score-number {{
    font-size: 37px;
    font-weight: 900;
    letter-spacing: -1px;
}}

.result-mark {{
    width: 82px;
    height: 82px;
    border-radius: 28px;
    border: 4px solid rgba(217,45,32,0.13);
    color: rgba(217,45,32,0.25) !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 52px;
    font-weight: 300;
}}

.result-mark.medium {{
    border-color: rgba(202,138,4,0.16);
    color: rgba(202,138,4,0.30) !important;
}}

.result-mark.strong {{
    border-color: rgba(22,163,74,0.16);
    color: rgba(22,163,74,0.30) !important;
}}

.metric-card {{
    background: linear-gradient(145deg, {C["card"]}, {C["card2"]});
    border: 1px solid {C["border"]};
    border-radius: 18px;
    padding: 22px;
    box-shadow: {C["shadow"]};
    display: flex;
    align-items: center;
    gap: 18px;
    min-height: 100px;
    transition: transform 0.22s ease;
}}

.metric-card:hover {{
    transform: translateY(-2px);
}}

.metric-icon {{
    min-width: 54px;
    width: 54px;
    height: 54px;
    background: {C["soft"]};
    border-radius: 999px;
    color: {C["gold"]} !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 900;
}}

.metric-number {{
    color: {C["text"]};
    font-size: 31px;
    font-weight: 900;
    line-height: 1;
}}

.metric-label {{
    color: {C["muted"]};
    font-size: 13px;
    font-weight: 650;
    margin-top: 8px;
}}

.alt-item {{
    display: flex;
    gap: 15px;
    padding: 13px 0 18px 0;
    border-bottom: 1px solid {C["border"]};
}}

.alt-item:last-child {{
    border-bottom: none;
}}

.alt-number {{
    min-width: 35px;
    width: 35px;
    height: 35px;
    background: linear-gradient(135deg, {C["gold"]}, {C["gold2"]});
    color: #ffffff !important;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
}}

.alt-label {{
    color: {C["muted"]};
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 4px;
}}

.alt-password {{
    color: {C["text"]};
    font-size: 15px;
    font-weight: 900;
    word-break: break-all;
}}

.stButton > button {{
    background: linear-gradient(135deg, {C["gold"]}, {C["gold2"]});
    color: #ffffff;
    border: none;
    border-radius: 13px;
    min-height: 51px;
    font-weight: 900;
    box-shadow: 0 14px 30px rgba(184,135,19,0.24);
}}

.stButton > button:hover {{
    background: linear-gradient(135deg, #d6a538, {C["gold"]});
    color: #ffffff;
    border: none;
}}

.stTextInput input {{
    min-height: 50px !important;
    border-radius: 13px !important;
    border: 1px solid {C["border"]} !important;
    color: {C["text"]} !important;
    background: {C["input"]} !important;
}}

.stTextInput input::placeholder {{
    color: {C["muted"]} !important;
}}

.stSelectbox div[data-baseweb="select"] > div {{
    min-height: 50px !important;
    border-radius: 13px !important;
    border: 1px solid {C["border"]} !important;
    background: {C["input"]} !important;
    color: {C["text"]} !important;
}}

.stSelectbox div[data-baseweb="select"] span {{
    color: {C["text"]} !important;
}}

.stTextInput label, .stSelectbox label {{
    color: {C["muted"]} !important;
    font-weight: 750 !important;
    font-size: 14px !important;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid {C["border"]};
    border-radius: 15px;
    overflow: hidden;
}}

[data-testid="stDataFrame"] * {{
    color: {C["table"]} !important;
}}

div[data-testid="stExpander"] {{
    background: {C["card"]};
    border: 1px solid {C["border"]};
    border-radius: 13px;
}}

div[data-testid="stExpander"] * {{
    color: {C["text"]} !important;
}}

@media (max-width: 900px) {{
    .hero-row {{
        flex-direction: column;
    }}

    .hero-title {{
        font-size: 39px;
    }}

    .security-tip,
    .sidebar-footer {{
        position: static;
        width: auto;
        margin-top: 30px;
    }}
}}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero-row">
    <div>
        <div class="hero-title">Password Strength Analyzer</div>
        <div class="hero-subtitle">
            A professional machine learning interface for evaluating password strength,
            entropy, character diversity, and estimated security risk using trained
            classification models.
        </div>
    </div>
    <div class="status-pill">
        <span class="gold-dot"></span>Machine Learning System
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)


input_col, result_col = st.columns([0.9, 1.05], gap="large")

with input_col:
    with st.container(border=True):
        st.markdown('<div class="card-title">Security Analysis</div>', unsafe_allow_html=True)

        model_choice = st.selectbox(
            "Model version",
            ["V1", "V2"],
            index=1
        )

        password = st.text_input(
            "Password input",
            placeholder="Enter a password for analysis",
            type="password"
        )

        analyze = st.button("Run Security Analysis", use_container_width=True)
        st.caption("Your password will be analyzed instantly.")


if analyze:
    if password:
        st.session_state.analysis_done = True
        st.session_state.password_value = password
        st.session_state.model_choice = model_choice
    else:
        st.warning("Please enter a password before running the analysis.")


try:
    model = load_model(st.session_state.model_choice)
except FileNotFoundError:
    st.error("Model file not found. Please check model_rf_v1.pkl and model_rf_v2.pkl files.")
    st.stop()


if st.session_state.analysis_done:
    features = extract_features(st.session_state.password_value)
    prediction = model.predict(features)[0]
    entropy_score = round(features["entropy"][0], 2)

    diversity = (
        features["has_upper"][0]
        + features["has_lower"][0]
        + features["has_digit"][0]
        + features["has_special"][0]
    )

    if prediction == "weak":
        security_score = min(int(entropy_score * 0.65), 35)
        badge_class = "badge-weak"
        score_class = "score-red"
        result_label = "WEAK PASSWORD"
        result_text = "This password is weak and may be easily guessed or cracked."
        mark_symbol = "×"
        mark_class = ""
    elif prediction == "medium":
        security_score = min(max(int(entropy_score * 0.75), 40), 74)
        badge_class = "badge-medium"
        score_class = "score-yellow"
        result_label = "MEDIUM PASSWORD"
        result_text = "This password has moderate strength but can still be improved."
        mark_symbol = "−"
        mark_class = "medium"
    else:
        security_score = min(max(int(entropy_score), 75), 100)
        badge_class = "badge-strong"
        score_class = "score-green"
        result_label = "STRONG PASSWORD"
        result_text = "This password has strong security characteristics."
        mark_symbol = "✓"
        mark_class = "strong"
else:
    features = None
    entropy_score = 0
    security_score = 0
    diversity = 0
    badge_class = "badge-weak"
    score_class = "score-red"
    result_label = "WAITING FOR ANALYSIS"
    result_text = "Enter a password and run the analysis to see the result."
    mark_symbol = "×"
    mark_class = ""


if security_score < 25:
    progress_color = "#dc2626"
elif security_score < 50:
    progress_color = "#f97316"
elif security_score < 75:
    progress_color = "#eab308"
else:
    progress_color = "#16a34a"


st.markdown(f"""
<style>
.stProgress > div > div > div > div {{
    background: {progress_color} !important;
}}
</style>
""", unsafe_allow_html=True)


with result_col:
    with st.container(border=True):
        top_a, top_b = st.columns([1, 0.22])

        with top_a:
            st.markdown('<div class="card-title">Analysis Result</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="result-badge {badge_class}">{result_label}</div>',
                unsafe_allow_html=True
            )
            st.markdown(f'<div class="card-text">{result_text}</div>', unsafe_allow_html=True)

        with top_b:
            st.markdown(
                f'<div class="result-mark {mark_class}">{mark_symbol}</div>',
                unsafe_allow_html=True
            )

        st.progress(security_score / 100)

        score_left, score_right = st.columns(2)

        with score_left:
            st.markdown(f"""
            <div style="margin-top:16px;">
                <div class="card-text">Security Score</div>
                <div class="score-number {score_class}">{security_score}%</div>
            </div>
            """, unsafe_allow_html=True)

        with score_right:
            st.markdown(f"""
            <div style="margin-top:16px;text-align:right;">
                <div class="card-text">Entropy Score</div>
                <div class="score-number" style="font-size:30px;color:{C["text"]};">
                    {entropy_score} bits
                </div>
            </div>
            """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


if features is not None:
    length_value = features["length"][0]
    category_count = diversity
else:
    length_value = 0
    category_count = 0


m1, m2, m3, m4 = st.columns(4)

metric_data = [
    ("LEN", length_value, "Password Length"),
    ("DIV", f"{diversity}/4", "Character Diversity"),
    ("CAT", category_count, "Character Categories"),
    ("SEC", f"{security_score}%", "Security Score"),
]

for col, (icon, number, label) in zip([m1, m2, m3, m4], metric_data):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div>
                <div class="metric-number">{number}</div>
                <div class="metric-label">{label}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


bottom_left, bottom_right = st.columns([1.15, 0.85], gap="large")

if features is not None:
    analysis_df = pd.DataFrame({
        "Feature": ["Uppercase Letters", "Lowercase Letters", "Numbers", "Special Characters"],
        "Status": [
            "Available" if features["has_upper"][0] else "Missing",
            "Available" if features["has_lower"][0] else "Missing",
            "Available" if features["has_digit"][0] else "Missing",
            "Available" if features["has_special"][0] else "Missing",
        ],
        "Count": [
            features["count_upper"][0],
            features["count_lower"][0],
            features["count_digit"][0],
            features["count_special"][0],
        ],
        "Details": [
            "Good" if features["has_upper"][0] else "Include at least one uppercase letter",
            "Good" if features["has_lower"][0] else "Include lowercase letters",
            "Good" if features["has_digit"][0] else "Include at least one number",
            "Good" if features["has_special"][0] else "Add special characters for stronger security",
        ]
    })
else:
    analysis_df = pd.DataFrame({
        "Feature": ["Uppercase Letters", "Lowercase Letters", "Numbers", "Special Characters"],
        "Status": ["Waiting", "Waiting", "Waiting", "Waiting"],
        "Count": [0, 0, 0, 0],
        "Details": [
            "Run analysis to display result",
            "Run analysis to display result",
            "Run analysis to display result",
            "Run analysis to display result",
        ]
    })


with bottom_left:
    with st.container(border=True):
        st.markdown('<div class="card-title">Security Feature Breakdown</div>', unsafe_allow_html=True)
        st.dataframe(analysis_df, use_container_width=True, hide_index=True)

        with st.expander("Raw Model Input Features"):
            if features is not None:
                st.dataframe(features, use_container_width=True)
            else:
                st.write("Run analysis to display raw model features.")


with bottom_right:
    with st.container(border=True):
        st.markdown('<div class="card-title">Recommended Stronger Alternatives</div>', unsafe_allow_html=True)

        if features is not None:
            suggestions = generate_stronger_passwords(st.session_state.password_value)
        else:
            suggestions = [
                "ExamplePass#2026",
                "Secure_Pass!84",
                "K9m!aZpQ3xLr#7tV"
            ]

        labels = [
            "Personalized variation",
            "Restructured secure version",
            "Randomized strong alternative"
        ]

        for i, (label, suggestion) in enumerate(zip(labels, suggestions), start=1):
            safe_suggestion = html.escape(str(suggestion))

            st.markdown(f"""
            <div class="alt-item">
                <div class="alt-number">{i}</div>
                <div>
                    <div class="alt-label">{label}</div>
                    <div class="alt-password">{safe_suggestion}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)