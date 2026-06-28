import os

from core.extraction.pdf_extractor import (
    extract_text_from_pdf
)

from core.scoring.ats_scorer import (
    calculate_ats_score
)

from core.analysis.recommendation import (
    get_recommendation
)


def process_resumes(
        resumes_folder,
        job_description):

    results = []

    for file_name in os.listdir(
            resumes_folder):

        if file_name.endswith(".pdf"):

            file_path = os.path.join(
                resumes_folder,
                file_name
            )

            resume_text = (
                extract_text_from_pdf(
                    file_path
                )
            )

            analysis = (
                calculate_ats_score(
                    resume_text,
                    job_description
                )
            )

            recommendation, emoji = (
                get_recommendation(
                    analysis["ats_score"]
                )
            )

            analysis["candidate"] = (
                file_name
            )

            analysis[
                "recommendation"
            ] = recommendation

            analysis["emoji"] = emoji

            results.append(
                analysis
            )

    results = sorted(
        results,
        key=lambda x:
            x["ats_score"],
        reverse=True
    )

    return results