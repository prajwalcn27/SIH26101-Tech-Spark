import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )

client = genai.Client(api_key=api_key)


def generate_mcqs(
    learning_material,
    number_of_questions=5
):
    """
    Generate MCQs from approved learning material
    using Google Gemini.

    The AI is instructed to use only the
    supplied learning material.
    """

    prompt = f"""
You are an AI learning assessment generator.

Use ONLY the learning material provided below.

Generate exactly {number_of_questions}
multiple-choice questions.

For every question provide:

1. question
2. options: exactly four options A, B, C, D
3. correct_answer: A, B, C, or D
4. explanation
5. topic
6. difficulty: Easy, Medium, or Hard

Rules:

- Every answer must be directly supported by
  the learning material.
- Do not use outside knowledge.
- Each question must have only one intended
  correct answer.
- Options must be meaningful and relevant.
- Avoid ambiguous questions.
- Avoid duplicate questions.
- Return valid JSON only.

Learning Material:
------------------
{learning_material}
------------------

Return this exact JSON structure:

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
            "explanation": "Explanation based only on the material",
            "topic": "Topic name",
            "difficulty": "Easy"
        }}
    ]
}}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    return json.loads(response.text)


if __name__ == "__main__":

    material_file = "sample_material.txt"

    with open(
        material_file,
        "r",
        encoding="utf-8"
    ) as file:

        material = file.read()

    result = generate_mcqs(
        material,
        5
    )

    print(
        "\n===== GENERATED 5 MCQs =====\n"
    )

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )