from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.user import UserRegister
from app.schemas.login import UserLogin

from app.database import SessionLocal
from app.services.ats_service import calculate_ats_score
from app.models.user import User
from app.models.resume import Resume
from app.models.interview import Interview


from app.auth import verify_password
from app.token import create_access_token


from app.utils.resume_parser import extract_text_from_pdf

from app.services.gemini_service import analyze_resume
from app.services.interview_service import generate_questions
from app.services.mock_interview_service import evaluate_answer


import bcrypt
import shutil
import os



app = FastAPI()



# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://interviewgenieai-e1iueufng-nandinisathi123-1467s-projects.vercel.app",
        "https://interviewgenieai-zeta.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------- HOME ----------------


@app.get("/")
def home():

    return {

        "message":"Backend Running"

    }




# ---------------- REGISTER ----------------


@app.post("/register")
def register(user: UserRegister):

    db = SessionLocal()


    try:


        existing_user = db.query(User).filter(

            User.email == user.email

        ).first()



        if existing_user:

            return {

                "message":"Email already registered"

            }



        hashed_password = bcrypt.hashpw(

            user.password.encode("utf-8"),

            bcrypt.gensalt()

        ).decode("utf-8")




        new_user = User(

            name=user.name,

            email=user.email,

            password=hashed_password

        )



        db.add(new_user)

        db.commit()

        db.refresh(new_user)



        return {

            "message":"User Registered Successfully"

        }



    finally:

        db.close()





# ---------------- LOGIN ----------------


@app.post("/login")
def login(user: UserLogin):


    db = SessionLocal()



    try:


        db_user = db.query(User).filter(

            User.email == user.email

        ).first()



        if not db_user:

            return {

                "message":"User not found"

            }



        if not verify_password(

            user.password,

            db_user.password

        ):

            return {

                "message":"Invalid password"

            }



        token = create_access_token(

            {

                "email":db_user.email

            }

        )



        return {


            "message":"Login Successful",

            "access_token":token,

            "email":db_user.email


        }



    finally:

        db.close()






# ---------------- RESUME UPLOAD ----------------



@app.post("/upload-resume")
def upload_resume(
    resume: UploadFile = File(...)
):


    upload_folder="uploads"



    if not os.path.exists(upload_folder):

        os.makedirs(upload_folder)



    file_path=os.path.join(

        upload_folder,

        resume.filename

    )



    with open(file_path,"wb") as buffer:


        shutil.copyfileobj(

            resume.file,

            buffer

        )




    resume_text = extract_text_from_pdf(

        file_path

    )



    analysis = analyze_resume(

        resume_text

    )



    db = SessionLocal()



    try:


        new_resume = Resume(

            filename=resume.filename,

            resume_text=resume_text,

            analysis=analysis

        )



        db.add(new_resume)

        db.commit()



    finally:

        db.close()




    return {


        "message":"Resume Uploaded Successfully",

        "filename":resume.filename,

        "analysis":analysis


    }





# ---------------- RESUME HISTORY ----------------



@app.get("/resume-history")
def resume_history():


    db=SessionLocal()



    try:


        resumes=db.query(Resume).all()



        data=[]



        for resume in resumes:


            data.append({

                "id":resume.id,

                "filename":resume.filename,

                "analysis":resume.analysis

            })



        return data



    finally:

        db.close()





# ---------------- GENERATE QUESTIONS ----------------



@app.post("/generate-questions")
def generate_interview_questions(
    resume: UploadFile = File(...)
):


    upload_folder="uploads"



    if not os.path.exists(upload_folder):

        os.makedirs(upload_folder)




    file_path=os.path.join(

        upload_folder,

        resume.filename

    )



    with open(file_path,"wb") as buffer:


        shutil.copyfileobj(

            resume.file,

            buffer

        )




    resume_text = extract_text_from_pdf(

        file_path

    )



    questions = generate_questions(

        resume_text

    )



    return {


        "questions":questions


    }







# ---------------- MOCK INTERVIEW EVALUATION ----------------



@app.post("/evaluate-answer")
def evaluate_interview_answer(

    email:str = Body(...),

    question:str = Body(...),

    answer:str = Body(...)

):


    feedback = evaluate_answer(

        question,

        answer

    )



    score=0



    db=SessionLocal()



    try:


        interview = Interview(

            email=email,

            question=question,

            answer=answer,

            feedback=feedback,

            score=score

        )


        db.add(interview)

        db.commit()



    finally:

        db.close()




    return {


        "message":"Answer Evaluated Successfully",

        "feedback":feedback

    }





# ---------------- INTERVIEW HISTORY ----------------



@app.get("/interview-history/{email}")
def interview_history(email:str):


    db=SessionLocal()



    try:


        interviews=db.query(Interview).filter(

            Interview.email==email

        ).all()



        data=[]



        for item in interviews:


            data.append({

                "id":item.id,

                "question":item.question,

                "answer":item.answer,

                "feedback":item.feedback,

                "score":item.score

            })



        return data



    finally:

        db.close()






# ---------------- PROFILE ----------------



@app.get("/profile/{email}")
def profile(email:str):


    db=SessionLocal()



    try:


        user=db.query(User).filter(

            User.email==email

        ).first()



        resume_count=db.query(Resume).count()



        interview_count=db.query(Interview).count()



        return {


            "name":user.name,

            "email":user.email,

            "resume_count":resume_count,

            "interview_attempts":interview_count,

            "average_score":0


        }



    finally:

        db.close()
        # ---------------- ATS SCORE ----------------


@app.post("/ats-score")
def ats_score(
    resume: UploadFile = File(...)
):


    upload_folder="uploads"



    if not os.path.exists(upload_folder):

        os.makedirs(upload_folder)



    file_path=os.path.join(

        upload_folder,

        resume.filename

    )



    with open(file_path,"wb") as buffer:


        shutil.copyfileobj(

            resume.file,

            buffer

        )



    resume_text = extract_text_from_pdf(

        file_path

    )



    score = calculate_ats_score(

        resume_text

    )



    return {


        "filename":resume.filename,

        "ats_score":score


    }
# ---------------- ANALYTICS ----------------


@app.get("/analytics/{email}")
def analytics(email:str):


    db = SessionLocal()


    try:


        total_resumes = db.query(
            Resume
        ).count()



        total_interviews = db.query(
            Interview
        ).filter(
            Interview.email == email
        ).count()



        interviews = db.query(
            Interview
        ).filter(
            Interview.email == email
        ).all()



        average_score = 0



        if interviews:


            total = 0


            for item in interviews:

                if item.score:

                    total += item.score



            average_score = round(
                total / len(interviews),
                2
            )



        return {


            "total_resumes":total_resumes,

            "total_interviews":total_interviews,

            "average_score":average_score


        }


    finally:

        db.close()