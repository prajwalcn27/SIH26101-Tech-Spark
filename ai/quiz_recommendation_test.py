from quiz_result_analyzer import QuizResultAnalyzer
from recommendation_engine import RecommendationEngine


# ---------------------------------------------------------
# STEP 1: Sample quiz questions
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# STEP 2: Employee answers
# ---------------------------------------------------------

answers = {
    "1": "A",
    "2": "C",
    "3": "B"
}


# ---------------------------------------------------------
# STEP 3: Analyze quiz
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# STEP 4: Create gap analysis
#         Only HIGH and MEDIUM gaps are recommended
# ---------------------------------------------------------

gap_analysis = []

for topic, data in quiz_analysis["topic_analysis"].items():

    if data["gap_level"] in ["HIGH", "MEDIUM"]:

        gap_analysis.append({
            "topic": topic,
            "score": data["percentage"],
            "level": data["gap_level"]
        })


print("\n===================================")
print("       GAP ANALYSIS")
print("===================================")

if not gap_analysis:

    print("No learning gaps found.")

else:

    for gap in gap_analysis:

        print(
            f"{gap['topic']}: "
            f"{gap['score']}% "
            f"({gap['level']})"
        )


# ---------------------------------------------------------
# STEP 5: Generate recommendations
# ---------------------------------------------------------

engine = RecommendationEngine(
    "content_index.json"
)

recommendations = engine.generate_recommendations(
    gap_analysis,
    top_k=2
)


# ---------------------------------------------------------
# STEP 6: Display recommendations
# ---------------------------------------------------------

print("\n===================================")
print("   PERSONALIZED RECOMMENDATIONS")
print("===================================")

engine.display_recommendations(
    recommendations
)