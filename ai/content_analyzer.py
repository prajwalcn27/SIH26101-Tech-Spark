import json
import os
import time

from google import genai
from google.genai import types
from dotenv import load_dotenv

from content_retriever import ContentRetriever


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "❌ GEMINI_API_KEY not found in .env file."
    )

client = genai.Client(
    api_key=api_key
)

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# CONTENT ANALYZER
# ============================================================

def analyze_content(
    topic,
    retrieved_content
):
    """
    Use Gemini to identify the most relevant learning
    content and concepts from retrieved source material.
    """

    if not retrieved_content:
        return None

    prompt = f"""
You are an educational content analysis system.

Your task is to analyze approved learning material
retrieved for a learner's topic.

Learner Topic:
{topic}

Retrieved Learning Material:
{retrieved_content}

IMPORTANT RULES:

1. Use ONLY the provided learning material.
2. Do not add outside knowledge.
3. Identify which sections are actually relevant to
   the learner topic.
4. Distinguish primary learning content from:
   - revision questions
   - duplicate content
   - unrelated content
   - administrative information
   - examples that are not directly relevant
5. Extract the important concepts present in the
   relevant material.
6. Keep concepts grounded in the source.
7. Do not invent concepts.
8. Identify the main learning points.
9. Return ONLY valid JSON.

Return exactly this structure:

{{
    "topic": "{topic}",
    "relevant_sections": [
        {{
            "section_id": 0,
            "relevance": "PRIMARY",
            "confidence": 0,
            "reason": "short explanation"
        }}
    ],
    "concepts": [
        {{
            "name": "concept name",
            "description": "source-grounded description"
        }}
    ],
    "learning_points": [
        "learning point 1",
        "learning point 2"
    ]
}}

Allowed relevance values:

PRIMARY
SUPPORTING
LOW
IRRELEVANT

Confidence must be between 0 and 100.
"""

    # ========================================================
    # GEMINI REQUEST WITH RETRY
    # ========================================================

    for attempt in range(3):

        try:

            response = client.models.generate_content(

                model=MODEL_NAME,

                contents=prompt,

                config=types.GenerateContentConfig(

                    response_mime_type="application/json"
                )
            )

            result = json.loads(
                response.text
            )

            return result

        except Exception as error:

            error_message = str(error)

            print(
                f"\n⚠️ Gemini error "
                f"(attempt {attempt + 1}/3):"
            )

            print(error_message)

            # ------------------------------------------------
            # Retry only for temporary service errors
            # ------------------------------------------------

            if "503" in error_message:

                if attempt < 2:

                    print(
                        "⏳ Temporary Gemini "
                        "service error. Retrying..."
                    )

                    time.sleep(5)

                    continue

            # ------------------------------------------------
            # Quota errors should not be retried repeatedly
            # ------------------------------------------------

            if "429" in error_message:

                print(
                    "\n❌ Gemini API quota/rate "
                    "limit reached."
                )

                print(
                    "Please wait for the quota "
                    "to reset."
                )

                return None

            return None

    return None


# ============================================================
# DISPLAY ANALYSIS
# ============================================================

def display_analysis(result):

    if not result:

        print(
            "\n❌ No analysis returned."
        )

        return

    print("\n" + "=" * 60)
    print("GEMINI CONTENT ANALYSIS")
    print("=" * 60)

    print(
        f"\n🎯 Topic: "
        f"{result.get('topic')}"
    )

    # --------------------------------------------------------
    # Relevant sections
    # --------------------------------------------------------

    print(
        "\n📚 RELEVANT SECTIONS"
    )

    print("-" * 60)

    for section in result.get(
        "relevant_sections",
        []
    ):

        print(
            f"Section: "
            f"{section.get('section_id')}"
        )

        print(
            f"Relevance: "
            f"{section.get('relevance')}"
        )

        print(
            f"Confidence: "
            f"{section.get('confidence')}%"
        )

        print(
            f"Reason: "
            f"{section.get('reason')}"
        )

        print()

    # --------------------------------------------------------
    # Concepts
    # --------------------------------------------------------

    print(
        "🧠 CONCEPTS"
    )

    print("-" * 60)

    for concept in result.get(
        "concepts",
        []
    ):

        print(
            f"\n• {concept.get('name')}"
        )

        print(
            f"  {concept.get('description')}"
        )

    # --------------------------------------------------------
    # Learning points
    # --------------------------------------------------------

    print(
        "\n📌 LEARNING POINTS"
    )

    print("-" * 60)

    for point in result.get(
        "learning_points",
        []
    ):

        print(
            f"• {point}"
        )

    print("\n" + "=" * 60)


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("             CONTENT ANALYZER")
    print("=" * 60)

    try:

        # ----------------------------------------------------
        # Load retriever
        # ----------------------------------------------------

        retriever = ContentRetriever(
            "content_index.json"
        )

        # ----------------------------------------------------
        # Test topic
        # ----------------------------------------------------

        topic = "Decision Tree"

        print(
            f"\n🔎 Searching material for: "
            f"{topic}"
        )

        retrieved = (
            retriever.get_relevant_content(
                topic,
                top_k=3,
                max_words=1200
            )
        )

        if not retrieved:

            print(
                "\n❌ No content retrieved."
            )

            exit()

        # ----------------------------------------------------
        # Get combined source material
        # ----------------------------------------------------

        source_text = retrieved.get(
            "combined_text",
            ""
        )

        print(
            f"\n📄 Retrieved approximately "
            f"{len(source_text.split())} words."
        )

        # ----------------------------------------------------
        # Analyze using Gemini
        # ----------------------------------------------------

        print(
            "\n🤖 Sending candidate content "
            "to Gemini..."
        )

        result = analyze_content(
            topic,
            source_text
        )

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        display_analysis(
            result
        )

        # ----------------------------------------------------
        # Save result
        # ----------------------------------------------------

        if result:

            output_file = (
                "content_analysis.json"
            )

            with open(
                output_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    result,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print(
                f"\n📁 Analysis saved as: "
                f"{output_file}"
            )

    except Exception as error:

        print(
            "\n❌ Error:"
        )

        print(error)

    print("\n" + "=" * 60)
    print(
        "✅ CONTENT ANALYZER COMPLETED!"
    )
    print("=" * 60)