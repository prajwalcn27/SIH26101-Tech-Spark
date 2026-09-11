import pymupdf


def extract_text_from_pdf(pdf_path):

    document = pymupdf.open(pdf_path)

    full_text = ""

    for page in document:
        full_text += page.get_text()

    document.close()

    return full_text


# Test only when this file is run directly
if __name__ == "__main__":

    import os

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

    text = extract_text_from_pdf(pdf_path)

    print(text)