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
# PROCESS QUIZ RESULT
# Calculates quiz score, identifies mistakes,
# and updates competency score
# ============================================================

def process_quiz_result(attempt_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # ----------------------------------------------------
        # 1. Get quiz attempt
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                quiz_id,
                employee_id,
                total_questions
            FROM quiz_attempts
            WHERE id = %s
            """,
            (attempt_id,)
        )

        attempt = cursor.fetchone()

        if not attempt:
            print("Quiz attempt not found.")
            return

        quiz_id = attempt["quiz_id"]
        employee_id = attempt["employee_id"]
        total_questions = attempt["total_questions"]

        # ----------------------------------------------------
        # 2. Get quiz answers
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                qa.question_id,
                qa.selected_answer,
                qa.is_correct,
                q.correct_answer,
                q.competency_id
            FROM quiz_answers qa
            JOIN questions q
                ON qa.question_id = q.id
            WHERE qa.attempt_id = %s
            """,
            (attempt_id,)
        )

        answers = cursor.fetchall()

        if not answers:
            print("No quiz answers found.")
            return

        # ----------------------------------------------------
        # 3. Calculate score
        # ----------------------------------------------------

        correct_count = sum(
            1 for answer in answers
            if answer["is_correct"] == 1
        )

        quiz_score = (
            correct_count / total_questions
        ) * 100

        # ----------------------------------------------------
        # 4. Update quiz attempt score
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE quiz_attempts
            SET score = %s
            WHERE id = %s
            """,
            (
                round(quiz_score, 2),
                attempt_id
            )
        )

        # ----------------------------------------------------
        # 5. Count mistakes by competency
        # ----------------------------------------------------

        competency_correct = {}
        competency_total = {}

        for answer in answers:

            competency_id = answer["competency_id"]

            competency_total[competency_id] = (
                competency_total.get(
                    competency_id, 0
                ) + 1
            )

            if answer["is_correct"] == 1:

                competency_correct[competency_id] = (
                    competency_correct.get(
                        competency_id, 0
                    ) + 1
                )

            else:

                competency_correct.setdefault(
                    competency_id,
                    0
                )

        # ----------------------------------------------------
        # 6. Update competency score
        # ----------------------------------------------------

        for competency_id in competency_total:

            total = competency_total[competency_id]

            correct = competency_correct.get(
                competency_id,
                0
            )

            quiz_competency_score = (
                correct / total
            ) * 100

            # Get previous competency score
            cursor.execute(
                """
                SELECT score
                FROM competency_scores
                WHERE employee_id = %s
                AND competency_id = %s
                """,
                (
                    employee_id,
                    competency_id
                )
            )

            previous = cursor.fetchone()

            if previous:

                before_score = float(
                    previous["score"]
                )

                updated_score = update_competency_score(
                    before_score,
                    quiz_competency_score
                )

            else:

                updated_score = round(
                    quiz_competency_score,
                    2
                )

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
                    updated_score,
                    "Quiz"
                )
            )

        # ----------------------------------------------------
        # 7. Commit changes
        # ----------------------------------------------------

        conn.commit()

        # ----------------------------------------------------
        # 8. Display result
        # ----------------------------------------------------

        print("\n======================================")
        print("             QUIZ RESULT")
        print("======================================")

        print(
            f"Quiz Score: {quiz_score:.2f}%"
        )

        print(
            f"Correct Answers: "
            f"{correct_count}/{total_questions}"
        )

        print(
            f"Mistakes: "
            f"{total_questions - correct_count}"
        )

        print("\nMistake Analysis:")

        for answer in answers:

            if answer["is_correct"] == 0:

                print(
                    f"Question ID {answer['question_id']}: "
                    f"Wrong answer "
                    f"({answer['selected_answer']}) → "
                    f"Correct answer "
                    f"({answer['correct_answer']})"
                )

        print(
            "\nCompetency scores updated successfully."
        )

    except Exception as e:

        conn.rollback()

        print(
            "\nQuiz processing error:",
            e
        )

    finally:

        cursor.close()
        conn.close()
        
# ============================================================
# UPDATE LEARNING PROGRESS
# ============================================================

def update_learning_progress(
    employee_id,
    material_id,
    progress_percentage
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        if progress_percentage >= 100:
            status = "Completed"
            completed_at = "NOW()"
        else:
            status = "In Progress"
            completed_at = "NULL"

        cursor.execute(
            """
            SELECT id
            FROM employee_learning_progress
            WHERE employee_id = %s
            AND material_id = %s
            """,
            (
                employee_id,
                material_id
            )
        )

        existing = cursor.fetchone()

        if existing:

            if progress_percentage >= 100:

                cursor.execute(
                    """
                    UPDATE employee_learning_progress
                    SET progress_percentage = %s,
                        status = %s,
                        completed_at = NOW()
                    WHERE employee_id = %s
                    AND material_id = %s
                    """,
                    (
                        round(progress_percentage, 2),
                        status,
                        employee_id,
                        material_id
                    )
                )

            else:

                cursor.execute(
                    """
                    UPDATE employee_learning_progress
                    SET progress_percentage = %s,
                        status = %s
                    WHERE employee_id = %s
                    AND material_id = %s
                    """,
                    (
                        round(progress_percentage, 2),
                        status,
                        employee_id,
                        material_id
                    )
                )

        else:

            if progress_percentage >= 100:

                cursor.execute(
                    """
                    INSERT INTO employee_learning_progress
                    (
                        employee_id,
                        material_id,
                        progress_percentage,
                        status,
                        started_at,
                        completed_at
                    )
                    VALUES (%s, %s, %s, %s, NOW(), NOW())
                    """,
                    (
                        employee_id,
                        material_id,
                        round(progress_percentage, 2),
                        status
                    )
                )

            else:

                cursor.execute(
                    """
                    INSERT INTO employee_learning_progress
                    (
                        employee_id,
                        material_id,
                        progress_percentage,
                        status,
                        started_at
                    )
                    VALUES (%s, %s, %s, %s, NOW())
                    """,
                    (
                        employee_id,
                        material_id,
                        round(progress_percentage, 2),
                        status
                    )
                )

        conn.commit()

        print(
            "\nLearning progress updated successfully."
        )

    except Exception as e:

        conn.rollback()

        print(
            "\nProgress update error:",
            e
        )

    finally:

        cursor.close()
        conn.close()
        
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