import os
import google.generativeai as genai
import google.api_core.exceptions
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")


def analyze_resume(resume_text):

    prompt = f"""
You are an ATS Resume Analyzer.

Analyze this resume.

Resume:

{resume_text}
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except google.api_core.exceptions.ResourceExhausted:
        return "⚠️ Gemini API quota exceeded. Please try again later."

    except Exception as e:
        return f"Error analyzing resume: {str(e)}"