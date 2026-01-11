---

# 📄 Resume Parser AI — SaaS-Ready Resume Intelligence Platform

A **full-stack AI-powered Resume Parsing and Classification platform** built with **FastAPI, Streamlit, and Machine Learning**, designed to extract, analyze, and classify resumes at scale.

This project demonstrates **end-to-end AI product development**, from data ingestion and ML inference to secure APIs, interactive dashboards, and SaaS-ready authentication.

---

## 🚀 Features

### 🔍 Resume Parsing

* Extracts structured information from resumes:

  * Name
  * Email
  * Phone
  * Skills
  * Raw resume text

### 🧠 Machine Learning Classification

* Predicts **resume category** (e.g., Data Science, HR, DevOps)
* Provides **confidence score (%)** for each prediction
* Supports both **single resume** and **bulk dataset** classification

### 📤 Resume Upload

* Upload resumes in:

  * **PDF**
  * **DOCX**
* Real-time parsing and classification

### 📊 Interactive Analytics Dashboard

* Skill distribution charts
* Category distribution
* Contact information coverage
* Top candidates per category (confidence-based ranking)

### 🔎 Advanced Filtering

* Filter by:

  * Skills (multi-select)
  * Category
  * Missing email / phone
  * Name search

### ⬇️ Export & Download

* Download filtered results as:

  * CSV
  * JSON

### 🔐 Authentication (SaaS-Ready)

* Token-based authentication (JWT)
* Protected API routes
* Login / Logout flow
* Session handling & expiry detection

---

## 🏗️ Architecture

```
resume-parser-ai/
│
├── api/
│   ├── main.py              # FastAPI application
│   ├── parser.py            # Resume parsing logic
│   ├── file_parser.py       # PDF / DOCX text extraction
│
├── ml/
│   ├── resume_classifier.pkl # Trained ML model
│
├── ui/
│   └── app.py               # Streamlit dashboard
│
├── data/
│   └── UpdatedResumeDataSet.csv
│
├── requirements.txt
├── README.md
```

---

## 🛠️ Tech Stack

### Backend

* **FastAPI** – High-performance REST API
* **Uvicorn** – ASGI server
* **JWT Authentication**

### Frontend

* **Streamlit** – Interactive web UI
* **Plotly** – Interactive analytics & charts

### Machine Learning

* **Scikit-learn**
* **TF-IDF / Text Vectorization**
* **Multi-class classification**
* Confidence scoring using `predict_proba`

### File Processing

* **PyPDF2 / pdfplumber**
* **python-docx**

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/resume-parser-ai.git
cd resume-parser-ai
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Start FastAPI Backend

```bash
uvicorn api.main:app --reload
```

API will run at:

```
http://127.0.0.1:8000
```

### Start Streamlit Frontend

```bash
streamlit run ui/app.py
```

Dashboard will open at:

```
http://localhost:8501
```

---

## 🔐 Authentication Flow

1. User logs in via Streamlit UI
2. Credentials sent to `/token`
3. JWT token returned
4. Token attached to all protected API requests
5. Session expiry handled gracefully

---

## 📡 API Endpoints

| Method | Endpoint         | Description                      |
| ------ | ---------------- | -------------------------------- |
| POST   | `/token`         | Authenticate user                |
| GET    | `/parse`         | Parse & classify dataset resumes |
| POST   | `/upload_resume` | Upload & classify single resume  |

---

## 📊 Sample Output

```json
{
  "name": "John Doe",
  "email": "john@email.com",
  "phone": "+123456789",
  "skills": ["Python", "ML", "FastAPI"],
  "category": "Data Science",
  "confidence": 92.45
}
```

---

## 🧪 Project Level & Skill Impact

* **Skill Level:** Beginner → Intermediate / Early Mid-Level
* **Concepts Covered:**

  * Full-stack AI systems
  * REST APIs
  * Authentication
  * ML inference in production
  * Interactive analytics
  * SaaS architecture fundamentals

💡 This project strongly boosts:

* Backend engineering confidence
* ML deployment skills
* SaaS product thinking
* Portfolio credibility

---

## 🚀 Future Enhancements (Roadmap)

* Multi-tenant user accounts
* Role-based access (Admin / Recruiter)
* Resume scoring & ranking engine
* Stripe subscription billing
* Docker & CI/CD
* Cloud deployment (AWS / GCP / Azure)

---

## 📄 License

MIT License — Free to use, modify, and distribute.

---

## 🤝 Author

**Muhammad Azhar**

AI Engineer | AI & Full-Stack Developer
