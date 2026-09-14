"""
Integrated AI Learning Pipeline
SIH26101 - Tech Spark

This file connects the main AI learning components:

1. Question Manager
2. Initial Assessment
3. Competency Gap Analysis
4. Learning Recommendation
5. Targeted Quiz
6. Quiz Result Analysis
7. Competency Update
8. Learning Profile
9. Save Complete Pipeline Result

Gemini API is NOT called directly here.
Gemini is used by the individual AI modules such as:
- mcq_generator.py
- validator.py
- content_analyzer.py

This pipeline connects all modules together.
"""

import json

from question_manager import QuestionManager
from assessment_engine import (
    AssessmentEngine,
    display_results as display_assessment_results
)
from gap_analyzer import GapAnalyzer
from recommendation_engine import RecommendationEngine
from quiz_manager import QuizManager
from quiz_result_analyzer import (
    QuizResultAnalyzer,
    display_results as display_quiz_results
)
from competency_updater import CompetencyUpdater
from learning_profile import LearningProfile


# ============================================================
# CONFIGURATION
# ============================================================

QUESTION_BANK_FILE = "question_bank.json"

OUTPUT_FILE = "integrated_ai_pipeline_result.json"

EMPLOYEE_ID = "EMP001"

EMPLOYEE_NAME = "Demo Employee"

NUMBER_OF_ASSESSMENT_QUESTIONS = 6

NUMBER_OF_QUIZ_QUESTIONS = 5

GAP_THRESHOLD = 60

LEARNING_WEIGHT = 0.4


# ============================================================
# STEP 1
# LOAD QUESTION BANK
# ============================================================

def load_questions():

    print("\n" + "=" * 70)
    print("[STEP 1] Loading question bank...")
    print("=" * 70)

    question_manager = QuestionManager(
        QUESTION_BANK_FILE
    )

    # Remove duplicate questions
    question_manager.remove_duplicates()

    # Get questions for initial assessment
    questions = question_manager.get_random_questions(
        NUMBER_OF_ASSESSMENT_QUESTIONS
    )

    if not questions:

        print("❌ No questions available.")

        return None, None

    print(
        f"✅ Selected {len(questions)} questions "
        f"for initial assessment."
    )

    return question_manager, questions


# ============================================================
# STEP 2
# INITIAL ASSESSMENT
# ============================================================

def run_initial_assessment(questions):

    print("\n" + "=" * 70)
    print("[STEP 2] Running initial competency assessment...")
    print("=" * 70)

    # --------------------------------------------------------
    # Demo answers
    #
    # These answers are only for testing the pipeline.
    #
    # In the real application:
    # Employee answers will come from the frontend.
    # --------------------------------------------------------

    demo_answers = {}

    for index, question in enumerate(
        questions,
        start=1
    ):

        question_id = str(
            question.get(
                "id",
                index
            )
        )

        # ----------------------------------------------------
        # For demonstration:
        #
        # Make some answers correct and some wrong.
        # ----------------------------------------------------

        if index % 3 == 0:

            # Deliberately wrong answer
            demo_answers[question_id] = "A"

        else:

            # Use correct answer
            demo_answers[question_id] = (
                question["correct_answer"]
            )

    engine = AssessmentEngine()

    results = engine.calculate_results(
        questions,
        demo_answers
    )

    display_assessment_results(results)

    return results, demo_answers


# ============================================================
# STEP 3
# COMPETENCY GAP ANALYSIS
# ============================================================

def analyze_competency_gaps(assessment_results):

    print("\n" + "=" * 70)
    print("[STEP 3] Analyzing competency gaps...")
    print("=" * 70)

    # --------------------------------------------------------
    # AssessmentEngine returns:
    #
    # topic_scores = {
    #     "Data Cleaning": {
    #         "correct": 2,
    #         "total": 2,
    #         "percentage": 100
    #     }
    # }
    #
    # GapAnalyzer expects:
    #
    # {
    #     "Data Cleaning": 100
    # }
    #
    # Therefore convert the structure here.
    # --------------------------------------------------------

    topic_scores = {}

    for topic, result in assessment_results[
        "topic_scores"
    ].items():

        topic_scores[topic] = result[
            "percentage"
        ]

    gap_analyzer = GapAnalyzer(
        gap_threshold=GAP_THRESHOLD
    )

    gap_analysis = gap_analyzer.analyze(
        topic_scores
    )

    print("\nCompetency Gap Results:")

    for result in gap_analysis[
        "competency_results"
    ]:

        print(
            f"  {result['topic']:<25} "
            f"{result['score']:.2f}% "
            f"-> {result['status']} "
            f"({result['priority']})"
        )

    print("\nWeak Topics:")

    for topic in gap_analysis[
        "weak_topics"
    ]:

        print(
            f"  ⚠️ {topic}"
        )

    return gap_analysis


