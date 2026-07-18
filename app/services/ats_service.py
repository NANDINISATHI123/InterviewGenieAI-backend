import re

def calculate_ats_score(resume_text):

    score = 0

    resume = resume_text.lower()

    skills = [
        "python",
        "java",
        "c",
        "c++",
        "sql",   
        "html",
        "css",
        "javascript",
        "react",
        "fastapi",
        "django",
        "flask",
        "git",
        "github"
    ]

    found = []

    for skill in skills:
        if skill in resume:
            found.append(skill)
            score += 5

    if "education" in resume:
        score += 10

    if "project" in resume:
        score += 15

    if "experience" in resume:
        score += 10

    if "internship" in resume:
        score += 10

    if score > 100:
        score = 100

    return f"""
ATS Score: {score}/100

Skills Found:
{', '.join(found) if found else 'No major skills detected'}

Suggestions:
• Add more technical skills.
• Include measurable project achievements.
• Add internships if available.
• Keep resume to one page.
• Use ATS-friendly headings.
"""