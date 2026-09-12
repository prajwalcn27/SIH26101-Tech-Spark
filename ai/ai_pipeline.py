import json

from mcq_generator import generate_mcqs
from validator import validate_mcq


# ============================================================
# CONFIGURATION
# ============================================================

SAMPLE_MATERIAL_PATH = "sample_material.txt"

NUMBER_OF_QUESTIONS = 5

OUTPUT_FILE = "ai_pipeline_result.json"


# ============================================================
# MAIN AI PIPELINE
# ============================================================

def run_ai_pipeline():

    print("=" * 60)
    print("          SIH AI LEARNING PIPELINE")
    print("=" * 60)

    # --------------------------------------------------------
    # STEP 1: READ SAMPLE LEARNING MATERIAL
    # --------------------------------------------------------

    print("\n📄 Step 1: Reading learning material...")
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
            f"❌ File not found: "
            f"{SAMPLE_MATERIAL_PATH}"
        )

        return

    if not learning_material.strip():

        print("❌ Learning material is empty.")
        return

    print("✅ Learning material loaded successfully.")

    print(
        f"Characters extracted: "
        f"{len(learning_material)}"
    )

    # --------------------------------------------------------
    # STEP 2: GENERATE MCQs
    # --------------------------------------------------------

    print("\n🤖 Step 2: Generating MCQs...")
    print("-" * 60)

    mcqs = generate_mcqs(
        learning_material,
        NUMBER_OF_QUESTIONS
    )

    if not mcqs:

        print("❌ MCQ generation failed.")
        return

    questions = mcqs.get(
        "questions",
        []
    )

    if not questions:

        print("❌ No questions were generated.")
        return

    print(
        f"✅ {len(questions)} MCQs generated successfully!"
    )

    # --------------------------------------------------------
    # STEP 3: DISPLAY GENERATED MCQs
    # --------------------------------------------------------

    print("\n📝 Generated MCQs")
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

        for option in ["A", "B", "C", "D"]:

            print(
                f"  {option}. "
                f"{options.get(option, 'N/A')}"
            )

        print(
            f"\nCorrect Answer : "
            f"{question.get('correct_answer', 'N/A')}"
        )

        print(
            f"Explanation    : "
            f"{question.get('explanation', 'N/A')}"
        )

        print(
            f"Topic          : "
            f"{question.get('topic', 'N/A')}"
        )

        print(
            f"Difficulty     : "
            f"{question.get('difficulty', 'N/A')}"
        )

        print("-" * 60)

    # --------------------------------------------------------
    # STEP 4: VALIDATE MCQs
    # --------------------------------------------------------

    print("\n🔍 Step 3: Validating MCQs...")
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

        validation_results.append({

            "question_number": index,

            "question": question.get(
                "question",
                ""
            ),

            "validation": validation
        })

    print(
        "✅ MCQ validation completed!"
    )

    # --------------------------------------------------------
    # STEP 5: DISPLAY VALIDATION RESULTS
    # --------------------------------------------------------

    print("\n📋 Validation Results")
    print("=" * 60)

    valid_count = 0
    review_count = 0
    invalid_count = 0

    for result in validation_results:

        validation = result["validation"]

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
            f"Status         : {status}"
        )

        print(
            f"Confidence     : {confidence}%"
        )

        print(
            f"Source Support : "
            f"{source_support}%"
        )

        print(
            f"Issues         : "
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

    print("\n📊 Validation Summary")
    print("=" * 60)

    print(
        f"Total Questions : "
        f"{len(questions)}"
    )

    print(
        f"VALID           : "
        f"{valid_count}"
    )

    print(
        f"REVIEW          : "
        f"{review_count}"
    )

    print(
        f"INVALID         : "
        f"{invalid_count}"
    )

    # --------------------------------------------------------
    # STEP 7: SAVE COMPLETE RESULT
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
        f"\n💾 Result saved to: "
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