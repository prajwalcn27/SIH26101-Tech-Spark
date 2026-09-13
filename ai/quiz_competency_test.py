from quiz_result_analyzer import QuizResultAnalyzer
from competency_updater import CompetencyUpdater


# ============================================
# SAMPLE QUIZ
# ============================================

questions = [
    {
        "question": "What is data cleaning?",
        "correct_answer": "A",
        "topic": "Data Cleaning",
        "explanation": "Data cleaning improves data quality."
    },
    {
        "question": "What is a duplicate record?",
        "correct_answer": "B",
        "topic": "Data Cleaning",
        "explanation": "A duplicate record is repeated data."
    },
    {
        "question": "What does data validation check?",
        "correct_answer": "A",
        "topic": "Data Validation",
        "explanation": "Data validation checks predefined rules."
    }
]


# ============================================
# EMPLOYEE ANSWERS
# ============================================

answers = {
    "1": "A",
    "2": "C",
    "3": "B"
}


# ============================================
# STEP 1: ANALYZE QUIZ
# ============================================

analyzer = QuizResultAnalyzer()

quiz_analysis = analyzer.analyze(
    questions,
    answers
)

print("\n===================================")
print("       QUIZ ANALYSIS")
print("===================================")

print(
    f"Score: {quiz_analysis['score_percentage']}%"
)

print(
    f"Weak Topics: {quiz_analysis['weak_topics']}"
)


# ============================================
# STEP 2: PREPARE COMPETENCY DATA
# ============================================

previous_scores = {
    "Data Cleaning": 50,
    "Data Validation": 40
}


quiz_results = {}

for topic, data in quiz_analysis["topic_analysis"].items():

    quiz_results[topic] = {
        "percentage": data["percentage"]
    }


# ============================================
# STEP 3: UPDATE COMPETENCY
# ============================================

updater = CompetencyUpdater(
    learning_weight=0.4
)

updated_result = updater.update_competency(
    previous_scores,
    quiz_results
)


# ============================================
# DISPLAY RESULT
# ============================================

print("\n===================================")
print("     UPDATED COMPETENCIES")
print("===================================")

for topic, data in updated_result[
    "updated_competencies"
].items():

    print(
        f"{topic}: "
        f"{data['previous_score']}% → "
        f"{data['updated_score']}% "
        f"({data['status']})"
    )