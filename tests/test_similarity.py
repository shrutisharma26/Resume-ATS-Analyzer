from core.scoring.similarity import (
    calculate_similarity
)

resume = """
Python Machine Learning SQL
Deep Learning NLP
"""

job_description = """
Looking for a candidate
with Python, SQL,
Machine Learning skills.
"""

score = calculate_similarity(
    resume,
    job_description
)

print(
    f"Similarity Score: {score}%"
)
