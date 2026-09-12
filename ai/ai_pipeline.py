import json

from mcq_generator import generate_mcqs
from validator import validate_mcq


# ============================================================
# CONFIGURATION
# ============================================================

SAMPLE_MATERIAL_PATH = "sample_material.txt"

NUMBER_OF_QUESTIONS = 5

# True  = Use local MCQs (does not call Gemini)
# False = Use Gemini API
USE_MOCK_MODE = True

OUTPUT_FILE = "ai_pipeline_result.json"


# ============================================================
# LOCAL MOCK MCQs
# ============================================================

def get_mock_mcqs():

    return {
        "questions": [

            {
                "question": "What is the purpose of removing duplicate records?",
                "options": {
                    "A": "To improve data quality",
                    "B": "To increase missing values",
                    "C": "To create inconsistent data",
                    "D": "To remove all outliers"
                },
                "correct_answer": "A",
                "explanation": "Removing duplicate records helps improve data quality.",
                "topic": "Data Cleaning",
                "difficulty": "Easy"
            },

            {
                "question": "How can missing values be handled?",
                "options": {
                    "A": "Only by deleting the entire dataset",
                    "B": "By removing records or replacing values",
                    "C": "By creating duplicate records",
                    "D": "By ignoring all data validation"
                },
                "correct_answer": "B",
                "explanation": "Missing values can be handled by removing records, replacing values, or using statistical methods.",
                "topic": "Missing Values",
                "difficulty": "Easy"
            },

            {
                "question": "What should be done with outliers?",
                "options": {
                    "A": "They should always be deleted",
                    "B": "They should be examined carefully",
                    "C": "They should always be duplicated",
                    "D": "They should be ignored"
                },
                "correct_answer": "B",
                "explanation": "Outliers should be examined carefully because they may represent errors or genuine unusual observations.",
                "topic": "Outliers",
                "difficulty": "Medium"
            },

            {
                "question": "What does data validation check?",
                "options": {
                    "A": "Whether data follows predefined rules and constraints",
                    "B": "Whether data contains only duplicate records",
                    "C": "Whether all values are missing",
                    "D": "Whether data has no numerical values"
                },
                "correct_answer": "A",
                "explanation": "Data validation checks whether data follows predefined rules, formats, and constraints.",
                "topic": "Data Validation",
                "difficulty": "Easy"
            },

            {
                "question": "What may data preprocessing include?",
                "options": {
                    "A": "Only data deletion",
                    "B": "Data cleaning, transformation, and normalization",
                    "C": "Only duplicate creation",
                    "D": "Only data collection"
                },
                "correct_answer": "B",
                "explanation": "Data preprocessing may include data cleaning, transformation, and normalization before the data is used for analysis or machine learning.",
                "topic": "Data Preprocessing",
                "difficulty": "Medium"
            }

        ]
    }


# ============================================================
# MAIN AI PIPELINE
# ============================================================

