import re
import os


# ============================================================
# TOPIC EXTRACTOR
# ============================================================

def clean_topic(topic):
    """Clean and normalize a topic."""

    topic = topic.strip()

    # Remove unwanted punctuation at the end
    topic = re.sub(r'[,;:.…]+$', '', topic)

    # Remove multiple spaces
    topic = re.sub(r'\s+', ' ', topic)

    return topic.strip()


def add_topic(topics, topic):
    """Add topic if it is valid and not already present."""

    topic = clean_topic(topic)

    if not topic:
        return

    # Ignore very long sentences
    if len(topic.split()) > 12:
        return

    # Ignore sentences ending with common sentence patterns
    unwanted_phrases = [
        "is like",
        "involves an agent",
        "can handle both",
        "mimic the way",
        "as it yields",
        "are the foundation",
        "showing how",
        "train and test a model"
    ]

    lower_topic = topic.lower()

    for phrase in unwanted_phrases:
        if phrase in lower_topic:
            return

    # Avoid duplicates
    if lower_topic not in [t.lower() for t in topics]:
        topics.append(topic)


def extract_topics(text):

    topics = []

    lines = text.splitlines()

    # ========================================================
    # 1. Extract topics from Lecture lines
    # ========================================================

    for line in lines:

        line = line.strip()

        if not line:
            continue

        lecture_match = re.match(
            r'Lecture\s+\d+\s*:\s*(.+)',
            line,
            re.IGNORECASE
        )

        if lecture_match:

            lecture_content = lecture_match.group(1)

            # Split lecture content by comma
            parts = lecture_content.split(',')

            for part in parts:

                part = clean_topic(part)

                if part:
                    add_topic(topics, part)

    # ========================================================
    # 2. Important ML topics
    # ========================================================

    important_patterns = [

        r'^Introduction to Machine Learning$',

        r'^Types of Machine Learning$',

        r'^Supervised Learning$',

        r'^UnSupervised Learning$',

        r'^Unsupervised Learning$',

        r'^Reinforcement Learning$',

        r'^Performance measures.*$',

        r'^Performance Measures.*$',

        r'^Bias[- ]variance Tradeoff.*$',

        r'^Bias[- ]Variance Tradeoff.*$',

        r'^Decision Tree$',

        r'^Decision Tree…$',

        r'^Types of Decision Trees$',

        r'^Learning with Trees.*$',

        r'^CART$',

        r'^Types of Random variable.*$',

        r'^Types of Probability Density functions.*$',

        r'^Na[iï]ve Bayes.*$',

        r'^The Na[iï]ve Bayes classifier.*$',

        r'^Types of Na[iï]ve Bayes.*$',

        r'^Bayesian Networks$',

        r'^Bayesian Network$',

    ]

    # ========================================================
    # 3. Search lines for important topics
    # ========================================================

    for line in lines:

        line = line.strip()

        if not line:
            continue

        for pattern in important_patterns:

            if re.match(pattern, line, re.IGNORECASE):

                add_topic(topics, line)

                break

    # ========================================================
    # 4. Remove unwanted lecture fragments
    # ========================================================

    unwanted = [

        "Program Integration",

        "Course Plan",

        "Turning data into Probabilities",

    ]

    final_topics = []

    for topic in topics:

        # Skip unwanted fragments
        if topic.lower() in [
            item.lower() for item in unwanted
        ]:
            continue

        # Skip very short meaningless values
        if len(topic) < 3:
            continue

        final_topics.append(topic)

    # ========================================================
    # 5. Remove duplicates again
    # ========================================================

    unique_topics = []

    for topic in final_topics:

        if topic.lower() not in [
            t.lower() for t in unique_topics
        ]:
            unique_topics.append(topic)

    return unique_topics


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("              CLEAN TOPIC EXTRACTOR")
    print("=" * 60)

    input_file = "cleaned_text.txt"
    output_file = "topics.txt"

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

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    print("✅ Text loaded successfully!")

    print(f"\nCharacters: {len(text)}")
    print(f"Words: {len(text.split())}")

    # --------------------------------------------------------
    # Extract topics
    # --------------------------------------------------------

    print("\n🔍 Extracting clean learning topics...")

    topics = extract_topics(text)

    # --------------------------------------------------------
    # Display topics
    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("LEARNING TOPICS")
    print("-" * 60)

    for number, topic in enumerate(topics, start=1):

        print(f"{number}. {topic}")

    print("\n" + "-" * 60)
    print(f"📚 Total topics found: {len(topics)}")
    print("-" * 60)

    # --------------------------------------------------------
    # Save topics
    # --------------------------------------------------------

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        for number, topic in enumerate(topics, start=1):

            file.write(
                f"{number}. {topic}\n"
            )

    # --------------------------------------------------------
    # Final message
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("✅ TOPIC EXTRACTION COMPLETED!")
    print(f"📁 Saved as: {output_file}")
    print("=" * 60)