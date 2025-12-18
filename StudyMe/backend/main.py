import os
import json
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai

# 1. הגדרות וטעינת מפתחות
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ שים לב: מפתח ה-API לא נמצא בקובץ .env")

genai.configure(api_key=api_key)

app = FastAPI()

# אפשור CORS כדי שהפרונטנד (React) יוכל לדבר עם השרת
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # בסביבת פרודקשן נגביל את זה
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    try:
        # א. שמירת הקובץ זמנית במערכת
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        # ב. העלאת הקובץ ל-Gemini File API (מאפשר ניתוח אודיו עמוק)
        print(f"Uploading {file.filename} to Gemini...")
        audio_file = genai.upload_file(path=temp_file_path)

        # ג. המתנה שהקובץ יעובד ע"י גוגל
        while audio_file.state.name == "PROCESSING":
            time.sleep(2)
            audio_file = genai.get_file(audio_file.name)

        # ד. הפרומפט המנצח - דורשים JSON מובנה
        prompt = """
        Analyze this audio recording for a student. 
        Return ONLY a JSON object with the following structure:
        {
          "summary": "A concise summary of the lecture",
          "key_points": ["Point 1", "Point 2"],
          "quiz": [
            {"question": "Question 1?", "options": ["A", "B", "C", "D"], "answer": "Correct Option"},
            {"question": "Question 2?", "options": ["A", "B", "C", "D"], "answer": "Correct Option"}
          ],
          "tasks": ["Task 1 based on lecture", "Task 2"]
        }
        Make sure the JSON is valid and the summary is helpful.
        """

        # ה. יצירת התוכן
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content([audio_file, prompt])
        
        # ניקוי ה-JSON (לפעמים המודל מחזיר אותו עם סימני ```json)
        raw_text = response.text.replace('```json', '').replace('```', '').strip()
        result = json.loads(raw_text)

        # ו. מחיקת הקובץ הזמני מהשרת שלנו
        os.remove(temp_file_path)

        return result

    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
        
        # טיפול בשגיאת מכסה
        if "429" in error_msg or "quota" in error_msg.lower():
            raise HTTPException(
                status_code=429, 
                detail="API quota exceeded. Please wait a moment and try again."
            )
        
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)