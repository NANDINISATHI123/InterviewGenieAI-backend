import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_resume(resume_text):

    prompt = f"""
You are an ATS Resume Analyzer.

Analyze this resume and return the result in this format.

Resume Score: __/100

ATS Score: __/100

Technical Skills:
- ...

Soft Skills:
- ...

Missing Skills:
- ...

Strengths:
- ...

Weaknesses:
- ...

Suggestions:
- ...

Suitable Job Roles:
- ...

Resume:

{resume_text}
"""

    response = model.generate_content(prompt)

    return response.text