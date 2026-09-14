# SIH26101 - Tech Spark
# Member 6 - Assessment, Scoring & Progress

from db import get_connection


# ============================================================
# ASSESSMENT QUESTIONS
# ============================================================

questions = [
    {
        "question": "Which Excel feature is used to summarize large amounts of data?",
        "topic": "Excel",
        "competency_id": 1,
        "correct_answer": "B"
    },
    {
        "question": "Which Excel function is commonly used to add numbers?",
        "topic": "Excel",
        "competency_id": 1,
        "correct_answer": "A"
    },
    {
        "question": "What is the process of removing incorrect or duplicate data called?",
        "topic": "Data Cleaning",
        "competency_id": 2,
        "correct_answer": "C"
    },
    {
        "question": "Which technique can be used to handle missing values?",
        "topic": "Data Cleaning",
        "competency_id": 2,
        "correct_answer": "B"
    },
    {
        "question": "What is the average value of a dataset called?",
        "topic": "Statistics",
        "competency_id": 4,
        "correct_answer": "A"
    },
    {
        "question": "Which measure represents the middle value of ordered data?",
        "topic": "Statistics",
        "competency_id": 4,
        "correct_answer": "C"
    },
    {
        "question": "What does a chart help us do?",
        "topic": "Data Visualization",
        "competency_id": 3,
        "correct_answer": "B"
    },
    {
        "question": "What is data interpretation?",
        "topic": "Data Visualization",
        "competency_id": 3,
        "correct_answer": "A"
    },
    {
        "question": "Which Excel feature can group and summarize data?",
        "topic": "Excel",
        "competency_id": 1,
        "correct_answer": "D"
    },
    {
        "question": "Which is an important step before analyzing data?",
        "topic": "Data Cleaning",
        "competency_id": 2,
        "correct_answer": "C"
    }
]


# ============================================================
# CALCULATE ASSESSMENT SCORE
# ============================================================

def calculate_score(questions, answers):

    total_questions = len(questions)
    correct_answers = 0

    topic_total = {}
    topic_correct = {}

    for i, question in enumerate(questions):

        topic = question["topic"]

        # Count total questions for each topic
        topic_total[topic] = topic_total.get(topic, 0) + 1

        # Check employee answer
        if answers[i].upper() == question["correct_answer"]:
            correct_answers += 1
            topic_correct[topic] = topic_correct.get(topic, 0) + 1
        else:
            topic_correct.setdefault(topic, 0)

    # Overall percentage
    overall_percentage = (
        correct_answers / total_questions
    ) * 100

    # Topic-wise percentage
    topic_scores = {}

    for topic in topic_total:

        score = (
            topic_correct[topic]
            / topic_total[topic]
        ) * 100

        topic_scores[topic] = score

    # Find weakest topic
    weakest_topic = min(
        topic_scores,
        key=topic_scores.get
    )

    # No gap if weakest topic is 70% or above
    if topic_scores[weakest_topic] >= 70:
        weakest_topic = "No significant gap"

    return (
        overall_percentage,
        topic_scores,
        weakest_topic
    )


# ============================================================
# COMPETENCY LEVEL
# ============================================================

def get_competency_level(score):

    if score >= 80:
        return "Strong"

    elif score >= 60:
        return "Moderate"

    else:
        return "Needs Improvement"


# ============================================================
# UPDATE COMPETENCY SCORE
# Used later after quiz
# ============================================================

def update_competency_score(before_score, quiz_score):

    updated_score = (
        before_score + quiz_score
    ) / 2

    return round(updated_score, 2)


# ============================================================
# SAVE ASSESSMENT RESULT TO MYSQL
# ============================================================

