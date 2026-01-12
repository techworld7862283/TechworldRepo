import re

def parse_resume_text(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "resume_text": text
    }

def extract_email(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r"\+?\d[\d\s\-]{8,}", text)
    return match.group(0) if match else None

def extract_name(text):
    return text.split("\n")[0][:40]

def extract_skills(text):
    SKILLS = ["python", "java", "sql", "aws", "docker", "ml", "ai"]
    return [s for s in SKILLS if s.lower() in text.lower()]