# ============================================================
# STEP 4
# LEARNING RECOMMENDATIONS
# ============================================================

def generate_recommendations(gap_analysis):

    print("\n" + "=" * 70)
    print("[STEP 4] Generating learning recommendations...")
    print("=" * 70)

    recommendation_engine = RecommendationEngine()

    recommendations = (
        recommendation_engine.generate_recommendations(
            gap_analysis,
            top_k=2
        )
    )

    print(
        f"✅ Generated {len(recommendations)} recommendations."
    )

    print("\nRecommendations:")

    for recommendation in recommendations:

        print(
            f"\n  Topic       : "
            f"{recommendation['topic']}"
        )

        print(
            f"  Section    : "
            f"{recommendation['section_id']}"
        )

        print(
            f"  Pages      : "
            f"{recommendation['pages']}"
        )

        print(
            f"  Match Score: "
            f"{recommendation['score']:.4f}"
        )

    return recommendations


# ============================================================
# STEP 5
# CREATE TARGETED QUIZ
# ============================================================

def create_targeted_quiz(
    question_manager,
    gap_analysis
):

    print("\n" + "=" * 70)
    print("[STEP 5] Creating targeted quiz...")
    print("=" * 70)

    # --------------------------------------------------------
    # Select the weakest topic.
    #
    # Instead of using weak_topics[0], we explicitly find
    # the topic with the lowest score.
    # --------------------------------------------------------

    competency_results = gap_analysis[
        "competency_results"
    ]

    if not competency_results:

        print("❌ No competency results available.")

        return None, None

    weakest_result = min(
        competency_results,
        key=lambda item: item["score"]
    )

    target_topic = weakest_result[
        "topic"
    ]

    print(
        f"🎯 Target topic: {target_topic}"
    )

    quiz_manager = QuizManager(
        question_manager
    )

    quiz_questions = (
        quiz_manager.create_targeted_quiz(
            topic=target_topic,
            number_of_questions=NUMBER_OF_QUIZ_QUESTIONS
        )
    )

    if not quiz_questions:

        print(
            "⚠️ No targeted quiz questions available."
        )

        return target_topic, []

    print(
        f"✅ Created targeted quiz with "
        f"{len(quiz_questions)} questions."
    )

    quiz_manager.display_quiz(
        quiz_questions
    )

    return target_topic, quiz_questions


# ============================================================
# STEP 6
# TAKE QUIZ
# ============================================================

def take_quiz(quiz_questions):

    print("\n" + "=" * 70)
    print("[STEP 6] Processing quiz answers...")
    print("=" * 70)

    if not quiz_questions:

        print("❌ No quiz questions available.")

        return {}

    # --------------------------------------------------------
    # Demo quiz answers
    #
    # For testing the pipeline we automatically select the
    # correct answer.
    #
    # In the real application:
    # These answers will come from the employee through
    # the frontend.
    # --------------------------------------------------------

    answers = {}

    for index, question in enumerate(
        quiz_questions,
        start=1
    ):

        question_id = str(
            question.get(
                "id",
                index
            )
        )

        answers[question_id] = (
            question["correct_answer"]
        )

    print(
        f"✅ Received answers for "
        f"{len(answers)} questions."
    )

    return answers


# ============================================================
# STEP 7
# ANALYZE QUIZ RESULT
# ============================================================

def analyze_quiz(
    quiz_questions,
    quiz_answers
):

    print("\n" + "=" * 70)
    print("[STEP 7] Analyzing quiz result...")
    print("=" * 70)

    analyzer = QuizResultAnalyzer()

    quiz_results = analyzer.analyze(
        quiz_questions,
        quiz_answers
    )

    display_quiz_results(
        quiz_results
    )

    return quiz_results


# ============================================================
# STEP 8
# PREPARE QUIZ RESULTS FOR COMPETENCY UPDATER
# ============================================================

