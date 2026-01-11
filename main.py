from fastapi import FastAPI, UploadFile, File
import joblib
import tempfile
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from api.parser import parse_all_resumes, parse_resume_text
from api.file_parser import extract_text_from_pdf, extract_text_from_docx
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from api.auth import authenticate_user, create_access_token, SECRET_KEY, ALGORITHM

app = FastAPI(title="Resume Parser API")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401)
        return email
    except JWTError:
        raise HTTPException(status_code=401)

# ------------------------
# App & Config
# ------------------------
CSV_PATH = "data/UpdatedResumeDataSet.csv"
MODEL_PATH = "ml/resume_classifier.pkl"

classifier = joblib.load(MODEL_PATH)

# ------------------------
# Parse CSV Resumes
# ------------------------
@app.get("/parse")
def parse_resumes(limit: int = 10, user: str = Depends(get_current_user)):
    return parse_all_resumes(CSV_PATH, limit)

@app.get("/parse")
def parse_resumes(limit: int = 10):
    results = parse_all_resumes(CSV_PATH, limit)

    for r in results:
        text = r.get("resume_text", "")

        if text:
            probs = classifier.predict_proba([text])[0]
            idx = probs.argmax()

            r["category"] = classifier.classes_[idx]
            r["confidence"] = round(probs[idx] * 100, 2)
        else:
            r["category"] = "Unknown"
            r["confidence"] = 0.0

    return results

# ------------------------
# Upload Resume (PDF/DOCX)
# ------------------------
@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    suffix = file.filename.split(".")[-1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        if suffix == "pdf":
            text = extract_text_from_pdf(tmp_path)
        elif suffix in ["docx", "doc"]:
            text = extract_text_from_docx(tmp_path)
        else:
            return {"error": "Unsupported file format"}

        parsed = parse_resume_text(text)

        if text:
            probs = classifier.predict_proba([text])[0]
            idx = probs.argmax()

            parsed["category"] = classifier.classes_[idx]
            parsed["confidence"] = round(probs[idx] * 100, 2)
        else:
            parsed["category"] = "Unknown"
            parsed["confidence"] = 0.0

        return parsed

    finally:
        os.remove(tmp_path)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login():
    return {"access_token": "demo-token", "token_type": "bearer"}
@app.get("/parse")
def parse_resumes(limit: int = 10, token: str = Depends(oauth2_scheme)):
    if limit > 10:
        raise HTTPException(403, "Upgrade your plan")
