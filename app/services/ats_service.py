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



def calculate_ats_score(resume_text):


    prompt = f"""

You are an ATS resume evaluator.


Analyze this resume:

{resume_text}


Give response in this format:


ATS Score: XX/100


Skills Match:

Experience:

Projects:


Suggestions:


Keep the answer professional.


"""


    response = model.generate_content(
        prompt
    )


    return response.text