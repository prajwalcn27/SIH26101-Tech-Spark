import json
import os

from pdf_reader import extract_text_from_pdf
from mcq_generator import generate_mcqs
from validator import validate_mcqs


# ============================================================
# CONFIGURATION
# ============================================================

PDF_PATH = "../learning_materials/ML_Module1.pdf"

NUMBER_OF_QUESTIONS = 5


# ============================================================
# MAIN AI PIPELINE
# ============================================================

def run_ai_pipeline():

    print("=" * 60)
    print("              SIH AI LEARNING PIPELINE")
    print("=" * 60)

    # --------------------------------------------------------
    # STEP 1: READ PDF
    # --------------------------------------------------------

    print("\n📄 Step 1: Reading learning material...")
    print("-" * 60)

    learning_material = extract_text_from_pdf(PDF_PATH)

    if not learning_material:
        print("❌ Could not extract text from PDF.")
        return

    print("✅ PDF text extracted successfully!")

    # --------------------------------------------------------
    # STEP 2: DISPLAY INFORMATION
    # --------------------------------------------------------

    print("\n📊 Extracted material information:")
    print(f"Characters extracted: {len(learning_material)}")
    print(f"Words approximately: {len(learning_material.split())}")

    # --------------------------------------------------------
    # STEP 3: GENERATE MCQs
    # --------------------------------------------------------

    print("\n🤖 Step 2: Generating MCQs...")
    print("-" * 60)

    mcqs = generate_mcqs(
        learning_material,
        number_of_questions=NUMBER_OF_QUESTIONS
    )

    if not mcqs:
        print("❌ MCQ generation failed.")
        return

    print("✅ MCQs generated successfully!")

    # --------------------------------------------------------
    # STEP 4: DISPLAY GENERATED MCQs
    # --------------------------------------------------------

    print("\n📝 Generated MCQs")
    print("=" * 60)

    print(
        json.dumps(
            mcqs,
            indent=4,
            ensure_ascii=False
        )
    )

    # --------------------------------------------------------
    # STEP 5: VALIDATE MCQs
    # --------------------------------------------------------

    print("\n🔍 Step 3: Validating MCQs...")
    print("-" * 60)

    validation_results = validate_mcqs(
        learning_material,
        mcqs
    )

    if not validation_results:
        print("❌ MCQ validation failed.")
        return

    print("✅ MCQ validation completed!")

    # --------------------------------------------------------
    # STEP 6: DISPLAY VALIDATION RESULTS
    # --------------------------------------------------------

    print("\n📋 Validation Results")
    print("=" * 60)

    print(
        json.dumps(
            validation_results,
            indent=4,
            ensure_ascii=False
        )
    )

    # --------------------------------------------------------
    # STEP 7: SAVE COMPLETE RESULT
    # --------------------------------------------------------

    final_result = {
        "source_file": PDF_PATH,
        "number_of_questions": NUMBER_OF_QUESTIONS,
        "mcqs": mcqs,
        "validation": validation_results
    }

    output_file = "ai_pipeline_result.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            final_result,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 60)
    print("✅ AI PIPELINE COMPLETED!")
    print(f"📁 Result saved as: {output_file}")
    print("=" * 60)


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    run_ai_pipeline()