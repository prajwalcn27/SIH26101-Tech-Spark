import pymupdf
import os


def extract_text_from_pdf(pdf_path):

    try:
        # Check whether PDF exists
        if not os.path.exists(pdf_path):
            print(f"❌ PDF not found: {pdf_path}")
            return None

        # Open PDF
        document = pymupdf.open(pdf_path)

        extracted_text = ""

        # Read every page
        for page_number, page in enumerate(document, start=1):

            page_text = page.get_text("text")

            extracted_text += (
                f"\n--- Page {page_number} ---\n"
            )

            extracted_text += page_text

        # Close PDF
        document.close()

        return extracted_text

    except Exception as e:

        print("❌ PDF extraction error:")
        print(e)

        return None


# --------------------------------------------------
# Test PDF Reader
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 50)
    print("          PDF TEXT EXTRACTOR")
    print("=" * 50)

    # PDF file location
    pdf_path = "../learning_materials/ML_Module1.pdf"

    print("\nReading PDF...")
    print("-" * 50)

    text = extract_text_from_pdf(pdf_path)

    if text:

        print("✅ PDF text extracted successfully!")

        print("\nExtracted Text:")
        print("=" * 50)

        print(text)

        # Save extracted text
        output_file = "extracted_text.txt"

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(text)

        print("\n" + "=" * 50)
        print("✅ Text extraction completed!")
        print(f"📁 Saved as: {output_file}")
        print("=" * 50)

    else:

        print("❌ No text extracted from PDF.")