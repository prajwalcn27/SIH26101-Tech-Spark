class QuizResultAnalyzer:

    def analyze(self, questions, answers):

        if not questions:

            return {
                "status": "error",
                "message": "No questions provided."
            }

        total_questions = len(questions)

        correct_count = 0
        wrong_count = 0

        wrong_questions = []

        topic_results = {}

        # ======================================================
        # ANALYZE EACH QUESTION
        # ======================================================

        for index, question in enumerate(
            questions,
            start=1
        ):

            # --------------------------------------------------
            # First try the actual question ID.
            # If not available, use question number.
            # --------------------------------------------------

            question_id = str(
                question.get("id", "")
            )

            question_number = str(index)

            if question_id in answers:

                employee_answer = str(
                    answers.get(question_id, "")
                ).strip().upper()

            else:

                employee_answer = str(
                    answers.get(question_number, "")
                ).strip().upper()

            correct_answer = str(
                question.get(
                    "correct_answer",
                    ""
                )
            ).strip().upper()

            topic = str(
                question.get(
                    "topic",
                    "Unknown"
                )
            ).strip()

            # --------------------------------------------------
            # Create topic entry if it doesn't exist
            # --------------------------------------------------

            if topic not in topic_results:

                topic_results[topic] = {
                    "correct": 0,
                    "wrong": 0,
                    "total": 0
                }

            topic_results[topic]["total"] += 1

            # --------------------------------------------------
            # Check answer
            # --------------------------------------------------

            if employee_answer == correct_answer:

                correct_count += 1

                topic_results[topic][
                    "correct"
                ] += 1

            else:

                wrong_count += 1

                topic_results[topic][
                    "wrong"
                ] += 1

                wrong_questions.append({

                    "question_number": index,

                    "question_id": question.get(
                        "id"
                    ),

                    "question": question.get(
                        "question",
                        ""
                    ),

                    "employee_answer":
                        employee_answer,

                    "correct_answer":
                        correct_answer,

                    "topic":
                        topic,

                    "explanation":
                        question.get(
                            "explanation",
                            ""
                        )
                })

        # ======================================================
        # OVERALL SCORE
        # ======================================================

        score_percentage = (
            correct_count /
            total_questions
        ) * 100

        # ======================================================
        # TOPIC-WISE ANALYSIS
        # ======================================================

        topic_analysis = {}

        weak_topics = []

        for topic, result in (
            topic_results.items()
        ):

            topic_percentage = (
                result["correct"] /
                result["total"]
            ) * 100

            # --------------------------------------------------
            # Determine gap level
            # --------------------------------------------------

            if topic_percentage < 50:

                level = "HIGH"

                weak_topics.append(
                    topic
                )

            elif topic_percentage < 70:

                level = "MEDIUM"

                weak_topics.append(
                    topic
                )

            else:

                level = "LOW"

            topic_analysis[topic] = {

                "correct":
                    result["correct"],

                "wrong":
                    result["wrong"],

                "total":
                    result["total"],

                "percentage":
                    round(
                        topic_percentage,
                        2
                    ),

                "gap_level":
                    level
            }

        # ======================================================
        # FINAL RESULT
        # ======================================================

        return {

            "status":
                "success",

            "total_questions":
                total_questions,

            "correct_answers":
                correct_count,

            "wrong_answers":
                wrong_count,

            "score_percentage":
                round(
                    score_percentage,
                    2
                ),

            "wrong_questions":
                wrong_questions,

            "topic_analysis":
                topic_analysis,

            "weak_topics":
                weak_topics
        }


# ==============================================================
# TEST
# ==============================================================

if __name__ == "__main__":

    questions = [

        {
            "id": 10,

            "question":
                "Which is commonly handled during data cleaning?",

            "correct_answer":
                "A",

            "topic":
                "Data Cleaning",

            "explanation":
                "Missing values are commonly handled during data cleaning."
        },

        {
            "id": 15,

            "question":
                "What is the purpose of data cleaning?",

            "correct_answer":
                "B",

            "topic":
                "Data Cleaning",

            "explanation":
                "Data cleaning removes or corrects incorrect and inconsistent data."
        }
    ]

    answers = {

        "10": "A",

        "15": "B"
    }

    analyzer = QuizResultAnalyzer()

    result = analyzer.analyze(
        questions,
        answers
    )

    print("\n===================================")
    print("          QUIZ RESULT")
    print("===================================")

    print(
        f"Score: "
        f"{result['score_percentage']}%"
    )

    print(
        f"Correct Answers: "
        f"{result['correct_answers']}"
    )

    print(
        f"Wrong Answers: "
        f"{result['wrong_answers']}"
    )

    print(
        f"Weak Topics: "
        f"{result['weak_topics']}"
    )