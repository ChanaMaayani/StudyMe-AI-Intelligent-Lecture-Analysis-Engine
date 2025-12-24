import os
import json
import time
import ssl
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai

# --- 1. הגדרות נטפרי (חובה!) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
cert_path = os.path.join(current_dir, "netfree-ca.crt")

# טעינת תעודה אם קיימת
if os.path.exists(cert_path):
    print(f"Loading NetFree certificate from: {cert_path}")
    os.environ['SSL_CERT_FILE'] = cert_path
    os.environ['REQUESTS_CA_BUNDLE'] = cert_path
    os.environ['GRPC_DEFAULT_SSL_ROOTS_FILE_PATH'] = cert_path

# ביטול אימות SSL מחמיר (פותר בעיות באתרוג/נטפרי)
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['CURL_CA_BUNDLE'] = ""
os.environ['PYTHONHTTPSVERIFY'] = "0"
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384'

# --- 2. אתחול והגדרת ג'מיני ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key, transport='rest')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "message": "StudyMe API is running"}

@app.post("/analyze")
async def analyze_media(file: UploadFile = File(...)):
    filename = file.filename
    temp_file_path = f"temp_{filename}"
    google_file = None

    try:
        # א. שמירה לוקאלית
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        print(f"Uploading {filename} to Gemini...")
        google_file = genai.upload_file(path=temp_file_path)

        while google_file.state.name == "PROCESSING":
            print("Processing media...")
            time.sleep(2)
            google_file = genai.get_file(google_file.name)

        if google_file.state.name == "FAILED":
             raise HTTPException(status_code=500, detail="Google failed to process the file.")

        # ד. הפרומפט המלא (סיכום, משימות, מבחן)
        prompt = """
        Analyze the attached audio/video file (a lecture).
        Output ONLY a valid JSON object. Do not add markdown formatting like ```json.
        Structure:
        {
          "summary": "סיכום מקיף של השיעור בעברית",
          "key_points": ["נקודה 1", "נקודה 2", "נקודה 3"],
          "tasks": ["משימה 1 (אם הוזכרה)", "משימה 2"],
          "quiz": [
            {
              "question": "שאלה 1 על החומר?",
              "options": ["תשובה א", "תשובה ב", "תשובה ג", "תשובה ד"],
              "answer": "התשובה הנכונה"
            },
             {
              "question": "שאלה 2 על החומר?",
              "options": ["תשובה א", "תשובה ב", "תשובה ג", "תשובה ד"],
              "answer": "התשובה הנכונה"
            },
             {
              "question": "שאלה 3 על החומר?",
              "options": ["תשובה א", "תשובה ב", "תשובה ג", "תשובה ד"],
              "answer": "התשובה הנכונה"
            }
          ]
        }
        Use Hebrew for all values.
        """

        # Try different model names until one works
        model_names = ['gemini-flash-latest', 'gemini-pro', 'models/gemini-pro', 'gemini-1.5-flash']
        
        for model_name in model_names:
            try:
                print(f"Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content([google_file, prompt])
                break
            except Exception as model_error:
                print(f"Model {model_name} failed: {model_error}")
                if model_name == model_names[-1]:  # Last model
                    raise model_error
                continue
        
        raw_text = response.text
        # מנקים סימני Markdown אם המודל הוסיף אותם בטעות
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "").replace("```", "")
        elif raw_text.startswith("```"):
             raw_text = raw_text.replace("```", "")
        
        result = json.loads(raw_text.strip())
        return result

    except Exception as e:
        print(f"Error details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # ז. ניקוי קבצים (חשוב מאוד!)
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass
        
        if google_file:
            try:
                genai.delete_file(google_file.name)
                print("Deleted remote file from Google.")
            except Exception as e:
                print(f"Could not delete remote file: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)