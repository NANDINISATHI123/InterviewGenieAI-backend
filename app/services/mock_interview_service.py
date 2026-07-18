import os
import google.generativeai as genai
import google.api_core.exceptions
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")


def evaluate_answer(question, answer):

    prompt = f"""
You are a technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Give:

Score /10

Strengths

Weaknesses

Improved Answer

Suggestions
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except google.api_core.exceptions.ResourceExhausted:
        return "⚠️ Gemini API quota exceeded."

    except Exception as e:
        return f"Error evaluating answer: {str(e)}"