def run_ai_pipeline():

    print("=" * 60)
    print("          SIH AI LEARNING PIPELINE")
    print("=" * 60)

    # --------------------------------------------------------
    # STEP 1: READ LEARNING MATERIAL
    # --------------------------------------------------------

    print("\n[STEP 1] Reading learning material...")
    print("-" * 60)

    try:

        with open(
            SAMPLE_MATERIAL_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            learning_material = file.read()

    except FileNotFoundError:

        print(
            f"ERROR: File not found: "
            f"{SAMPLE_MATERIAL_PATH}"
        )

        return

    if not learning_material.strip():

        print("ERROR: Learning material is empty.")

        return

    print("SUCCESS: Learning material loaded.")

    print(
        f"Characters extracted: "
        f"{len(learning_material)}"
    )

    # --------------------------------------------------------
    # STEP 2: GENERATE MCQs
    # --------------------------------------------------------

    print("\n[STEP 2] Generating MCQs...")
    print("-" * 60)

    if USE_MOCK_MODE:

        print(
            "MOCK MODE: Using local sample MCQs."
        )

        mcq_result = get_mock_mcqs()

    else:

        print(
            "GEMINI MODE: Generating MCQs using Gemini..."
        )

        try:

            mcq_result = generate_mcqs(
                learning_material,
                NUMBER_OF_QUESTIONS
            )

        except Exception as error:

            print(
                "ERROR: MCQ generation failed."
            )

            print(
                f"Details: {error}"
            )

            return

    # --------------------------------------------------------
    # CHECK MCQ RESULT
    # --------------------------------------------------------

    if not mcq_result:

        print(
            "ERROR: No MCQ result received."
        )

        return

    questions = mcq_result.get(
        "questions",
        []
    )

    if not questions:

        print(
            "ERROR: No questions were generated."
        )

        return

    print(
        f"SUCCESS: {len(questions)} MCQs generated."
    )

    # --------------------------------------------------------
    # STEP 3: DISPLAY GENERATED MCQs
    # --------------------------------------------------------

    print("\n[STEP 3] Generated MCQs")
    print("=" * 60)

    for index, question in enumerate(
        questions,
        start=1
    ):

        print(
            f"\nQuestion {index}:"
        )

        print(
            question.get(
                "question",
                "N/A"
            )
        )

        print("\nOptions:")

        options = question.get(
            "options",
            {}
        )

        for option in [
            "A",
            "B",
            "C",
            "D"
        ]:

            print(
                f"  {option}. "
                f"{options.get(option, 'N/A')}"
            )

        print(
            f"\nCorrect Answer: "
            f"{question.get('correct_answer', 'N/A')}"
        )

        print(
            f"Explanation: "
            f"{question.get('explanation', 'N/A')}"
        )

        print(
            f"Topic: "
            f"{question.get('topic', 'N/A')}"
        )

        print(
            f"Difficulty: "
            f"{question.get('difficulty', 'N/A')}"
        )

        print("-" * 60)

    # --------------------------------------------------------
    # STEP 4: VALIDATE MCQs
    # --------------------------------------------------------

    print("\n[STEP 4] Validating MCQs...")
    print("-" * 60)

    validation_results = []

    for index, question in enumerate(
        questions,
        start=1
    ):

        validation = validate_mcq(
            question,
            learning_material
        )

        validation_results.append(
            {
                "question_number": index,

                "question": question.get(
                    "question",
                    ""
                ),

                "validation": validation
            }
        )

    print(
        "SUCCESS: MCQ validation completed."
    )

    # --------------------------------------------------------
    # STEP 5: DISPLAY VALIDATION RESULTS
    # --------------------------------------------------------

    print("\n[STEP 5] Validation Results")
    print("=" * 60)

    valid_count = 0
    review_count = 0
    invalid_count = 0

    for result in validation_results:

        validation = result[
            "validation"
        ]

        status = validation.get(
            "status",
            "UNKNOWN"
        )

        confidence = validation.get(
            "confidence",
            0
        )

        source_support = validation.get(
            "source_support_percentage",
            0
        )

        print(
            f"\nQuestion "
            f"{result['question_number']}"
        )

        print(
            f"Status: {status}"
        )

        print(
            f"Confidence: {confidence}%"
        )

        print(
            f"Source Support: "
            f"{source_support}%"
        )

        print(
            f"Issues: "
            f"{validation.get('issues', [])}"
        )

        if status == "VALID":

            valid_count += 1

        elif status == "REVIEW":

            review_count += 1

        elif status == "INVALID":

            invalid_count += 1

    # --------------------------------------------------------
    # STEP 6: VALIDATION SUMMARY
    # --------------------------------------------------------

    print("\n[STEP 6] Validation Summary")
    print("=" * 60)

    print(
        f"Total Questions: "
        f"{len(questions)}"
    )

    print(
        f"VALID: {valid_count}"
    )

    print(
        f"REVIEW: {review_count}"
    )

    print(
        f"INVALID: {invalid_count}"
    )

    # --------------------------------------------------------
    # STEP 7: SAVE RESULT
    # --------------------------------------------------------

    final_result = {

        "source_file": SAMPLE_MATERIAL_PATH,

        "number_of_questions": len(
            questions
        ),

        "mcqs": questions,

        "validation": validation_results,

        "summary": {

            "total": len(questions),

            "valid": valid_count,

            "review": review_count,

            "invalid": invalid_count
        }
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            final_result,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nResult saved to: "
        f"{OUTPUT_FILE}"
    )

    print("\n" + "=" * 60)

    print(
        "       AI PIPELINE COMPLETED"
    )

    print("=" * 60)


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    run_ai_pipeline()