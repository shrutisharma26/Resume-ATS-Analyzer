import pandas as pd


def create_dataframe(results):

    rows = []

    for candidate in results:

        rows.append({
            "Candidate":
                candidate["candidate"],

            "ATS Score":
                candidate["ats_score"],

            "Similarity Score":
                candidate["similarity_score"],

            "Skill Match":
                candidate["skill_score"],

            "Recommendation":
                candidate["recommendation"],

            "Matched Skills":
                ", ".join(
                    candidate["matched_skills"]
                ),

            "Missing Skills":
                ", ".join(
                    candidate["missing_skills"]
                )
        })

    return pd.DataFrame(rows)