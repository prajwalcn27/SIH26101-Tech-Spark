import re


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text


sample_text = """
Data Cleaning


is the process of

identifying    incorrect data
"""

cleaned_text = clean_text(sample_text)

print(cleaned_text)