def prepare_quiz_results_for_updater(
    quiz_results
):

    # --------------------------------------------------------
    # QuizResultAnalyzer returns:
    #
    # "topic_results": {
    #     "Data Cleaning": {
    #         "correct": 2,
    #         "total": 2,
    #         "percentage": 100
    #     }
    # }
    #
    # CompetencyUpdater expects the quiz percentage directly:
    #
    # {
    #     "Data Cleaning": 100
    # }
    # --------------------------------------------------------

    quiz_topic_results = {}

    for topic, result in quiz_results[
        "topic_results"
    ].items():

        quiz_topic_results[topic] = (
            result["percentage"]
        )

    return quiz_topic_results


# ============================================================
# STEP 9
# UPDATE COMPETENCY
# ============================================================

def update_competencies(
    gap_analysis,
    quiz_results
):

    print("\n" + "=" * 70)
    print("[STEP 8] Updating competency profile...")
    print("=" * 70)

    # --------------------------------------------------------
    # Get previous competency scores
    # --------------------------------------------------------

    previous_scores = {}

    for result in gap_analysis[
        "competency_results"
    ]:

        previous_scores[
            result["topic"]
        ] = result["score"]

    print("\nPrevious Scores:")

    for topic, score in previous_scores.items():

        print(
            f"  {topic:<25} "
            f"{score:.2f}%"
        )

    # --------------------------------------------------------
    # Convert quiz results into format expected by
    # CompetencyUpdater.
    # --------------------------------------------------------

    quiz_topic_results = (
        prepare_quiz_results_for_updater(
            quiz_results
        )
    )

    print("\nQuiz Scores:")

    for topic, score in quiz_topic_results.items():

        print(
            f"  {topic:<25} "
            f"{score:.2f}%"
        )

    # --------------------------------------------------------
    # Competency Updater
    # --------------------------------------------------------

    updater = CompetencyUpdater(
        learning_weight=LEARNING_WEIGHT
    )

    updater_result = (
        updater.update_competency(
            previous_scores,
            quiz_topic_results
        )
    )

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # CompetencyUpdater returns:
    #
    # {
    #     "updated_competencies": {
    #         "Data Cleaning": {
    #             "previous_score": 0,
    #             "quiz_score": 100,
    #             "updated_score": 40,
    #             "status": "GAP"
    #         }
    #     }
    # }
    #
    # So we must access ["updated_competencies"].
    # --------------------------------------------------------

    updated_competencies = (
        updater_result[
            "updated_competencies"
        ]
    )

    print("\nUpdated Competencies:")

    for topic, data in (
        updated_competencies.items()
    ):

        updated_score = data[
            "updated_score"
        ]

        status = data[
            "status"
        ]

        quiz_score = data[
            "quiz_score"
        ]

        print(
            f"  {topic:<25} "
            f"{updated_score:.2f}% "
            f"({status}) "
            f"| Quiz: {quiz_score}"
        )

    return updater_result


# ============================================================
# STEP 10
# CREATE LEARNING PROFILE
# ============================================================

def create_learning_profile(
    gap_analysis,
    recommendations,
    quiz_results,
    updater_result
):

    print("\n" + "=" * 70)
    print("[STEP 9] Creating employee learning profile...")
    print("=" * 70)

    profile = LearningProfile(
        employee_id=EMPLOYEE_ID,
        employee_name=EMPLOYEE_NAME
    )

    # --------------------------------------------------------
    # Initial competency scores
    # --------------------------------------------------------

    initial_competencies = {}

    for result in gap_analysis[
        "competency_results"
    ]:

        initial_competencies[
            result["topic"]
        ] = result["score"]

    profile.add_competencies(
        initial_competencies
    )

    # --------------------------------------------------------
    # Weak topics
    # --------------------------------------------------------

    profile.add_weak_topics(
        gap_analysis[
            "weak_topics"
        ]
    )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    profile.add_recommendations(
        recommendations
    )

    # --------------------------------------------------------
    # Quiz history
    # --------------------------------------------------------

    profile.add_quiz_result(
        quiz_results
    )

    # --------------------------------------------------------
    # Updated competency scores
    # --------------------------------------------------------

    updated_competencies = (
        updater_result[
            "updated_competencies"
        ]
    )

    # --------------------------------------------------------
    # Convert updater structure into the format expected
    # by LearningProfile.
    #
    # LearningProfile should receive:
    #
    # {
    #     "Data Cleaning": 40,
    #     "Decision Tree": 50
    # }
    # --------------------------------------------------------

    updated_scores = {}

    for topic, data in (
        updated_competencies.items()
    ):

        updated_scores[
            topic
        ] = data[
            "updated_score"
        ]

    profile.update_competencies(
        updated_scores
    )

    # --------------------------------------------------------
    # Display profile
    # --------------------------------------------------------

    profile.display_profile()

    return profile


