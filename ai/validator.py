import re


def validate_mcq(question, source_material):
    """
    Simple local validation for an AI-generated MCQ.
    Checks source support, options, answer, ambiguity,
    duplicate options, topic and difficulty.
    """

    issues = []

    # ---------------------------------------
    # Required fields
    # ---------------------------------------

    required_fields = [
        "question",
        "options",
        "correct_answer",
        "explanation",
        "topic",
        "difficulty"
    ]

    for field in required_fields:
        if field not in question:
            issues.append(f"Missing field: {field}")

    if issues:
        return {
            "status": "INVALID",
            "confidence": 0,
            "issues": issues
        }

    # ---------------------------------------
    # Check options
    # ---------------------------------------

    options = question["options"]

    if not isinstance(options, dict):
        issues.append("Options must be a dictionary.")

    else:
        expected_options = {"A", "B", "C", "D"}

        if set(options.keys()) != expected_options:
            issues.append("MCQ must contain exactly A, B, C and D options.")

        # Check duplicate options
        option_values = [
            str(value).strip().lower()
            for value in options.values()
        ]

        if len(option_values) != len(set(option_values)):
            issues.append("Duplicate options found.")

        # Check empty options
        for key, value in options.items():
            if not str(value).strip():
                issues.append(f"Option {key} is empty.")

    # ---------------------------------------
    # Check correct answer
    # ---------------------------------------

    correct_answer = str(question["correct_answer"]).strip().upper()

    if correct_answer not in {"A", "B", "C", "D"}:
        issues.append("Correct answer must be A, B, C or D.")

    # ---------------------------------------
    # Check question clarity
    # ---------------------------------------

    question_text = str(question["question"]).strip()

    if len(question_text) < 10:
        issues.append("Question is too short.")

    if "?" not in question_text:
        issues.append("Question may be unclear because it does not contain a question mark.")

    # ---------------------------------------
    # Check topic
    # ---------------------------------------

    topic = str(question["topic"]).strip()

    if not topic:
        issues.append("Topic is empty.")

    # ---------------------------------------
    # Check difficulty
    # ---------------------------------------

    difficulty = str(question["difficulty"]).strip().capitalize()

    if difficulty not in {"Easy", "Medium", "Hard"}:
        issues.append("Difficulty must be Easy, Medium or Hard.")

    # ---------------------------------------
    # Source support check
    # ---------------------------------------

    source_lower = source_material.lower()

    # Important words from question and correct answer
    text_to_check = (
        question_text + " " +
        str(question["options"].get(correct_answer, "")) + " " +
        str(question["explanation"])
    ).lower()

    words = re.findall(r"[a-zA-Z]{4,}", text_to_check)

    supported_words = 0

    for word in words:
        if word in source_lower:
            supported_words += 1

    if words:
        support_percentage = (supported_words / len(words)) * 100
    else:
        support_percentage = 0

    if support_percentage < 30:
        issues.append("Answer or explanation may not be sufficiently supported by the source material.")

    # ---------------------------------------
    # Final status
    # ---------------------------------------

    if not issues:
        status = "VALID"
        confidence = 95

    elif any(
        "not sufficiently supported" in issue.lower()
        or "unclear" in issue.lower()
        for issue in issues
    ):
        status = "REVIEW"
        confidence = 60

    else:
        status = "INVALID"
        confidence = 30

    return {
        "status": status,
        "confidence": confidence,
        "source_support_percentage": round(support_percentage, 2),
        "issues": issues
    }


# ---------------------------------------
# LOCAL TEST
# ---------------------------------------

if __name__ == "__main__":

    sample_material = """
    Data cleaning is the process of detecting and correcting inaccurate,
    incomplete, duplicated, or inconsistent data.

    Missing values can be handled by removing records, replacing values,
    or using statistical methods.

    Duplicate records occur when the same data is stored more than once.
    Removing duplicate records helps improve data quality.
    """

    sample_question = {
        "question": "What is the purpose of removing duplicate records?",
        "options": {
            "A": "To improve data quality",
            "B": "To create more duplicate records",
            "C": "To increase missing values",
            "D": "To remove all statistical methods"
        },
        "correct_answer": "A",
        "explanation": "Removing duplicate records helps improve data quality.",
        "topic": "Data Cleaning",
        "difficulty": "Easy"
    }

    result = validate_mcq(sample_question, sample_material)

    print("\n===== MCQ VALIDATION =====")
    print(f"Status: {result['status']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Source Support: {result['source_support_percentage']}%")
    print(f"Issues: {result['issues']}")