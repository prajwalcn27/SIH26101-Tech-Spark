import re


def clean_text(text):
    """
    Clean common PDF extraction problems.
    """

    # Fix common UTF-8 / Latin-1 encoding issues
    replacements = {
        "â€“": "–",
        "â€”": "—",
        "â€˜": "‘",
        "â€™": "’",
        "â€œ": "“",
        "â€": "”",
        "â€¦": "…",
        "â€": '"',
        "NaÃ¯ve": "Naïve",
        "naÃ¯ve": "naïve",
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("              TEXT CLEANER")
    print("=" * 60)

    input_file = "extracted_text.txt"
    output_file = "cleaned_text.txt"

    print("\n📄 Reading extracted text...")

    try:
        with open(
            input_file,
            "r",
            encoding="utf-8"
        ) as file:
            text = file.read()

    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        exit()

    print("✅ Text loaded successfully!")

    print(f"Original characters: {len(text)}")
    print(f"Original words: {len(text.split())}")

    # Clean the text
    cleaned_text = clean_text(text)

    print("\n🧹 Cleaning text completed!")

    print(f"Cleaned characters: {len(cleaned_text)}")
    print(f"Cleaned words: {len(cleaned_text.split())}")

    # Save cleaned text
    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(cleaned_text)

    print("\n" + "=" * 60)
    print("✅ TEXT CLEANING COMPLETED!")
    print(f"📁 Saved as: {output_file}")
    print("=" * 60)

    # Show sample
    print("\n📖 First 30 lines:")
    print("-" * 60)

    print("\n".join(cleaned_text.splitlines()[:30]))

    print("\n" + "=" * 60)