from core.extraction.pdf_extractor import (
    extract_text_from_pdf
)

text = extract_text_from_pdf(
    "data/resumes/sample_resume.pdf"
)

print(text[:1000])
