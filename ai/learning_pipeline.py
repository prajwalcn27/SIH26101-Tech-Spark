import json

from question_manager import QuestionManager
from assessment_engine import AssessmentEngine, display_results
from gap_analyzer import CompetencyGapAnalyzer
from recommendation_engine import RecommendationEngine


def run_learning_pipeline():

    print("=" * 60)
    print("              LEARNING PIPELINE")
    print("=" * 60)

    # --------------------------------------------------
    # 1. QUESTION MANAGER
    # --------------------------------------------------

    print("\n📚 STEP 1: Loading Question Manager...")

    question_manager = QuestionManager()

    # Remove duplicate questions
    question_manager.remove_duplicates()

    # Get questions for assessment
    questions = question_manager.get_random_questions(
        number_of_questions=6
    )

    if not questions:
        print("❌ No questions available.")
        return

    print(
        f"✅ Selected {len(questions)} questions "
        "for assessment."
    )

    # Display selected questions
    question_manager.display_questions(questions)

    # --------------------------------------------------
    # 2. EMPLOYEE ANSWERS
    # --------------------------------------------------

    print("\n📝 STEP 2: Processing employee answers...")

    # Demo answers for testing.
    #
    # In the real system these answers will come
    # from the frontend.

    answers = {}

    for question in questions:

        question_id = str(question["id"])

        # Demo answers
        demo_answers = {
            "1": "B",
            "2": "A",
            "3": "A",
            "4": "C",
            "5": "B",
            "6": "D"
        }

        answers[question_id] = demo_answers.get(
            question_id,
            ""
        )

    print("✅ Employee answers received.")

    # --------------------------------------------------
    # 3. ASSESSMENT ENGINE
    # --------------------------------------------------

    print("\n📊 STEP 3: Calculating assessment results...")

    assessment_engine = AssessmentEngine()

    assessment_results = assessment_engine.calculate_results(
        questions,
        answers
    )

    if not assessment_results:
        print("❌ Assessment calculation failed.")
        return

    display_results(assessment_results)

    # --------------------------------------------------
    # 4. GAP ANALYSIS
    # --------------------------------------------------

    print("\n🔍 STEP 4: Identifying competency gaps...")

    analyzer = CompetencyGapAnalyzer(
        gap_threshold=60
    )

    # Convert topic scores into the format expected
    # by GapAnalyzer

    competency_scores = {}

    for topic, data in assessment_results[
        "topic_scores"
    ].items():

        competency_scores[topic] = data[
            "percentage"
        ]

    gap_analysis = analyzer.analyze(
        competency_scores
    )

    print("\n📌 GAP ANALYSIS")

    for result in gap_analysis["competency_results"]:

     print(
        f"📘 {result['topic']:<20} "
        f"{result['score']}% → "
        f"{result['status']}"
    )
   
   

   
   
   
   
   

    print("\n⚠️ Weak Topics:")

    for topic in gap_analysis["weak_topics"]:

        print(f"   • {topic}")

    # --------------------------------------------------
    # 5. RECOMMENDATION ENGINE
    # --------------------------------------------------

    print("\n🎯 STEP 5: Generating recommendations...")

    recommendation_engine = RecommendationEngine()

    recommendations = recommendation_engine.generate_recommendations(
        gap_analysis
    )

    print("\n📚 RECOMMENDATIONS")

    if recommendations:

        for recommendation in recommendations:

            print(
                f"\n📘 Topic: "
                f"{recommendation.get('topic', 'Unknown')}"
            )

            print(
                f"   Section: "
                f"{recommendation.get('section_id', 'N/A')}"
            )

            print(
                f"   Score: "
                f"{recommendation.get('final_score', 0)}"
            )

    else:

        print("ℹ️ No recommendations generated.")

    # --------------------------------------------------
    # 6. SAVE COMPLETE PIPELINE RESULT
    # --------------------------------------------------

    final_result = {

        "assessment": assessment_results,

        "gap_analysis": gap_analysis,

        "recommendations": recommendations

    }

    output_file = "learning_pipeline_result.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            final_result,
            file,
            indent=4
        )

    print(
        f"\n💾 Complete pipeline result saved to: "
        f"{output_file}"
    )

    print("\n" + "=" * 60)
    print("       LEARNING PIPELINE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":

    run_learning_pipeline()