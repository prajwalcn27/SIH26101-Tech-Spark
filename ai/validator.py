import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def validate_mcqs(learning_material, mcqs):

    prompt = f"""
You are an AI question validator.

Your task is to validate the following multiple-choice questions
using ONLY the provided learning material.

DO NOT use outside knowledge.

LEARNING MATERIAL:
{learning_material}

MCQs:
{json.dumps(mcqs, indent=2)}

For every question, check:

1. Is the correct answer supported by the learning material?
2. Does the question topic match the learning material?
3. Is there exactly one correct answer?
4. Are all four options meaningful?
5. Is the question clear and grammatically correct?
6. Is it a duplicate of another question?
7. Is the difficulty appropriate?
8. Give confidence from 0 to 100.
9. Make sure no outside knowledge was used.

Status rules:

VALID = clearly supported by the material
REVIEW = uncertain or needs human checking
INVALID = incorrect or unsupported

Return ONLY valid JSON.

Required format:

{{
    "validation_results": [
        {{
            "question_number": 1,
            "status": "VALID",
            "confidence": 95,
            "answer_supported": true,
            "topic_match": true,
            "single_correct_answer": true,
            "options_meaningful": true,
            "grammar_clear": true,
            "duplicate": false,
            "difficulty_appropriate": true,
            "reason": "Short explanation"
        }}
    ]
}}
"""

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:
            print(f"Validation attempt {attempt}/{max_attempts}...")

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            result = json.loads(response.text)

            print("✅ MCQ validation successful!")

            return result

        except Exception as e:

            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < max_attempts:
                    print("⚠️ Gemini server is busy.")
                    print("⏳ Waiting 5 seconds before retrying...")
                    time.sleep(5)

                else:
                    print("❌ Gemini is still busy after 3 attempts.")
                    return None

            else:
                print("❌ MCQ validation error:")
                print(e)
                return None


if __name__ == "__main__":

    sample_material = """
    Data cleaning is the process of identifying, correcting,
    removing, or replacing incorrect, incomplete, duplicate,
    and inconsistent data.

    Missing values are values that are not present in a dataset.

    Duplicate records are repeated records in a dataset.

    Data validation checks whether data meets predefined rules
    and requirements.
    """

    sample_mcqs = [
        {
            "question": "What is data cleaning?",
            "options": {
                "A": "Creating a database",
                "B": "Identifying and correcting incorrect or incomplete data",
                "C": "Deleting all data",
                "D": "Creating charts"
            },
            "correct_answer": "B",
            "explanation": "Data cleaning identifies and corrects incorrect or incomplete data.",
            "topic": "Data Cleaning",
            "difficulty": "Easy"
        }
    ]

    print("Validating MCQs...")
    print("----------------------------------------")

    result = validate_mcqs(sample_material, sample_mcqs)

    if result:
        print(json.dumps(result, indent=2))