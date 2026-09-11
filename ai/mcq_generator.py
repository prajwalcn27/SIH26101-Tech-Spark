import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ---------------------------------------
# LOAD API KEY
# ---------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env")
    exit()


# ---------------------------------------
# CREATE GEMINI CLIENT
# ---------------------------------------

client = genai.Client(api_key=api_key)


# ---------------------------------------
# MCQ GENERATOR
# ---------------------------------------

def generate_mcqs(learning_material, number_of_questions=5):

    prompt = f"""
You are an AI learning assistant for the SIH26101
AI-enabled learning platform.

Generate exactly {number_of_questions} multiple-choice
questions using ONLY the learning material provided below.

RULES:

1. Use ONLY information from the learning material.
2. Do not use outside knowledge.
3. Each question must have exactly 4 options.
4. There must be exactly ONE correct answer.
5. Include a short explanation.
6. Include the topic.
7. Difficulty must be Easy, Medium, or Hard.
8. Do not create duplicate questions.
9. Questions should test understanding where possible.
10. Do not invent information.

Return ONLY valid JSON.

Format:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            }},
            "correct_answer": "A",
            "explanation": "Explanation",
            "topic": "Topic",
            "difficulty": "Easy"
        }}
    ]
}}

LEARNING MATERIAL:

{learning_material}
"""

    # ---------------------------------------
    # RETRY SETTINGS
    # ---------------------------------------

    max_retries = 3

    for attempt in range(1, max_retries + 1):

        try:

            print(
                f"Gemini request attempt {attempt}/{max_retries}..."
            )

            response = client.models.generate_content(

                model="gemini-3.6-flash",

                contents=prompt,

                config=types.GenerateContentConfig(

                    response_mime_type="application/json"

                )
            )

            result = json.loads(response.text)

            return result


        except Exception as e:

            error_message = str(e)

            print()
            print("❌ Gemini error:")
            print(error_message)

            # ---------------------------------------
            # RETRY 503
            # ---------------------------------------

            if "503" in error_message:

                if attempt < max_retries:

                    print()
                    print(
                        "⚠️ Gemini server is temporarily busy."
                    )

                    print(
                        "Waiting 5 seconds before retry..."
                    )

                    time.sleep(5)

                    continue

                else:

                    print()
                    print(
                        "❌ Gemini is still unavailable "
                        "after multiple attempts."
                    )

                    return None

            else:

                return None

    return None


# ---------------------------------------
# TEST
# ---------------------------------------

if __name__ == "__main__":

    learning_material = """
    Data cleaning is the process of identifying and correcting
    incorrect, incomplete, duplicate, or inconsistent data.

    Missing values occur when some data fields do not contain
    a value. Missing values can be handled by removing records
    or replacing missing values with appropriate values.

    Duplicate records are repeated records in a dataset.
    Removing duplicate records helps improve data quality.

    Data validation checks whether data follows predefined
    rules and formats.
    """

    print()
    print("Generating MCQs...")
    print("----------------------------------------")

    result = generate_mcqs(
        learning_material,
        5
    )

    if result:

        print()
        print("✅ MCQs generated successfully!")
        print()

        print(
            json.dumps(
                result,
                indent=4,
                ensure_ascii=False
            )
        )

    else:

        print()
        print("❌ MCQ generation failed.")