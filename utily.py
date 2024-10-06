import os
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv
from crud import update_translation_task
from sqlalchemy.orm import Session

load_dotenv()
gemini_api_key = os.getenv("gemini_api_key")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-pro')


def perform_translation(task_id: int, text: str, languages: List[str], db: Session):
    translations = {}

    for i in languages:
        try:
            response = model.generate_content(f"Can you translate this text {text} to {i}")
            translations[i] = response.text
        except Exception as e:
            print(f"Error translation to {i}:{e}")
            translations[i] = f"Error:{e}"
    update_translation_task(db, task_id, translations)
