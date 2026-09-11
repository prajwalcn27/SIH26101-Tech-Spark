import re
import os


# ============================================================
# TEXT SPLITTER
# ============================================================

def split_text_into_sections(text, max_words=500):
    """
    Split cleaned text into smaller sections.

    Each section will contain approximately max_words words.
    """

    # --------------------------------------------------------
    # Step 1: Remove excessive spaces
    # --------------------------------------------------------
    text = re.sub(r'[ \t]+', ' ', text)

    # --------------------------------------------------------
    # Step 2: Normalize blank lines
    # --------------------------------------------------------
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    # --------------------------------------------------------
    # Step 3: Split text into lines
    # --------------------------------------------------------
    lines = text.splitlines()

    sections = []
    current_section = []
    current_word_count = 0

    # --------------------------------------------------------
    # Step 4: Create sections
    # --------------------------------------------------------
    for line in lines:

        line = line.strip()

        # Skip completely empty lines
        if not line:
            continue

        # Count words in current line
        line_words = line.split()
        line_word_count = len(line_words)

        # If adding this line exceeds the limit,
        # save the current section first.
        if (
            current_word_count + line_word_count > max_words
            and current_section
        ):
            sections.append("\n".join(current_section))

            current_section = []
            current_word_count = 0

        # Add line to current section
        current_section.append(line)
        current_word_count += line_word_count

    # --------------------------------------------------------
    # Step 5: Add remaining text
    # --------------------------------------------------------
    if current_section:
        sections.append("\n".join(current_section))

    return sections


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("                  TEXT SPLITTER")
    print("=" * 60)

    # --------------------------------------------------------
    # Input and output files
    # --------------------------------------------------------
    input_file = "cleaned_text.txt"
    output_file = "text_sections.txt"

    # --------------------------------------------------------
    # Check input file
    # --------------------------------------------------------
    if not os.path.exists(input_file):
        print(f"\n❌ File not found: {input_file}")
        print("Please run text_cleaner.py first.")
        exit()

    # --------------------------------------------------------
    # Read cleaned text
    # --------------------------------------------------------
    print("\n📄 Reading cleaned text...")

    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    print("✅ Text loaded successfully!")

    # --------------------------------------------------------
    # Display text statistics
    # --------------------------------------------------------
    character_count = len(text)
    word_count = len(text.split())

    print(f"\nTotal characters: {character_count}")
    print(f"Total words: {word_count}")

    # --------------------------------------------------------
    # Split text
    # --------------------------------------------------------
    print("\n✂️ Splitting text into sections...")

    sections = split_text_into_sections(
        text,
        max_words=500
    )

    # --------------------------------------------------------
    # Display number of sections
    # --------------------------------------------------------
    print(f"\n✅ Text splitting completed!")
    print(f"📚 Number of sections: {len(sections)}")

    # --------------------------------------------------------
    # Save sections
    # --------------------------------------------------------
    with open(output_file, "w", encoding="utf-8") as file:

        for index, section in enumerate(sections, start=1):

            file.write("=" * 60)
            file.write(f"\nSECTION {index}\n")
            file.write("=" * 60)
            file.write("\n\n")

            file.write(section)

            file.write("\n\n")

    print(f"\n📁 Saved as: {output_file}")

    # --------------------------------------------------------
    # Display first 3 sections
    # --------------------------------------------------------
    print("\n" + "=" * 60)
    print("📖 FIRST 3 SECTIONS")
    print("=" * 60)

    for index, section in enumerate(sections[:3], start=1):

        print(f"\n{'-' * 60}")
        print(f"SECTION {index}")
        print(f"{'-' * 60}")

        print(section[:1500])

        if len(section) > 1500:
            print("\n... [section continues] ...")

    # --------------------------------------------------------
    # Final message
    # --------------------------------------------------------
    print("\n" + "=" * 60)
    print("✅ TEXT SPLITTING COMPLETED SUCCESSFULLY!")
    print("=" * 60)