import os
import json
import time
import ssl
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai

# # --- הגדרות נטפרי ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# cert_path = os.path.join(current_dir, "netfree-ca.crt")

# if os.path.exists(cert_path):
#     print(f"Loading NetFree certificate from: {cert_path}")
#     os.environ['GRPC_DEFAULT_SSL_ROOTS_FILE_PATH'] = cert_path
#     os.environ['SSL_CERT_FILE'] = cert_path
#     os.environ['REQUESTS_CA_BUNDLE'] = cert_path

# # ביטול אימות SSL (פתרון לנטפרי)
# ssl._create_default_https_context = ssl._create_unverified_context
# os.environ['CURL_CA_BUNDLE'] = ""
# os.environ['PYTHONHTTPSVERIFY'] = "0"
# os.environ['GRPC_SSL_CIPHER_SUITES'] = 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384'

# # --- אתחול ---
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# if not api_key:
#     print("❌ שים לב: מפתח ה-API לא נמצא בקובץ .env")

# genai.configure(api_key=api_key)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/analyze")
# async def analyze_audio(file: UploadFile = File(...)):
#     temp_file_path = f"temp_{file.filename}"
#     audio_file = None # משתנה לאחסון האובייקט של גוגל

#     try:
#         # 1. שמירה לוקאלית
#         with open(temp_file_path, "wb") as buffer:
#             buffer.write(await file.read())

#         # 2. העלאה לגוגל
#         print(f"Uploading {file.filename} to Gemini...")
#         audio_file = genai.upload_file(path=temp_file_path)

#         # 3. המתנה לעיבוד
#         while audio_file.state.name == "PROCESSING":
#             time.sleep(2)
#             audio_file = genai.get_file(audio_file.name)

#         if audio_file.state.name == "FAILED":
#              raise HTTPException(status_code=500, detail="Google failed to process the audio file.")

#         # 4. הפרומפט המנצח (בדיוק כמו שביקשת)
#         prompt = """
#         Analyze this audio recording for a student. 
#         Return ONLY a JSON object with the following structure:
#         {
#           "summary": "A concise summary of the lecture",
#           "key_points": ["Point 1", "Point 2"],
#           "quiz": [
#             {"question": "Question 1?", "options": ["A", "B", "C", "D"], "answer": "Correct Option"},
#             {"question": "Question 2?", "options": ["A", "B", "C", "D"], "answer": "Correct Option"}
#           ],
#           "tasks": ["Task 1 based on lecture", "Task 2"]
#         }
#         Make sure the JSON is valid and the summary is helpful.
#         """

#         # 5. שימוש במודל המקורי שלך
#         model = genai.GenerativeModel('gemini-flash-latest')
#         response = model.generate_content([audio_file, prompt])
        
#         # ניקוי ה-JSON (השיטה הידנית שעבדה לך)
#         raw_text = response.text.replace('```json', '').replace('```', '').strip()
        
#         # בדיקה שהתוכן לא ריק לפני המרה
#         if not raw_text:
#              raise HTTPException(status_code=500, detail="Empty response from Gemini")

#         result = json.loads(raw_text)

#         return result

#     except Exception as e:
#         error_msg = str(e)
#         print(f"Error: {error_msg}")
        
#         if "429" in error_msg or "quota" in error_msg.lower():
#             raise HTTPException(
#                 status_code=429, 
#                 detail="API quota exceeded. Please wait a moment and try again."
#             )
        
#         raise HTTPException(status_code=500, detail=error_msg)

#     finally:
#         # --- אזור הניקוי החשוב ---
        
#         # מחיקה מהדיסק המקומי
#         if os.path.exists(temp_file_path):
#             try:
#                 os.remove(temp_file_path)
#             except:
#                 pass # אם לא הצליח למחוק לוקאלית, לא נורא

#         # מחיקה מהענן של גוגל (קריטי!)
#         if audio_file:
#             try:
#                 genai.delete_file(audio_file.name)
#                 print(f"Deleted remote file: {audio_file.name}")
#             except Exception as e:
#                 print(f"Warning: Could not delete from Google: {e}")

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

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
    uvicorn.run(app, host="0.0.0.0", port=9000)