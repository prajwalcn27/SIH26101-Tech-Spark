from validator import validate_mcq


SOURCE_TEXT = """
Data cleaning is the process of detecting and correcting inaccurate,
incomplete, duplicate, or inconsistent data.

Common data cleaning techniques include handling missing values,
removing duplicate records, correcting inconsistent formats,
and identifying invalid values.

Data validation is used to check whether data follows the required
rules and constraints.
"""


TEST_CASES = {

    "VALID QUESTION": {
        "question": "What is the main purpose of data cleaning?",
        "options": {
            "A": "To detect and correct inaccurate data",
            "B": "To create computer networks",
            "C": "To design websites",
            "D": "To install operating systems"
        },
        "correct_answer": "A",
        "explanation": "Data cleaning detects and corrects inaccurate, incomplete, duplicate, or inconsistent data.",
        "topic": "Data Cleaning",
        "difficulty": "Easy"
    },

    "MISSING CORRECT ANSWER": {
        "question": "What is the main purpose of data cleaning?",
        "options": {
            "A": "To detect and correct inaccurate data",
            "B": "To create computer networks",
            "C": "To design websites",
            "D": "To install operating systems"
        },
        "correct_answer": "",
        "explanation": "Data cleaning improves data quality.",
        "topic": "Data Cleaning",
        "difficulty": "Easy"
    },

    "DUPLICATE OPTIONS": {
        "question": "What is data validation?",
        "options": {
            "A": "Checking whether data follows required rules",
            "B": "Checking whether data follows required rules",
            "C": "Creating a database",
            "D": "Designing a website"
        },
        "correct_answer": "A",
        "explanation": "Data validation checks whether data follows required rules and constraints.",
        "topic": "Data Cleaning",
        "difficulty": "Easy"
    },

    "INVALID OPTION COUNT": {
        "question": "What is data cleaning?",
        "options": {
            "A": "Correcting inaccurate data",
            "B": "Removing duplicate data",
            "C": "Designing websites"
        },
        "correct_answer": "A",
        "explanation": "Data cleaning improves the quality of data.",
        "topic": "Data Cleaning",
        "difficulty": "Easy"
    },

    "UNSUPPORTED ANSWER": {
        "question": "What is data validation?",
        "options": {
            "A": "Creating a website",
            "B": "Checking data rules",
            "C": "Removing hardware",
            "D": "Installing software"
        },
        "correct_answer": "E",
        "explanation": "Data validation checks data against rules.",
        "topic": "Data Cleaning",
        "difficulty": "Easy"
    },

    "MISSING TOPIC": {
        "question": "What is data validation?",
        "options": {
            "A": "Checking whether data follows required rules",
            "B": "Creating a website",
            "C": "Installing software",
            "D": "Creating a network"
        },
        "correct_answer": "A",
        "explanation": "Data validation checks whether data follows required rules.",
        "topic": "",
        "difficulty": "Easy"
    },

    "AMBIGUOUS QUESTION": {
        "question": "Which one is correct?",
        "options": {
            "A": "Data cleaning",
            "B": "Data validation",
            "C": "Database",
            "D": "Website"
        },
        "correct_answer": "A",
        "explanation": "The question is too vague because it does not clearly identify what is being asked.",
        "topic": "Data Cleaning",
        "difficulty": "Easy"
    }
}


def run_tests():

    print("=" * 70)
    print("MALFORMED / AMBIGUOUS MCQ VALIDATION TEST")
    print("=" * 70)

    valid_count = 0
    review_count = 0
    invalid_count = 0
    error_count = 0

    for test_name, question in TEST_CASES.items():

        print("\n" + "-" * 70)
        print(test_name)
        print("-" * 70)

        try:

            # Your current validator accepts the question object
            # as the first argument.
            result = validate_mcq(question, SOURCE_TEXT)

            status = str(result.get("status", "UNKNOWN")).upper()
            confidence = result.get("confidence", 0)
            issues = result.get("issues", [])

            print(f"Status     : {status}")
            print(f"Confidence : {confidence}%")

            if issues:
                print("Issues:")
                for issue in issues:
                    print(f"  - {issue}")
            else:
                print("Issues     : None")

            if status == "VALID":
                valid_count += 1

            elif status == "REVIEW":
                review_count += 1

            elif status == "INVALID":
                invalid_count += 1

            else:
                print("Warning    : Unknown validator status")

        except Exception as error:

            error_count += 1
            print(f"Validator error: {error}")

    print("\n" + "=" * 70)
    print("FINAL VALIDATION SUMMARY")
    print("=" * 70)

    print(f"VALID questions   : {valid_count}")
    print(f"REVIEW questions  : {review_count}")
    print(f"INVALID questions : {invalid_count}")
    print(f"ERRORS            : {error_count}")

    print("=" * 70)
    print("VALIDATION TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()