import re


def extract_topics(text):

    keywords = [
        "Missing Values",
        "Duplicate Records",
        "Incorrect Data",
        "Inconsistent Formats",
        "Outliers",
        "Standardization",
        "Validation",
        "Data Quality",
        "Data Cleaning"
    ]

    found_topics = []

    for keyword in keywords:

        if re.search(
            re.escape(keyword),
            text,
            re.IGNORECASE
        ):

            found_topics.append(keyword)

    return found_topics


# Test only when this file is run directly
if __name__ == "__main__":

    import os

    from pdf_extractor import extract_text_from_pdf
    from text_cleaner import clean_text


    base_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )


    pdf_path = os.path.join(
        base_dir,
        "learning_materials",
        "Data_Cleaning.pdf"
    )


    text = extract_text_from_pdf(
        pdf_path
    )


    cleaned_text = clean_text(
        text
    )


    topics = extract_topics(
        cleaned_text
    )


    print("Topics found:")

    for topic in topics:
        print("-", topic)