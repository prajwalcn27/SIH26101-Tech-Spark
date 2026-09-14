import json
import os
import re
import urllib.request
import urllib.error

from question_manager import QuestionManager

from assessment_engine import (
    AssessmentEngine,
    display_results as display_assessment_results
)

from gap_analyzer import GapAnalyzer

from recommendation_engine import RecommendationEngine

from quiz_manager import QuizManager

from quiz_result_analyzer import QuizResultAnalyzer

from competency_updater import CompetencyUpdater


def generate_ai_quiz_from_material(material_text, topic=None, num_questions=5):
    """
    Generate source-grounded MCQs from uploaded material using Gemini.
    Returns the same question structure used by QuizManager.
    Falls back to [] when Gemini is not configured or generation fails.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key or not material_text:
        return []

    topic_text = topic or "the selected learning topic"
    prompt = f"""
You are an educational assessment generator for the Tech Spark learning platform.

Create exactly {num_questions} multiple-choice questions from ONLY the source material below.
Focus on: {topic_text}.

Rules:
- 4 options per question.
- Exactly one correct answer.
- Questions must be directly supported by the source.
- Do not use outside facts.
- Mix understanding, application, and scenario questions.
- Return ONLY valid JSON, no markdown.

JSON format:
[
  {{
    "id": "ai_1",
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "correct_answer": "A",
    "topic": "{topic_text}"
  }}
]

