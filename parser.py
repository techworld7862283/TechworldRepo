import pandas as pd
import joblib
from core.preprocessing import clean_text
from core.extraction import (
    extract_name, extract_email,
    extract_phone, extract_skills,
    extract_sections
)

# Load model ONCE
classifier = joblib.load("ml/resume_classifier.pkl")

def predict_category(text: str) -> str:
    return classifier.predict([text])[0]

def load_resumes(csv_path):
    df = pd.read_csv(csv_path)

    for col in df.columns:
        if "resume" in col.lower():
            return df[col].astype(str)

    raise ValueError("Resume column not found")

def parse_all_resumes(csv_path, limit=None):
    texts = load_resumes(csv_path)
    results = []

    for idx, text in texts.items():
        text = clean_text(text)

        results.append({
            "resume_id": idx,
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "skills": extract_skills(text),
            "sections": extract_sections(text),
            "category": predict_category(text)          
            })

        if limit and len(results) >= limit:
            break

    return results
def parse_resume_text(text: str) -> dict:
    text = clean_text(text)

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "category": predict_category(text),
        "sections": extract_sections(text)
    }




