from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from core.extraction.text_cleaner import (
    preprocess_text
)


def calculate_similarity(
        resume_text,
        jd_text):

    # Preprocess texts
    resume_text = preprocess_text(
        resume_text
    )

    jd_text = preprocess_text(
        jd_text
    )

    documents = [
        resume_text,
        jd_text
    ]

    tfidf = TfidfVectorizer()

    matrix = tfidf.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0]

    return round(
        similarity * 100,
        2
    )