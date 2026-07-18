def calculate_ats_score(resume_text):

    if not resume_text:
        return {
            "score": 0,
            "skills_found": [],
            "suggestions": [
                "Unable to extract resume text"
            ]
        }


    resume = resume_text.lower()


    skills = [
        "python",
        "java",
        "c++",
        "c",
        "sql",
        "html",
        "css",
        "javascript",
        "typescript",
        "react",
        "node",
        "fastapi",
        "django",
        "flask",
        "git",
        "github",
        "mongodb",
        "postgresql",
        "machine learning",
        "artificial intelligence",
        "aws",
        "docker"
    ]


    found = []

    score = 0


    for skill in skills:

        if skill.lower() in resume:

            found.append(skill)

            score += 5



    sections = [
        "education",
        "project",
        "experience",
        "internship",
        "certification",
        "achievement"
    ]


    for section in sections:

        if section in resume:

            score += 10



    if score > 100:

        score = 100



    suggestions = []


    if len(found) < 5:

        suggestions.append(
            "Add more technical skills"
        )


    if "project" not in resume:

        suggestions.append(
            "Add project descriptions with technologies used"
        )


    if "experience" not in resume:

        suggestions.append(
            "Add internship or experience details"
        )


    if not suggestions:

        suggestions.append(
            "Resume looks ATS friendly"
        )



    return {

        "score": score,

        "skills_found": found,

        "suggestions": suggestions

    }