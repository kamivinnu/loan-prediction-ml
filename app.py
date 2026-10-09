import streamlit as st
import numpy as np
import pandas as pd
import pickle

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Loan Approval AI",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --navy:   #0f1b2d;
    --navy2:  #1a2c45;
    --gold:   #c9a84c;
    --gold2:  #e8c96a;
    --cream:  #f5f0e8;
    --text:   #e8e2d8;
    --muted:  #8a9bb0;
    --green:  #2ecc8a;
    --red:    #e05c5c;
    --radius: 14px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--navy) !important;
    color: var(--text) !important;
}

.main .block-container {
    max-width: 720px;
    padding: 2rem 2rem 4rem;
    background: transparent;
}

.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-icon {
    font-size: 3.5rem;
    display: block;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 20px rgba(201,168,76,0.4));
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    font-weight: 400;
    color: var(--gold);
    margin: 0 0 0.3rem;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.hero p {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    margin: 0;
}
.hero-divider {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 1.5rem auto 2rem;
}

.section-card {
    background: var(--navy2);
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: var(--radius);
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
}
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(201,168,76,0.2);
}

div[data-testid="stSelectbox"] > label,
div[data-testid="stNumberInput"] > label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    letter-spacing: 0.02em !important;
    margin-bottom: 4px !important;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(201,168,76,0.2) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s ease !important;
}

div[data-testid="stSelectbox"] > div > div:hover,
div[data-testid="stNumberInput"] > div > div > input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.12) !important;
}

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--gold), var(--gold2)) !important;
    color: var(--navy) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.85rem 0 !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.3) !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(201,168,76,0.4) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

.result-approved {
    background: linear-gradient(135deg, rgba(46,204,138,0.12), rgba(46,204,138,0.06));
    border: 1px solid rgba(46,204,138,0.4);
    border-radius: var(--radius);
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
    animation: fadeInUp 0.4s ease;
}
.result-rejected {
    background: linear-gradient(135deg, rgba(224,92,92,0.12), rgba(224,92,92,0.06));
    border: 1px solid rgba(224,92,92,0.4);
    border-radius: var(--radius);
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
    animation: fadeInUp 0.4s ease;
}
.result-icon { font-size: 3rem; display: block; margin-bottom: 0.5rem; }
.result-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    font-weight: 400;
    margin: 0 0 0.4rem;
}
.result-approved .result-title { color: var(--green); }
.result-rejected .result-title { color: var(--red); }
.result-sub { color: var(--muted); font-size: 0.9rem; }

