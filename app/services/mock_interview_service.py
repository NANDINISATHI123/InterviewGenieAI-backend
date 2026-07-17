import os
import google.generativeai as genai

from dotenv import load_dotenv


load_dotenv()


genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


model = genai.GenerativeModel(
    "gemini-2.5-flash-lite"
)



def evaluate_answer(question, answer):


    prompt = f"""

You are a technical interviewer.


Question:

{question}



Candidate Answer:

{answer}



Evaluate the answer.


Give:


Score out of 10

Strengths

Weaknesses

Improved Answer

Suggestions



"""


    response = model.generate_content(
        prompt
    )


    return response.text