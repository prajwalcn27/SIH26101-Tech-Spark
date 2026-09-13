from mcq_generator import generate_mcqs
from validator import validate_mcq


# ============================================================
# SAMPLE LEARNING MATERIALS
# ============================================================

SAMPLE_TEXTS = {

    "Data Cleaning": """
Data cleaning is the process of detecting and correcting
inaccurate, incomplete, duplicate, or inconsistent data.

Common data cleaning techniques include handling missing values,
removing duplicate records, correcting inconsistent formats,
and identifying invalid values.

Data validation checks whether cleaned data satisfies
required rules and conditions.
""",

    "Decision Tree": """
A decision tree is a supervised machine learning algorithm
used for classification and regression.

A decision tree contains internal nodes, branches, and leaf
nodes. Internal nodes represent feature tests or decisions,
while leaf nodes represent the final prediction or outcome.

Decision trees make predictions by following decision rules
from the root node to a leaf node.
""",

    "Naive Bayes": """
Naive Bayes is a supervised machine learning classification
algorithm based on Bayes' theorem.

It assumes that features are conditionally independent
given the class.

Naive Bayes uses probability and conditional probability
to classify data into different classes.
"""
}


# ============================================================
# MULTIPLE SAMPLE TEST
# ============================================================

def run_multiple_sample_test():

    print("=" * 70)
    print("GEMINI MULTIPLE SAMPLE TEXT TEST")
    print("=" * 70)

    total_generated = 0
    valid_count = 0
    review_count = 0
    invalid_count = 0
    error_count = 0

    for topic, material in SAMPLE_TEXTS.items():

        print("\n" + "-" * 70)
        print(f"TESTING TOPIC: {topic}")
        print("-" * 70)

        try:

            # Current generate_mcqs() accepts:
            # material + number_of_questions
            mcq_result = generate_mcqs(
                material,
                5
            )

            if not mcq_result:

                print("No result returned from Gemini.")
                error_count += 1
                continue

            questions = mcq_result.get(
                "questions",
                []
            )

            if not questions:

                print("No questions generated.")
                error_count += 1
                continue

            print(
                f"Questions generated: "
                f"{len(questions)}"
            )

            total_generated += len(questions)

            # ------------------------------------------------
            # Validate generated questions
            # ------------------------------------------------

            for index, question in enumerate(
                questions,
                start=1
            ):

                validation = validate_mcq(
                    question,
                    material
                )

                status = validation.get(
                    "status",
                    "UNKNOWN"
                )

                confidence = validation.get(
                    "confidence",
                    0
                )

                print(
                    f"\nQuestion {index}"
                )

                print(
                    f"Status     : {status}"
                )

                print(
                    f"Confidence : {confidence}%"
                )

                print(
                    f"Topic      : "
                    f"{question.get('topic', 'N/A')}"
                )

                if validation.get("issues"):

                    print(
                        "Issues:"
                    )

                    for issue in validation["issues"]:

                        print(
                            f"  - {issue}"
                        )

                else:

                    print(
                        "Issues     : None"
                    )

                if status == "VALID":

                    valid_count += 1

                elif status == "REVIEW":

                    review_count += 1

                elif status == "INVALID":

                    invalid_count += 1

        except Exception as error:

            error_count += 1

            print(
                f"Gemini/API error: {error}"
            )

            print(
                "This sample could not be generated."
            )

            print(
                "The test will continue "
                "with the next sample."
            )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("FINAL TEST SUMMARY")
    print("=" * 70)

    print(
        f"Total questions generated : "
        f"{total_generated}"
    )

    print(
        f"VALID questions            : "
        f"{valid_count}"
    )

    print(
        f"REVIEW questions           : "
        f"{review_count}"
    )

    print(
        f"INVALID questions          : "
        f"{invalid_count}"
    )

    print(
        f"ERRORS                     : "
        f"{error_count}"
    )

    print("=" * 70)


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    run_multiple_sample_test()