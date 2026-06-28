import re

import nltk
from nltk.corpus import stopwords

# Download stopwords only once
try:
    STOP_WORDS = set(stopwords.words("english"))
except:
    nltk.download("stopwords")
    STOP_WORDS = set(stopwords.words("english"))


def clean_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def preprocess_text(text):

    text = clean_text(text)

    words = text.split()

    filtered_words = [
        word
        for word in words
        if word not in STOP_WORDS
    ]

    return " ".join(filtered_words)