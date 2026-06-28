from core.extraction.text_cleaner import (
    preprocess_text
)

sample = """
Hello! My name is Shruti.
I know Python, Machine Learning,
and SQL. I have completed 3 projects.
"""

cleaned = preprocess_text(sample)

print(cleaned)