import pymupdf
import os


def extract_text_from_pdf(pdf_path):
    """
    Extract text from all pages of a PDF file.
    """

    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return ""

    try:
        document = pymupdf.open(pdf_path)

        all_text = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text()

            if text.strip():
                all_text.append(
                    f"\n--- Page {page_number} ---\n{text}"
                )

        document.close()

        extracted_text = "\n".join(all_text)

        return extracted_text

    except Exception as error:
        print(f"❌ Error reading PDF: {error}")
        return ""


if __name__ == "__main__":

    print("=" * 50)
    print("          PDF TEXT EXTRACTOR")
    print("=" * 50)

    # Your actual learning material
    pdf_path = "../learning_materials/Data_Cleaning.pdf"

    output_file = "extracted_text.txt"

    print("\nReading PDF...")
    print("-" * 50)

    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        print("❌ No text extracted from PDF.")
    else:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text)

        print("✅ PDF text extracted successfully.")
        print(f"Characters extracted: {len(text)}")
        print(f"Saved as: {output_file}")

    print("=" * 50)