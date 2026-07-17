import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")


def generate_questions(resume_text):

    prompt = f"""
You are an experienced software engineering interviewer.

Based on the following resume, generate:

1. 10 Technical Interview Questions
2. 5 HR Interview Questions
3. 5 Project-Based Interview Questions
4. 5 Coding Questions

Return the answer in markdown with headings.

Resume:

{resume_text}
"""

    response = model.generate_content(prompt)

    return response.text
