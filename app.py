import streamlit as st
import requests
import pandas as pd
import json
from collections import Counter
import plotly.express as px
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Resume Parser AI", layout="wide")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# =========================
# SESSION STATE INIT
# =========================
if "token" not in st.session_state:
    st.session_state["token"] = None

if "resumes" not in st.session_state:
    st.session_state["resumes"] = []

# =========================
# AUTHENTICATION
# =========================
st.sidebar.title("🔐 Authentication")

if st.session_state["token"] is None:
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        res = requests.post(
            f"{API_URL}/token",
            data={"username": email, "password": password}
        )
        if res.status_code == 200:
            st.session_state["token"] = res.json()["access_token"]
            st.sidebar.success("Logged in successfully")
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid credentials")
else:
    st.sidebar.success("Logged in")
    if st.sidebar.button("Logout"):
        st.session_state["token"] = None
        st.experimental_rerun()

# Stop app if not logged in
if not st.session_state["token"]:
    st.warning("Please log in to continue")
    st.stop()

headers = {
    "Authorization": f"Bearer {st.session_state['token']}"
}

# =========================
# UPLOAD SINGLE RESUME
# =========================
st.sidebar.header("📤 Upload Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF or DOCX",
    type=["pdf", "docx"]
)

if uploaded_file:
    with st.spinner("Parsing resume..."):
        res = requests.post(
            f"{API_URL}/upload_resume",
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            },
            headers=headers
        )

        if res.status_code == 200:
            result = res.json()
            st.sidebar.success("Parsed Successfully")
            st.sidebar.markdown(
                f"**Category:** `{result['category']}`  \n"
                f"**Confidence:** `{result['confidence']}%`"
            )
            st.sidebar.json(result)
        elif res.status_code == 401:
            st.sidebar.error("Session expired. Please login again.")
            st.session_state["token"] = None
            st.experimental_rerun()
        else:
            st.sidebar.error("Failed to parse resume")

# =========================
# LOAD BULK RESUMES
# =========================
st.title("📄 Resume Parser AI Dashboard")

limit = st.slider("Number of resumes", 1, 50, 10)

if st.button("🔍 Parse Dataset"):
    with st.spinner("Loading resumes..."):
        res = requests.get(
            f"{API_URL}/parse",
            params={"limit": limit},
            headers=headers
        )

        if res.status_code == 401:
            st.error("Session expired. Please login again.")
            st.session_state["token"] = None
            st.experimental_rerun()

        try:
            data = res.json()
        except Exception:
            st.error("Failed to parse API response")
            st.stop()

        if res.status_code == 200 and isinstance(data, list):
            st.session_state["resumes"] = data
        else:
            st.error("API returned invalid data")

if not st.session_state["resumes"]:
    st.info("Load resumes to continue")
    st.stop()

resumes = st.session_state["resumes"]
filtered = resumes.copy()

# =========================
# GLOBAL DATA
# =========================
all_skills = []
categories = []

for r in resumes:
    all_skills.extend(r.get("skills", []))
    if r.get("category"):
        categories.append(r["category"])

# =========================
# FILTERS
# =========================
st.sidebar.header("🔎 Filters")

selected_skills = st.sidebar.multiselect(
    "Skills", sorted(set(all_skills))
)
selected_category = st.sidebar.selectbox(
    "Category", ["All"] + sorted(set(categories))
)
missing_email = st.sidebar.checkbox("Missing Email")
missing_phone = st.sidebar.checkbox("Missing Phone")
search_name = st.sidebar.text_input("Search Name")

if selected_skills:
    filtered = [
        r for r in filtered
        if all(s in r.get("skills", []) for s in selected_skills)
    ]

if selected_category != "All":
    filtered = [
        r for r in filtered
        if r.get("category") == selected_category
    ]

if missing_email:
    filtered = [r for r in filtered if not r.get("email")]

if missing_phone:
    filtered = [r for r in filtered if not r.get("phone")]

if search_name:
    filtered = [
        r for r in filtered
        if r.get("name") and search_name.lower() in r["name"].lower()
    ]

if not filtered:
    st.warning("No resumes match the selected filters")
    st.stop()

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(
    ["📄 Resumes", "📊 Analytics", "🏆 Top Candidates"]
)

# ---- TAB 1: RESUMES ----
with tab1:
    st.subheader(f"Showing {len(filtered)} resumes")

    for r in filtered[:20]:
        with st.expander(
            f"{r.get('name','Unknown')} — {r.get('category','')}"
        ):
            st.write("📧", r.get("email", "N/A"))
            st.write("📞", r.get("phone", "N/A"))
            st.write("🧠 Skills:", ", ".join(r.get("skills", [])))

# ---- TAB 2: ANALYTICS ----
with tab2:
    skill_df = pd.DataFrame(
        Counter(all_skills).items(),
        columns=["Skill", "Count"]
    )
    st.plotly_chart(
        px.bar(skill_df, x="Skill", y="Count"),
        use_container_width=True
    )

    cat_df = pd.DataFrame(
        Counter(categories).items(),
        columns=["Category", "Count"]
    )
    st.plotly_chart(
        px.bar(cat_df, x="Category", y="Count"),
        use_container_width=True
    )

# ---- TAB 3: TOP CANDIDATES ----
with tab3:
    top_n = st.slider("Top N", 1, 10, 5)

    for cat in sorted(set(categories)):
        top = sorted(
            [r for r in filtered if r.get("category") == cat],
            key=lambda x: x.get("confidence", 0),
            reverse=True
        )[:top_n]

        with st.expander(cat):
            for r in top:
                st.markdown(
                    f"**{r.get('name','Unknown')}** — "
                    f"{r.get('confidence',0)}%"
                )