.metrics-row {
    display: flex;
    gap: 0.8rem;
    margin: 1rem 0;
}
.metric-pill {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(201,168,76,0.12);
    border-radius: 10px;
    padding: 0.8rem;
    text-align: center;
}
.metric-pill .val {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: var(--gold);
}
.metric-pill .lbl {
    font-size: 0.68rem;
    color: var(--muted);
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.footer {
    text-align: center;
    color: rgba(138,155,176,0.5);
    font-size: 0.75rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Load Models ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model  = pickle.load(open("loan_model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl",     "rb"))
    return model, scaler

try:
    model, scaler = load_model()
    model_loaded = True
except Exception:
    model_loaded = False

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="hero-icon">🏦</span>
    <h1>Loan Approval AI</h1>
    <p>Instant eligibility prediction powered by machine learning</p>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Section 1: Personal Info ───────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">👤 Applicant Profile</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    gender        = st.selectbox("Gender",         ["Male", "Female"])
    married       = st.selectbox("Marital Status", ["Yes", "No"])
    dependents    = st.selectbox("Dependents",     ["0", "1", "2", "3+"])
with col2:
    education     = st.selectbox("Education",      ["Graduate", "Not Graduate"])
    self_emp      = st.selectbox("Self Employed",  ["No", "Yes"])
    property_area = st.selectbox("Property Area",  ["Urban", "Semiurban", "Rural"])

st.markdown('</div>', unsafe_allow_html=True)

# ── Section 2: Financial Info ──────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">💰 Financial Details</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    applicant_income   = st.number_input("Applicant Income (₹)",    min_value=0, value=5000,   step=500)
    coapplicant_income = st.number_input("Co-applicant Income (₹)", min_value=0, value=0,      step=500)
with col4:
    # User enters actual rupee amount (e.g. 1,20,000)
    # Model was trained with LoanAmount in thousands — we convert internally
    loan_amount_rupees = st.number_input("Loan Amount (₹)",         min_value=0, value=120000, step=5000)
    loan_term          = st.number_input("Loan Term (months)",      min_value=0, value=360,    step=12)

credit_history = st.selectbox(
    "Credit History",
    [1, 0],
    format_func=lambda x: "✅ Good (meets guidelines)" if x == 1 else "❌ Poor (does not meet guidelines)"
)

st.markdown('</div>', unsafe_allow_html=True)

# ── Compute derived values for live display ───────────────────────────────────
total_income     = applicant_income + coapplicant_income
loan_amount_k    = loan_amount_rupees / 1000  # convert to thousands for model

# ── Income Validation Warning (shown before button press too) ─────────────────
income_valid = total_income > 0
loan_valid   = loan_amount_rupees > 0

if not income_valid:
    st.error("⚠️ Both incomes are ₹0. Please enter at least one income (Applicant or Co-applicant) to proceed.")

# ── Live Summary Metrics ───────────────────────────────────────────────────────
if income_valid and loan_valid:
    ratio = round(loan_amount_k / total_income, 4)
else:
    ratio = "N/A"

st.markdown(f"""
<div class="metrics-row">
    <div class="metric-pill">
        <div class="val">₹{total_income:,}</div>
        <div class="lbl">Combined Income</div>
    </div>
    <div class="metric-pill">
        <div class="val">{ratio}</div>
        <div class="lbl">Loan/Income Ratio</div>
    </div>
    <div class="metric-pill">
        <div class="val">{loan_term // 12}y {loan_term % 12}m</div>
        <div class="lbl">Loan Duration</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Predict Button ─────────────────────────────────────────────────────────────
predict_btn = st.button("⚡  Check Eligibility")

if predict_btn:
    # ── Hard validation gate ──────────────────────────────────────────────────
    if total_income <= 0:
        st.error("❌ Both Applicant Income and Co-applicant Income are ₹0. Please enter at least one valid income.")
        st.stop()

    if loan_amount_rupees <= 0:
        st.error("❌ Loan Amount must be greater than ₹0.")
        st.stop()

    if not model_loaded:
        st.error("⚠️ Model files not found. Place `loan_model.pkl` and `scaler.pkl` in the same directory.")
        st.stop()

    # ── Soft warning ─────────────────────────────────────────────────────────
    if loan_amount_rupees > total_income * 10:
        st.warning("⚠️ Loan amount is very high relative to your income. Approval is unlikely.")

    try:
        # ── Encode categoricals ───────────────────────────────────────────────
        gender_enc   = 1 if gender    == "Male"         else 0
        married_enc  = 1 if married   == "Yes"          else 0
        edu_enc      = 1 if education == "Graduate"     else 0
        self_emp_enc = 1 if self_emp  == "Yes"          else 0
        dep_enc      = 3 if dependents == "3+" else int(dependents)
        prop_enc     = {"Rural": 0, "Semiurban": 1, "Urban": 2}[property_area]

        # ── Feature engineering — must match training ─────────────────────────
        # LoanAmount in model = thousands (as trained), ratio = LoanAmount_k / total_income
        loan_inc_ratio = loan_amount_k / total_income

        input_df = pd.DataFrame([[
            gender_enc, married_enc, dep_enc, edu_enc, self_emp_enc,
            applicant_income, coapplicant_income, loan_amount_k,
            loan_term, credit_history, prop_enc,
            total_income, loan_inc_ratio
        ]], columns=[
            'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
            'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
            'Loan_Amount_Term', 'Credit_History', 'Property_Area',
            'Total_Income', 'Loan_Income_Ratio'
        ])

        input_scaled = scaler.transform(input_df)
        prediction   = model.predict(input_scaled)[0]
        proba        = model.predict_proba(input_scaled)[0]
        confidence   = round(proba[prediction] * 100, 1)

        if prediction == 1:
            st.markdown(f"""
            <div class="result-approved">
                <span class="result-icon">✅</span>
                <div class="result-title">Loan Approved</div>
                <div class="result-sub">Confidence: <strong style="color:#2ecc8a">{confidence}%</strong> · Based on your financial profile</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-rejected">
                <span class="result-icon">❌</span>
                <div class="result-title">Loan Rejected</div>
                <div class="result-sub">Confidence: <strong style="color:#e05c5c">{confidence}%</strong> · Consider improving credit history or reducing loan amount</div>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Prediction error: {e}")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Loan Approval AI &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp; For portfolio demonstration only
</div>
""", unsafe_allow_html=True)