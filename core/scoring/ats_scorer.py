from core.scoring.similarity import (
    calculate_similarity
)

from core.skills.skill_extractor import (
    extract_skills
)

from core.analysis.section_checker import (
    check_sections
)


def calculate_ats_score(
        resume_text,
        jd_text):

    # ---------- Similarity Score ----------
    similarity_score = calculate_similarity(
        resume_text,
        jd_text
    )

    # ---------- Skill Match ----------
    resume_skills = set(
        extract_skills(resume_text)
    )

    jd_skills = set(
        extract_skills(jd_text)
    )

    matched_skills = (
        resume_skills.intersection(jd_skills)
    )

    if len(jd_skills) > 0:

        skill_score = (
            len(matched_skills)
            / len(jd_skills)
        ) * 100

    else:
        skill_score = 0

    # ---------- Resume Completeness ----------
    present_sections, _ = check_sections(
        resume_text
    )

    section_score = (
        len(present_sections) / 6
    ) * 100

    # ---------- Final Weighted Score ----------

    final_score = (
            0.50 * skill_score
            + 0.35 * similarity_score
            + 0.15 * section_score
    )

    return {
        "ats_score":
            float(round(final_score, 2)),

        "similarity_score":
            float(round(similarity_score, 2)),

        "skill_score":
            float(round(skill_score, 2)),

        "section_score":
            float(round(section_score, 2)),

        "matched_skills":
            list(matched_skills),

        "missing_skills":
            list(
                jd_skills - resume_skills
            )
    }