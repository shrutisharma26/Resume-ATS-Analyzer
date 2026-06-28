from core.scoring.ats_scorer import (
    calculate_ats_score
)

resume = """
Education

Skills:
Python SQL Machine Learning

Projects:
NLP Resume Screening System

Experience:
Intern at ABC
"""

jd = """
Looking for candidates with
Python, SQL, Machine Learning,
Docker and AWS.
"""

result = calculate_ats_score(
    resume,
    jd
)

print(result)