SOURCE MATERIAL:
{material_text[:30000]}
"""

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }).encode("utf-8")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.0-flash:generateContent?key=" + api_key
    )

    try:
        request = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        raw = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw).strip()

        questions = json.loads(raw)

        if not isinstance(questions, list):
            return []

        cleaned = []
        for i, q in enumerate(questions[:num_questions], start=1):
            options = q.get("options", [])
            if not q.get("question") or len(options) != 4:
                continue

            correct = str(q.get("correct_answer", "A")).upper()
            if correct not in ("A", "B", "C", "D"):
                correct = "A"

            cleaned.append({
                "id": q.get("id", f"ai_{i}"),
                "question": q["question"],
                "options": options,
                "correct_answer": correct,
                "topic": q.get("topic", topic_text)
            })

        return cleaned if len(cleaned) == num_questions else []

    except Exception as error:
        print(f"âš ï¸ Gemini quiz generation failed: {error}")
        return []



def run_complete_learning_cycle(weak_topics=None, num_questions=5, material_text=None, material_title=None):


    if weak_topics is None:
        weak_topics = []

    print("=" * 70)
    print("              COMPLETE LEARNING CYCLE")
    print("=" * 70)

   

    # ==========================================================
    # STEP 1: QUESTION MANAGER
    # ==========================================================

    print("\nðŸ“š STEP 1: Loading Question Manager...")

    question_manager = QuestionManager()

    question_manager.remove_duplicates()

    # Use weak topics when provided.
    # Some competency gaps can be sub-topics of a broader topic.
    # Example: "Missing Values" is covered under "Data Cleaning"
    # in the current question bank.
    if weak_topics:
        assessment_questions = []

        related_topic_map = {
            "missing values": "Data Cleaning",
            "duplicate records": "Data Cleaning",
            "data formatting": "Data Cleaning",
            "data validation": "Data Cleaning",
        }

        for topic in weak_topics:
            topic = str(topic).strip()

            # 1. Try an exact topic match first.
            topic_questions = question_manager.get_questions(
                topic=topic,
                number_of_questions=num_questions
            )

            # 2. If there is no exact match, try the broader
            #    topic that contains the competency gap.
            if not topic_questions:
                mapped_topic = related_topic_map.get(topic.lower())

                if mapped_topic:
                    print(
                        f"   ðŸ”— '{topic}' mapped to "
                        f"'{mapped_topic}'"
                    )

                    topic_questions = question_manager.get_questions(
                        topic=mapped_topic,
                        number_of_questions=num_questions
                    )

            assessment_questions.extend(topic_questions)

        # Remove duplicates while preserving question order.
        unique_questions = {}
        for question in assessment_questions:
            unique_questions[question.get("id")] = question

        assessment_questions = list(unique_questions.values())

        # Keep the requested assessment size.
        assessment_questions = assessment_questions[:num_questions]

    else:
        assessment_questions = question_manager.get_random_questions(
            number_of_questions=num_questions
        )

    if not assessment_questions:

        print("âŒ No assessment questions available.")

        return None

    print(
        f"âœ… Loaded {len(question_manager.questions)} "
        f"questions from question bank."
    )

    print(
        f"âœ… Selected {len(assessment_questions)} "
        f"assessment questions."
    )

    # ==========================================================
    # STEP 2: INITIAL ASSESSMENT
    # ==========================================================

    print("\nðŸ“ STEP 2: Initial Assessment...")

    # Demo employee answers.
    # Later these answers will come from the frontend.

    demo_answers = {
        "1": "B",
        "2": "A",
        "3": "A",
        "4": "C",
        "5": "B",
        "6": "D"
    }

    assessment_answers = {}

    for index, question in enumerate(
        assessment_questions,
        start=1
    ):

        question_id = str(
            question.get("id", "")
        )

        # First try actual question ID.
        if question_id in demo_answers:

            assessment_answers[question_id] = (
                demo_answers[question_id]
            )

        # Otherwise use question number.
        else:

            question_number = str(index)

            assessment_answers[question_id] = (
                demo_answers.get(
                    question_number,
                    ""
                )
            )

    assessment_engine = AssessmentEngine()

    assessment_results = (
        assessment_engine.calculate_results(
            assessment_questions,
            assessment_answers
        )
    )

    if not assessment_results:

        print(
            "âŒ Assessment calculation failed."
        )

        return None

    display_assessment_results(
        assessment_results
    )

    # ==========================================================
    # STEP 3: COMPETENCY GAP ANALYSIS
    # ==========================================================

    print(
        "\nðŸ” STEP 3: Competency "
        "Gap Analysis..."
    )

    competency_scores = {}

    for topic, data in (
        assessment_results[
            "topic_scores"
        ].items()
    ):

        competency_scores[topic] = (
            data["percentage"]
        )

    gap_analyzer = GapAnalyzer(
        gap_threshold=60
    )

    gap_analysis = gap_analyzer.analyze(
        competency_scores
    )

    print(
        "\nðŸ“Œ IDENTIFIED COMPETENCY GAPS"
    )

    for result in (
        gap_analysis[
            "competency_results"
        ]
    ):

        print(
            f"ðŸ“˜ {result['topic']:<20} "
            f"{result['score']}% â†’ "
            f"{result['status']} "
            f"[{result['priority']}]"
        )

    print("\nâš ï¸ Weak Topics:")

    if gap_analysis["weak_topics"]:

        for topic in (
            gap_analysis[
                "weak_topics"
            ]
        ):

            print(
                f"   â€¢ {topic}"
            )

    else:

        print(
            "   âœ… No weak topics found."
        )

    # ==========================================================
    # STEP 4: PERSONALIZED LEARNING RECOMMENDATION
    # ==========================================================

    print(
        "\nðŸŽ¯ STEP 4: Personalized "
        "Learning Recommendation..."
    )

    recommendation_engine = (
        RecommendationEngine()
    )

    recommendations = (
        recommendation_engine
        .generate_recommendations(
            gap_analysis[
                "competency_results"
            ],
            top_k=2
        )
    )

    print(
        "\nðŸ“š RECOMMENDED MATERIAL"
    )

    if recommendations:

        for recommendation in (
            recommendations
        ):

            print(
                f"\nðŸ“˜ Topic: "
                f"{recommendation['topic']}"
            )

            print(
                f"   Gap Level: "
                f"{recommendation['gap_level']}"
            )

            print(
                f"   Current Score: "
                f"{recommendation['current_score']}"
            )

            materials = (
                recommendation.get(
                    "recommended_materials",
                    []
                )
            )

            if not materials:

                print(
                    "   No matching learning "
                    "material found."
                )

                continue

            for material in materials:

                print(
                    f"   Section ID: "
                    f"{material['section_id']}"
                )

                print(
                    f"   Pages: "
                    f"{material['pages']}"
                )

                print(
                    f"   Relevance Score: "
                    f"{material['relevance_score']}"
                )

    else:

        print(
            "   â„¹ï¸ No recommendations."
        )

    # ==========================================================
    # STEP 5: TARGETED QUIZ
    # ==========================================================

    print(
        "\nðŸ“ STEP 5: Creating "
        "Targeted Quiz..."
    )

    quiz_manager = QuizManager(
        question_manager
    )

    # If an uploaded material is supplied, generate a quiz directly
    # from that source material. Existing question-bank behavior remains
    # as the fallback for the current prototype flow.
    ai_target_topic = None
    if weak_topics:
        ai_target_topic = str(weak_topics[0]).strip()

    targeted_quiz = []
    if material_text:
        print("\nðŸ¤– Generating source-grounded AI quiz from uploaded material...")
        targeted_quiz = generate_ai_quiz_from_material(
            material_text=material_text,
            topic=ai_target_topic,
            num_questions=num_questions
        )
        if targeted_quiz:
            target_topic = ai_target_topic or material_title or "Uploaded Material"
            print(f"âœ… AI generated {len(targeted_quiz)} questions.")
        else:
            print("âš ï¸ AI generation unavailable. Using existing question bank.")

    weak_topics = (
        gap_analysis[
            "weak_topics"
        ]
    )

    target_topic = None

    if not targeted_quiz and weak_topics:

        # ------------------------------------------------------
        # Select the weakest topic based on lowest score.
        # ------------------------------------------------------

        weak_topic_results = [

            result

            for result in (
                gap_analysis[
                    "competency_results"
                ]
            )

            if result["topic"]
            in weak_topics
        ]

        weak_topic_results.sort(
            key=lambda item: item["score"]
        )

        target_topic = (
            weak_topic_results[0]["topic"]
        )

        print(
            f"\nðŸŽ¯ Target Topic: "
            f"{target_topic}"
        )

        targeted_quiz = (
            quiz_manager.create_targeted_quiz(
                topic=target_topic,
                number_of_questions=num_questions
            )
        )

        # If the gap analyzer returns a sub-topic that does not have
        # its own questions, use the broader topic from the question bank.
        if not targeted_quiz:
            related_topic_map = {
                "missing values": "Data Cleaning",
                "duplicate records": "Data Cleaning",
                "data formatting": "Data Cleaning",
                "data validation": "Data Cleaning",
            }

            mapped_topic = related_topic_map.get(
                str(target_topic).strip().lower()
            )

            if mapped_topic:
                print(
                    f"   ðŸ”— Target quiz '{target_topic}' "
                    f"mapped to '{mapped_topic}'"
                )

                target_topic = mapped_topic

                targeted_quiz = (
                    quiz_manager.create_targeted_quiz(
                        topic=target_topic,
                        number_of_questions=num_questions
                    )
                )

    elif not targeted_quiz:

        targeted_quiz = (
            quiz_manager.create_quiz(
                number_of_questions=num_questions
            )
        )

    if not targeted_quiz:

        print(
            "âŒ Could not create targeted quiz."
        )

        return None

    quiz_manager.display_quiz(
        targeted_quiz
    )

    # ==========================================================
    # STEP 6: QUIZ ATTEMPT
    # ==========================================================

    print(
        "\nâœï¸ STEP 6: Processing "
        "Quiz Attempt..."
    )

    # ----------------------------------------------------------
    # Demo employee answers all questions correctly.
    #
    # Later these answers will come from the frontend.
    # ----------------------------------------------------------

    quiz_answers = {}

    for question in targeted_quiz:

        question_id = str(
            question.get("id", "")
        )

        quiz_answers[question_id] = (
            question.get(
                "correct_answer",
                ""
            )
        )

    print(
        "âœ… Employee quiz answers received."
    )

    # ==========================================================
    # STEP 7: QUIZ RESULT ANALYSIS
    # ==========================================================

    print(
        "\nðŸ“Š STEP 7: Analyzing "
        "Quiz Result..."
    )

    quiz_analyzer = QuizResultAnalyzer()

    quiz_results = quiz_analyzer.analyze(
        targeted_quiz,
        quiz_answers
    )

    if (
        not quiz_results
        or quiz_results.get("status")
        != "success"
    ):

        print(
            "âŒ Quiz result analysis failed."
        )

        return None

    print(
        "\n==================================="
    )

    print(
        "          QUIZ RESULT"
    )

    print(
        "==================================="
    )

    print(
        f"Score: "
        f"{quiz_results['score_percentage']}%"
    )

    print(
        f"Correct Answers: "
        f"{quiz_results['correct_answers']}"
    )

    print(
        f"Wrong Answers: "
        f"{quiz_results['wrong_answers']}"
    )

    print(
        f"Weak Topics: "
        f"{quiz_results['weak_topics']}"
    )

    # ==========================================================
    # STEP 8: COMPETENCY UPDATE
    # ==========================================================

    print(
        "\nðŸ”„ STEP 8: Updating "
        "Employee Competency..."
    )

    previous_scores = (
        competency_scores.copy()
    )

    # ----------------------------------------------------------
    # Convert QuizResultAnalyzer format:
    #
    # topic_analysis
    #
    # into CompetencyUpdater format.
    # ----------------------------------------------------------

    competency_quiz_results = {}

    for topic, data in (
        quiz_results[
            "topic_analysis"
        ].items()
    ):

        competency_quiz_results[topic] = {

            "percentage":
                data["percentage"]

        }

    competency_updater = (
        CompetencyUpdater(
            learning_weight=0.6
        )
    )

    updated_competency = (
        competency_updater.update_competency(
            previous_scores,
            competency_quiz_results
        )
    )

    print(
        "\nðŸ“ˆ UPDATED COMPETENCY PROFILE"
    )

    for topic, data in (
        updated_competency[
            "updated_competencies"
        ].items()
    ):

        print(
            f"\nðŸ“˜ {topic}"
        )

        print(
            f"   Previous : "
            f"{data['previous_score']}%"
        )

        if data["quiz_score"] is not None:

            print(
                f"   Quiz     : "
                f"{data['quiz_score']}%"
            )

        print(
            f"   Updated  : "
            f"{data['updated_score']}%"
        )

        print(
            f"   Status   : "
            f"{data['status']}"
        )

    # ==========================================================
    # STEP 9: FINAL LEARNING PROFILE
    # ==========================================================

    print(
        "\nðŸ’¾ STEP 9: Creating "
        "Final Learning Profile..."
    )

    final_result = {

        "assessment": {

            "questions":
                assessment_questions,

            "answers":
                assessment_answers,

            "results":
                assessment_results
        },

        "gap_analysis":
            gap_analysis,

        "recommendations":
            recommendations,

        "targeted_quiz": {

            "topic":
                target_topic,

            "questions":
                targeted_quiz,

            "answers":
                quiz_answers,

            "results":
                quiz_results
        },

        "updated_competency":
            updated_competency
    }

    # ----------------------------------------------------------
    # Save final result
    # ----------------------------------------------------------

    output_file = (
        "complete_learning_cycle_result.json"
    )

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

    print(
        f"\nðŸ’¾ Final learning profile saved to:"
        f"\n   {output_file}"
    )

    # ==========================================================
    # COMPLETE
    # ==========================================================

    print("\n")

    print(
        "=" * 70
    )

    print(
        "          COMPLETE LEARNING CYCLE FINISHED"
    )

    print(
        "=" * 70
    )

    print(
        "\nâœ… Question selection"
    )

    print(
        "âœ… Initial assessment"
    )

    print(
        "âœ… Competency gap analysis"
    )

    print(
        "âœ… Personalized recommendation"
    )

    print(
        "âœ… Targeted quiz"
    )

    print(
        "âœ… Quiz result analysis"
    )

    print(
        "âœ… Competency update"
    )

    print(
        "âœ… Final learning profile"
    )

    print(
        "\nðŸš€ AI LEARNING LOOP COMPLETED!"
    )

    # ==========================================================
    # IMPORTANT:
    # Return result to Flask API
    # ==========================================================

    return final_result


# ==============================================================
# RUN DIRECTLY
# ==============================================================

if __name__ == "__main__":

    run_complete_learning_cycle()