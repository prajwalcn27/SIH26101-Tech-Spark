import re
import json
import os


# ============================================================
# CONTENT INDEXER
# ============================================================

def parse_sections(text):
    """
    Read text_sections.txt and convert it into structured sections.
    """

    sections = []

    # Find SECTION blocks
    pattern = re.compile(
        r'={10,}\s*'
        r'SECTION\s+(\d+)\s*'
        r'={10,}\s*'
        r'(.*?)(?='
        r'={10,}\s*SECTION\s+\d+'
        r'|$)',
        re.DOTALL | re.IGNORECASE
    )

    matches = pattern.findall(text)

    for section_number, section_text in matches:

        section_text = section_text.strip()

        # ----------------------------------------------------
        # Find page numbers
        # Example:
        # --- Page 10 ---
        # ----------------------------------------------------

        page_matches = re.findall(
            r'---\s*Page\s+(\d+)\s*---',
            section_text,
            re.IGNORECASE
        )

        pages = [int(page) for page in page_matches]

        # ----------------------------------------------------
        # Remove page markers from searchable content
        # ----------------------------------------------------

        searchable_text = re.sub(
            r'---\s*Page\s+\d+\s*---',
            '',
            section_text,
            flags=re.IGNORECASE
        )

        searchable_text = re.sub(
            r'\s+',
            ' ',
            searchable_text
        ).strip()

        # ----------------------------------------------------
        # Count words
        # ----------------------------------------------------

        word_count = len(searchable_text.split())

        # ----------------------------------------------------
        # Create section object
        # ----------------------------------------------------

        section = {
            "section_id": int(section_number),
            "pages": pages,
            "word_count": word_count,
            "text": searchable_text
        }

        sections.append(section)

    return sections


# ============================================================
# CREATE INDEX
# ============================================================

def create_content_index(text, source_file):

    sections = parse_sections(text)

    index = {
        "document": {
            "file_name": os.path.basename(source_file),
            "total_sections": len(sections),
            "total_words": sum(
                section["word_count"]
                for section in sections
            )
        },
        "sections": sections
    }

    return index


# ============================================================
# SAVE INDEX
# ============================================================

def save_index(index, output_file):

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            index,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("                 CONTENT INDEXER")
    print("=" * 60)

    input_file = "text_sections.txt"
    output_file = "content_index.json"

    # --------------------------------------------------------
    # Check input file
    # --------------------------------------------------------

    if not os.path.exists(input_file):

        print(f"\n❌ File not found: {input_file}")

        print(
            "\nPlease run:"
            "\n1. python pdf_reader.py"
            "\n2. python text_cleaner.py"
            "\n3. python text_splitter.py"
        )

        exit()

    # --------------------------------------------------------
    # Read sections
    # --------------------------------------------------------

    print("\n📄 Reading text sections...")

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    print("✅ Text sections loaded successfully!")

    # --------------------------------------------------------
    # Create index
    # --------------------------------------------------------

    print("\n🔎 Creating content index...")

    index = create_content_index(
        text,
        "ML_Module1.pdf"
    )

    sections = index["sections"]

    # --------------------------------------------------------
    # Display statistics
    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("CONTENT INDEX INFORMATION")
    print("-" * 60)

    print(
        f"📄 Document: "
        f"{index['document']['file_name']}"
    )

    print(
        f"📚 Sections: "
        f"{index['document']['total_sections']}"
    )

    print(
        f"📝 Total words: "
        f"{index['document']['total_words']}"
    )

    # --------------------------------------------------------
    # Display section information
    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("SECTION INFORMATION")
    print("-" * 60)

    for section in sections:

        page_text = ", ".join(
            str(page)
            for page in section["pages"]
        )

        print(
            f"Section {section['section_id']}"
            f" | Pages: {page_text}"
            f" | Words: {section['word_count']}"
        )

    # --------------------------------------------------------
    # Save JSON index
    # --------------------------------------------------------

    save_index(
        index,
        output_file
    )

    print("\n" + "=" * 60)
    print("✅ CONTENT INDEX CREATED SUCCESSFULLY!")
    print(f"📁 Saved as: {output_file}")
    print("=" * 60)

    # --------------------------------------------------------
    # Show first section preview
    # --------------------------------------------------------

    if sections:

        first_section = sections[0]

        print("\n📖 FIRST SECTION PREVIEW")
        print("-" * 60)

        print(
            first_section["text"][:1000]
        )

        if len(first_section["text"]) > 1000:
            print("\n... [continues] ...")

    print("\n" + "=" * 60)