def save_assessment_result(
    employee_id,
    overall_score,
    topic_scores
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ----------------------------------------------------
        # 1. Save overall assessment
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO assessments
            (
                employee_id,
                title,
                total_questions,
                score,
                completed_at
            )
            VALUES (%s, %s, %s, %s, NOW())
            """,
            (
                employee_id,
                "Statistical Officer Initial Assessment",
                len(questions),
                round(overall_score, 2)
            )
        )

        # ----------------------------------------------------
        # 2. Save topic-wise competency scores
        # ----------------------------------------------------

        competency_map = {
            "Excel": 1,
            "Data Cleaning": 2,
            "Data Visualization": 3,
            "Statistics": 4
        }

        for topic, score in topic_scores.items():

            competency_id = competency_map.get(topic)

            if competency_id:

                cursor.execute(
                    """
                    INSERT INTO competency_scores
                    (
                        employee_id,
                        competency_id,
                        score,
                        assessed_from
                    )
                    VALUES (%s, %s, %s, %s)

                    ON DUPLICATE KEY UPDATE
                    score = VALUES(score),
                    assessed_from = VALUES(assessed_from)
                    """,
                    (
                        employee_id,
                        competency_id,
                        round(score, 2),
                        "Initial Assessment"
                    )
                )

        # ----------------------------------------------------
        # 3. Save competency gaps
        # ----------------------------------------------------

        required_score = 70.00

        for topic, score in topic_scores.items():

            competency_id = competency_map.get(topic)

            if competency_id:

                gap_score = max(
                    required_score - score,
                    0
                )

                if score >= 70:
                    gap_level = "No Gap"

                elif score >= 50:
                    gap_level = "Medium"

                else:
                    gap_level = "High"

                cursor.execute(
                    """
                    INSERT INTO competency_gaps
                    (
                        employee_id,
                        competency_id,
                        current_score,
                        required_score,
                        gap_score,
                        gap_level
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)

                    ON DUPLICATE KEY UPDATE
                    current_score = VALUES(current_score),
                    required_score = VALUES(required_score),
                    gap_score = VALUES(gap_score),
                    gap_level = VALUES(gap_level)
                    """,
                    (
                        employee_id,
                        competency_id,
                        round(score, 2),
                        required_score,
                        round(gap_score, 2),
                        gap_level
                    )
                )

        # ----------------------------------------------------
        # Commit all database changes
        # ----------------------------------------------------

        conn.commit()

        print(
            "\nAssessment result saved to MySQL successfully."
        )

        print(
            "Competency scores and gaps saved successfully."
        )

    except Exception as e:

        conn.rollback()

        print(
            "\nDatabase error:",
            e
        )

    finally:

        cursor.close()
        conn.close()


# ============================================================
# RUN ASSESSMENT
# ============================================================

def run_assessment():

    print("\n======================================")
    print("       SIH26101 EMPLOYEE ASSESSMENT")
    print("======================================")

    print(
        "\nAnswer each question using A, B, C or D."
    )

    answers = []

    # --------------------------------------------------------
    # Options
    # --------------------------------------------------------

    options = {

        1: [
            "A. Filter",
            "B. Pivot Table",
            "C. Sort",
            "D. Format"
        ],

        2: [
            "A. SUM",
            "B. COUNT",
            "C. MAX",
            "D. MIN"
        ],

        3: [
            "A. Data Entry",
            "B. Data Export",
            "C. Data Cleaning",
            "D. Data Storage"
        ],

        4: [
            "A. Delete everything",
            "B. Fill or replace values",
            "C. Ignore data",
            "D. Duplicate data"
        ],

        5: [
            "A. Mean",
            "B. Range",
            "C. Mode",
            "D. Variance"
        ],

        6: [
            "A. Mean",
            "B. Range",
            "C. Median",
            "D. Sum"
        ],

        7: [
            "A. Delete data",
            "B. Visualize data",
            "C. Encrypt data",
            "D. Store passwords"
        ],

        8: [
            "A. Understanding and analyzing data",
            "B. Deleting data",
            "C. Copying data",
            "D. Formatting passwords"
        ],

        9: [
            "A. Filter",
            "B. Sort",
            "C. Chart",
            "D. Pivot Table"
        ],

        10: [
            "A. Printing",
            "B. Formatting",
            "C. Cleaning data",
            "D. Sharing data"
        ]
    }

    # --------------------------------------------------------
    # Ask questions
    # --------------------------------------------------------

    for i, question in enumerate(
        questions,
        start=1
    ):

        print(
            f"\nQ{i}. {question['question']}"
        )

        for option in options[i]:
            print(option)

        answer = input(
            "Your answer: "
        ).strip().upper()

        while answer not in [
            "A",
            "B",
            "C",
            "D"
        ]:

            print(
                "Please enter only A, B, C or D."
            )

            answer = input(
                "Your answer: "
            ).strip().upper()

        answers.append(answer)

    # --------------------------------------------------------
    # Calculate result
    # --------------------------------------------------------

    overall, topic_scores, weakest_topic = calculate_score(
        questions,
        answers
    )

    # --------------------------------------------------------
    # Save to MySQL
    # --------------------------------------------------------

    save_assessment_result(
        employee_id=1,
        overall_score=overall,
        topic_scores=topic_scores
    )

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print("\n======================================")
    print("          ASSESSMENT RESULT")
    print("======================================")

    print(
        f"\nOverall Score: {overall:.2f}%"
    )

    print(
        "\nTopic-wise Performance:"
    )

    for topic, score in topic_scores.items():

        level = get_competency_level(score)

        print(
            f"{topic}: "
            f"{score:.2f}% → {level}"
        )

    print(
        "\n--------------------------------------"
    )

    if weakest_topic == "No significant gap":

        print(
            "Competency Status: GOOD"
        )

        print(
            "No significant competency gap identified."
        )

        print(
            "\nRecommendation:"
        )

        print(
            "Continue with the next learning activity."
        )

    else:

        print(
            f"Weakest Topic: {weakest_topic}"
        )

        print(
            f"Competency Gap Identified: "
            f"{weakest_topic}"
        )

        print(
            "\nRecommendation:"
        )

        print(
            "Focus on learning materials related to "
            f"{weakest_topic}."
        )

    print(
        "--------------------------------------"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_assessment()