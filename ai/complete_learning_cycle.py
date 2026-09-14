import json

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


def run_complete_learning_cycle():

    print("=" * 70)
    print("              COMPLETE LEARNING CYCLE")
    print("=" * 70)

    # ==========================================================
    # STEP 1: QUESTION MANAGER
    # ==========================================================

    print("\n📚 STEP 1: Loading Question Manager...")

    question_manager = QuestionManager()

    question_manager.remove_duplicates()

    assessment_questions = (
        question_manager.get_random_questions(
            number_of_questions=6
        )
    )

    if not assessment_questions:

        print("❌ No assessment questions available.")

        return None

    print(
        f"✅ Loaded {len(question_manager.questions)} "
        f"questions from question bank."
    )

    print(
        f"✅ Selected {len(assessment_questions)} "
        f"assessment questions."
    )

    # ==========================================================
    # STEP 2: INITIAL ASSESSMENT
    # ==========================================================

    print("\n📝 STEP 2: Initial Assessment...")

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
            "❌ Assessment calculation failed."
        )

        return None

    display_assessment_results(
        assessment_results
    )

    # ==========================================================
    # STEP 3: COMPETENCY GAP ANALYSIS
    # ==========================================================

    print(
        "\n🔍 STEP 3: Competency "
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
        "\n📌 IDENTIFIED COMPETENCY GAPS"
    )

    for result in (
        gap_analysis[
            "competency_results"
        ]
    ):

        print(
            f"📘 {result['topic']:<20} "
            f"{result['score']}% → "
            f"{result['status']} "
            f"[{result['priority']}]"
        )

    print("\n⚠️ Weak Topics:")

    if gap_analysis["weak_topics"]:

        for topic in (
            gap_analysis[
                "weak_topics"
            ]
        ):

            print(
                f"   • {topic}"
            )

    else:

        print(
            "   ✅ No weak topics found."
        )

    # ==========================================================
    # STEP 4: PERSONALIZED LEARNING RECOMMENDATION
    # ==========================================================

    print(
        "\n🎯 STEP 4: Personalized "
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
        "\n📚 RECOMMENDED MATERIAL"
    )

    if recommendations:

        for recommendation in (
            recommendations
        ):

            print(
                f"\n📘 Topic: "
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
            "   ℹ️ No recommendations."
        )

    # ==========================================================
    # STEP 5: TARGETED QUIZ
    # ==========================================================

    print(
        "\n📝 STEP 5: Creating "
        "Targeted Quiz..."
    )

    quiz_manager = QuizManager(
        question_manager
    )

    weak_topics = (
        gap_analysis[
            "weak_topics"
        ]
    )

    target_topic = None

    if weak_topics:

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
            f"\n🎯 Target Topic: "
            f"{target_topic}"
        )

        targeted_quiz = (
            quiz_manager.create_targeted_quiz(
                topic=target_topic,
                number_of_questions=2
            )
        )

    else:

        targeted_quiz = (
            quiz_manager.create_quiz(
                number_of_questions=2
            )
        )

    if not targeted_quiz:

        print(
            "❌ Could not create targeted quiz."
        )

        return None

    quiz_manager.display_quiz(
        targeted_quiz
    )

    # ==========================================================
    # STEP 6: QUIZ ATTEMPT
    # ==========================================================

    print(
        "\n✍️ STEP 6: Processing "
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
        "✅ Employee quiz answers received."
    )

    # ==========================================================
    # STEP 7: QUIZ RESULT ANALYSIS
    # ==========================================================

    print(
        "\n📊 STEP 7: Analyzing "
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
            "❌ Quiz result analysis failed."
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
        "\n🔄 STEP 8: Updating "
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
            learning_weight=0.4
        )
    )

    updated_competency = (
        competency_updater.update_competency(
            previous_scores,
            competency_quiz_results
        )
    )

    print(
        "\n📈 UPDATED COMPETENCY PROFILE"
    )

    for topic, data in (
        updated_competency[
            "updated_competencies"
        ].items()
    ):

        print(
            f"\n📘 {topic}"
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
        "\n💾 STEP 9: Creating "
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
        f"\n💾 Final learning profile saved to:"
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
        "\n✅ Question selection"
    )

    print(
        "✅ Initial assessment"
    )

    print(
        "✅ Competency gap analysis"
    )

    print(
        "✅ Personalized recommendation"
    )

    print(
        "✅ Targeted quiz"
    )

    print(
        "✅ Quiz result analysis"
    )

    print(
        "✅ Competency update"
    )

    print(
        "✅ Final learning profile"
    )

    print(
        "\n🚀 AI LEARNING LOOP COMPLETED!"
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