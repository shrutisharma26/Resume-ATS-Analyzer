from core.skills.skill_extractor import extract_skills


sample_text = """
I have experience in Python, Machine Learning,
SQL and Docker.
"""

print(extract_skills(sample_text))