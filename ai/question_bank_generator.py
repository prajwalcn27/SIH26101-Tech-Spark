import json

from pdf_reader import extract_text_from_pdf
from mcq_generator import generate_mcqs
from validator import validate_mcqs


# ============================================================
# CONFIGURATION
# ============================================================

PDF_PATH = "../learning_materials/ML_Module1.pdf"

NUMBER_OF_QUESTIONS = 5

OUTPUT_FILE = "question_bank.json"


# ============================================================
# SAVE QUESTION BANK
# ============================================================

def save_question_bank(questions, filename):

    question_bank = {
        "questions": questions
    }

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            question_bank,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\n✅ Question bank saved to: {filename}"
    )


# ============================================================
# FILTER VALID QUESTIONS
# ============================================================

def filter_valid_questions(mcqs, validation):

    questions = mcqs.get(
        "questions",
        []
    )

    validation_results = validation.get(
        "validation_results",
        []
    )

    valid_questions = []

    for question, result in zip(
        questions,
        validation_results
    ):

        status = result.get(
            "status",
            "INVALID"
        )

        confidence = result.get(
            "confidence",
            0
        )

        if (
            status == "VALID"
            and confidence >= 80
        ):

            valid_questions.append(question)

    return valid_questions


# ============================================================
# DISPLAY QUESTIONS
# ============================================================

def display_questions(questions):

    print("\n" + "=" * 60)
    print("              VALID QUESTION BANK")
    print("=" * 60)

    if not questions:

        print(
            "\n❌ No valid questions found."
        )

        return

    for index, question in enumerate(
        questions,
        start=1
    ):

        print(
            f"\n📘 Question {index}"
        )

        print(
            f"   Topic      : "
            f"{question.get('topic', 'Unknown')}"
        )

        print(
            f"   Difficulty : "
            f"{question.get('difficulty', 'Unknown')}"
        )

        print(
            f"   Question   : "
            f"{question.get('question', '')}"
        )

        options = question.get(
            "options",
            {}
        )

        for key, value in options.items():

            print(
                f"      {key}. {value}"
            )

        print(
            f"   Answer     : "
            f"{question.get('correct_answer', '')}"
        )

        print(
            f"   Explanation: "
            f"{question.get('explanation', '')}"
        )


# ============================================================
# MAIN QUESTION BANK GENERATOR
# ============================================================

def generate_question_bank():

    print("=" * 60)
    print("             QUESTION BANK GENERATOR")
    print("=" * 60)

    # --------------------------------------------------------
    # STEP 1: READ LEARNING MATERIAL
    # --------------------------------------------------------

    print("\n📄 STEP 1: Reading learning material...")

    learning_material = extract_text_from_pdf(
        PDF_PATH
    )

    if not learning_material:

        print(
            "❌ No learning material extracted."
        )

        return

    print(
        "✅ Learning material extracted."
    )

    print(
        f"   Characters: "
        f"{len(learning_material)}"
    )

    # --------------------------------------------------------
    # STEP 2: GENERATE MCQs
    # --------------------------------------------------------

    print(
        "\n🤖 STEP 2: Generating MCQs using Gemini..."
    )

    mcqs = generate_mcqs(
        learning_material,
        number_of_questions=NUMBER_OF_QUESTIONS
    )

    if not mcqs:

        print(
            "\n❌ MCQ generation failed."
        )

        print(
            "Possible reason: Gemini API quota "
            "or service availability."
        )

        return

    generated_questions = mcqs.get(
        "questions",
        []
    )

    print(
        f"✅ Generated "
        f"{len(generated_questions)} questions."
    )

    # --------------------------------------------------------
    # STEP 3: VALIDATE MCQs
    # --------------------------------------------------------

    print(
        "\n🔎 STEP 3: Validating generated questions..."
    )

    validation = validate_mcqs(
        learning_material,
        mcqs
    )

    if not validation:

        print(
            "\n❌ Validation failed."
        )

        return

    validation_results = validation.get(
        "validation_results",
        []
    )

    print(
        f"✅ Validated "
        f"{len(validation_results)} questions."
    )

    # --------------------------------------------------------
    # STEP 4: KEEP ONLY VALID QUESTIONS
    # --------------------------------------------------------

    print(
        "\n✅ STEP 4: Filtering valid questions..."
    )

    valid_questions = filter_valid_questions(
        mcqs,
        validation
    )

    print(
        f"✅ Accepted "
        f"{len(valid_questions)} questions."
    )

    rejected_count = (
        len(generated_questions)
        - len(valid_questions)
    )

    print(
        f"❌ Rejected/flagged "
        f"{rejected_count} questions."
    )

    # --------------------------------------------------------
    # STEP 5: DISPLAY VALID QUESTIONS
    # --------------------------------------------------------

    display_questions(
        valid_questions
    )

    # --------------------------------------------------------
    # STEP 6: SAVE QUESTION BANK
    # --------------------------------------------------------

    if valid_questions:

        save_question_bank(
            valid_questions,
            OUTPUT_FILE
        )

    else:

        print(
            "\n⚠️ Question bank was not saved "
            "because there are no valid questions."
        )

    # --------------------------------------------------------
    # COMPLETION
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("       QUESTION BANK GENERATION COMPLETED")
    print("=" * 60)


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    generate_question_bank()