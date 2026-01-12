import streamlit as st
import pandas as pd
import joblib
import tempfile
import os
from collections import Counter
import plotly.express as px

from utils.parser import parse_resume_text
from utils.file_parser import extract_text_from_pdf, extract_text_from_docx

st.set_page_config(page_title="Resume Parser AI", layout="wide")

# ======================
# LOAD MODEL
# ======================
classifier = joblib.load("ml/resume_classifier.pkl")

# ======================
# SIMPLE AUTH (MVP)
# ======================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.sidebar.title("🔐 Login")

if not st.session_state.logged_in:
    user = st.sidebar.text_input("Username")
    pwd = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if user == "admin" and pwd == "admin123":
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid credentials")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.experimental_rerun()

# ======================
# UPLOAD RESUME
# ======================
st.sidebar.header("📤 Upload Resume")

uploaded = st.sidebar.file_uploader("PDF / DOCX", ["pdf", "docx"])

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded.name) as tmp:
        tmp.write(uploaded.read())
        path = tmp.name

    if uploaded.name.endswith(".pdf"):
        text = extract_text_from_pdf(path)
    else:
        text = extract_text_from_docx(path)

    parsed = parse_resume_text(text)

    probs = classifier.predict_proba([text])[0]
    idx = probs.argmax()

    parsed["category"] = classifier.classes_[idx]
    parsed["confidence"] = round(probs[idx] * 100, 2)

    st.sidebar.success("Parsed Successfully")
    st.sidebar.json(parsed)

    os.remove(path)

# ======================
# LOAD DATASET
# ======================
st.title("📄 Resume Parser AI Dashboard")

df = pd.read_csv("data/UpdatedResumeDataSet.csv").head(50)

resumes = []
for i, row in df.iterrows():
    parsed = parse_resume_text(row["Resume"])
    probs = classifier.predict_proba([row["Resume"]])[0]
    idx = probs.argmax()
    parsed["category"] = classifier.classes_[idx]
    parsed["confidence"] = round(probs[idx] * 100, 2)
    resumes.append(parsed)

# ======================
# FILTERS
# ======================
skills = sorted({s for r in resumes for s in r["skills"]})
categories = sorted({r["category"] for r in resumes})

selected_skill = st.sidebar.selectbox("Skill", ["All"] + skills)
selected_cat = st.sidebar.selectbox("Category", ["All"] + categories)

filtered = resumes

if selected_skill != "All":
    filtered = [r for r in filtered if selected_skill in r["skills"]]

if selected_cat != "All":
    filtered = [r for r in filtered if r["category"] == selected_cat]

if not filtered:
    st.warning("No resumes match filters")
    st.stop()

# ======================
# TABS
# ======================
tab1, tab2, tab3 = st.tabs(["📄 Resumes", "📊 Analytics", "🏆 Top Candidates"])

with tab1:
    for r in filtered[:20]:
        with st.expander(f"{r['name']} — {r['category']}"):
            st.write("📧", r["email"])
            st.write("📞", r["phone"])
            st.write("🧠 Skills:", ", ".join(r["skills"]))
            st.write("🎯 Confidence:", r["confidence"], "%")

with tab2:
    skill_counts = Counter(s for r in resumes for s in r["skills"])
    st.plotly_chart(px.bar(
        pd.DataFrame(skill_counts.items(), columns=["Skill", "Count"]),
        x="Skill", y="Count"
    ), use_container_width=True)

with tab3:
    top_n = st.slider("Top N", 1, 10, 5)
    for cat in categories:
        top = sorted(
            [r for r in resumes if r["category"] == cat],
            key=lambda x: x["confidence"],
            reverse=True
        )[:top_n]

        with st.expander(cat):
            for r in top:
                st.write(f"**{r['name']}** — {r['confidence']}%")