# ============================================================
# STEP 11
# SAVE COMPLETE PIPELINE RESULT
# ============================================================

def save_complete_result(
    assessment_results,
    gap_analysis,
    recommendations,
    quiz_results,
    updater_result,
    profile
):

    print("\n" + "=" * 70)
    print("[STEP 10] Saving complete pipeline result...")
    print("=" * 70)

    # --------------------------------------------------------
    # Convert LearningProfile object into dictionary.
    #
    # The profile class stores the actual data inside
    # profile.profile.
    # --------------------------------------------------------

    if hasattr(
        profile,
        "profile"
    ):

        profile_data = (
            profile.profile
        )

    else:

        profile_data = profile

    complete_result = {

        "employee": {
            "employee_id": EMPLOYEE_ID,
            "employee_name": EMPLOYEE_NAME
        },

        "assessment": assessment_results,

        "gap_analysis": gap_analysis,

        "recommendations": recommendations,

        "quiz_results": quiz_results,

        "updated_competencies": (
            updater_result[
                "updated_competencies"
            ]
        ),

        "learning_profile": profile_data
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            complete_result,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"✅ Complete result saved: "
        f"{OUTPUT_FILE}"
    )

    return complete_result


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_integrated_pipeline():

    print("\n")
    print("=" * 70)
    print("      SIH26101 - INTEGRATED AI LEARNING PIPELINE")
    print("                     TECH SPARK")
    print("=" * 70)

    # --------------------------------------------------------
    # STEP 1
    # --------------------------------------------------------

    question_manager, assessment_questions = (
        load_questions()
    )

    if question_manager is None:

        return

    # --------------------------------------------------------
    # STEP 2
    # --------------------------------------------------------

    assessment_results, assessment_answers = (
        run_initial_assessment(
            assessment_questions
        )
    )

    # --------------------------------------------------------
    # STEP 3
    # --------------------------------------------------------

    gap_analysis = (
        analyze_competency_gaps(
            assessment_results
        )
    )

    # --------------------------------------------------------
    # STEP 4
    # --------------------------------------------------------

    recommendations = (
        generate_recommendations(
            gap_analysis
        )
    )

    # --------------------------------------------------------
    # STEP 5
    # --------------------------------------------------------

    target_topic, quiz_questions = (
        create_targeted_quiz(
            question_manager,
            gap_analysis
        )
    )

    # --------------------------------------------------------
    # STEP 6
    # --------------------------------------------------------

    quiz_answers = take_quiz(
        quiz_questions
    )

    # --------------------------------------------------------
    # STEP 7
    # --------------------------------------------------------

    quiz_results = analyze_quiz(
        quiz_questions,
        quiz_answers
    )

    # --------------------------------------------------------
    # STEP 8
    # --------------------------------------------------------

    updater_result = update_competencies(
        gap_analysis,
        quiz_results
    )

    # --------------------------------------------------------
    # STEP 9
    # --------------------------------------------------------

    profile = create_learning_profile(
        gap_analysis,
        recommendations,
        quiz_results,
        updater_result
    )

    # --------------------------------------------------------
    # STEP 10
    # --------------------------------------------------------

    complete_result = save_complete_result(
        assessment_results,
        gap_analysis,
        recommendations,
        quiz_results,
        updater_result,
        profile
    )

    # --------------------------------------------------------
    # FINAL MESSAGE
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("       ✅ AI PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nFlow completed:")

    print(
        "  1. Question Bank"
    )

    print(
        "  2. Initial Assessment"
    )

    print(
        "  3. Competency Gap Analysis"
    )

    print(
        "  4. Learning Recommendation"
    )

    print(
        "  5. Targeted Quiz"
    )

    print(
        "  6. Quiz Attempt"
    )

    print(
        "  7. Quiz Result Analysis"
    )

    print(
        "  8. Competency Update"
    )

    print(
        "  9. Learning Profile"
    )

    print(
        " 10. Complete Result Saved"
    )

    print(
        f"\n📄 Output file: "
        f"{OUTPUT_FILE}"
    )

    return complete_result


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_integrated_pipeline()