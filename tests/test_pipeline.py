from core.pipeline import (
    process_resumes
)

job_description = """
Looking for candidates with
Python, SQL, Machine Learning,
Docker and AWS skills.
"""

results = process_resumes(
    "data/resumes",
    job_description
)

for candidate in results:

    print("\n" + "="*50)

    print(
        candidate["candidate"]
    )

    print(
        "ATS Score:",
        candidate["ats_score"]
    )

    print(
        "Recommendation:",
        candidate["recommendation"],
        candidate["emoji"]
    )

    print(
        "Matched Skills:",
        candidate["matched_skills"]
    )

    print(
        "Missing Skills:",
        candidate["missing_skills"]
    )