import json
import re
from pathlib import Path


# Load skills from JSON file
BASE_DIR = Path(__file__).resolve().parent

with open(
        BASE_DIR / "skills_db.json",
        "r",
        encoding="utf-8") as file:

    SKILLS_DB = json.load(file)["skills"]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(found_skills)