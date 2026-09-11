import json


class QuizResultAnalyzer:

    def analyze(self, questions, answers):
        """
        Analyze quiz answers.

        questions:
            List of quiz questions.

        answers:
            Dictionary containing employee answers.

        Example:
        {
            "1": "B",
            "2": "A"
        }
        """

        if not questions:
            print("❌ No quiz questions provided.")
            return None

        total_questions = len(questions)
        correct_answers = 0

        wrong_questions = []
        topic_results = {}

        for question in questions:

            question_id = str(question["id"])
            topic = question.get(
                "topic",
                "General"
            )

            correct_answer = question[
                "correct_answer"
            ]

            employee_answer = answers.get(
                question_id
            )

            # Create topic entry
            if topic not in topic_results:

                topic_results[topic] = {
                    "correct": 0,
                    "total": 0
                }

            topic_results[topic]["total"] += 1

            # Check answer
            if employee_answer == correct_answer:

                correct_answers += 1

                topic_results[topic][
                    "correct"
                ] += 1

            else:

                wrong_questions.append({

                    "question_id": question_id,

                    "question": question.get(
                        "question",
                        ""
                    ),

                    "topic": topic,

                    "difficulty": question.get(
                        "difficulty",
                        "Unknown"
                    ),

                    "employee_answer":
                        employee_answer,

                    "correct_answer":
                        correct_answer,

                    "explanation":
                        question.get(
                            "explanation",
                            ""
                        )
                })

        # Calculate overall percentage
        score = (
            correct_answers /
            total_questions
        ) * 100

        # Calculate topic percentages
        for topic in topic_results:

            correct = topic_results[
                topic
            ]["correct"]

            total = topic_results[
                topic
            ]["total"]

            percentage = (
                correct / total
            ) * 100

            topic_results[topic][
                "percentage"
            ] = round(
                percentage,
                2
            )

        # Identify weak topics
        weak_topics = []

        for topic, data in topic_results.items():

            if data["percentage"] < 60:

                weak_topics.append(topic)

        result = {

            "total_questions":
                total_questions,

            "correct_answers":
                correct_answers,

            "wrong_answers":
                total_questions -
                correct_answers,

            "score":
                round(score, 2),

            "topic_results":
                topic_results,

            "weak_topics":
                weak_topics,

            "wrong_questions":
                wrong_questions
        }

        return result


def display_results(results):

    if not results:

        print("❌ No quiz result.")

        return

    print("\n")
    print("=" * 60)
    print("              QUIZ RESULT ANALYSIS")
    print("=" * 60)

    print(
        f"\n📊 Total Questions : "
        f"{results['total_questions']}"
    )

    print(
        f"✅ Correct Answers : "
        f"{results['correct_answers']}"
    )

    print(
        f"❌ Wrong Answers   : "
        f"{results['wrong_answers']}"
    )

    print(
        f"🎯 Quiz Score      : "
        f"{results['score']}%"
    )

    print("\n📚 TOPIC RESULTS")
    print("-" * 60)

    for topic, data in results[
        "topic_results"
    ].items():

        print(
            f"📘 {topic:<20} "
            f"{data['correct']}/"
            f"{data['total']} "
            f"→ {data['percentage']}%"
        )

    print("\n⚠️ WEAK TOPICS")

    if results["weak_topics"]:

        for topic in results[
            "weak_topics"
        ]:

            print(
                f"   • {topic}"
            )

    else:

        print(
            "   ✅ No weak topics identified."
        )

    print("\n❌ WRONG QUESTIONS")
    print("-" * 60)

    if results["wrong_questions"]:

        for item in results[
            "wrong_questions"
        ]:

            print(
                f"\nQuestion ID : "
                f"{item['question_id']}"
            )

            print(
                f"Topic       : "
                f"{item['topic']}"
            )

            print(
                f"Your Answer : "
                f"{item['employee_answer']}"
            )

            print(
                f"Correct     : "
                f"{item['correct_answer']}"
            )

    else:

        print(
            "   🎉 All answers are correct!"
        )

    print("=" * 60)


if __name__ == "__main__":

    print("=" * 60)
    print("           QUIZ RESULT ANALYZER")
    print("=" * 60)

    # Import QuestionManager and QuizManager
    from question_manager import QuestionManager
    from quiz_manager import QuizManager

    # Create QuestionManager
    question_manager = QuestionManager()

    # Remove duplicate questions
    question_manager.remove_duplicates()

    # Create QuizManager
    quiz_manager = QuizManager(
        question_manager
    )

    # Create a Data Cleaning quiz
    quiz = quiz_manager.create_targeted_quiz(
        topic="Data Cleaning",
        number_of_questions=2
    )

    # Display quiz
    quiz_manager.display_quiz(quiz)

    # --------------------------------------------------
    # DEMO EMPLOYEE ANSWERS
    # --------------------------------------------------

    print("\n📝 Processing employee answers...")

    # For Data Cleaning:
    #
    # Question 4 correct answer = B
    # Question 5 correct answer = A
    #
    # We intentionally give:
    #
    # Question 4 → C (wrong)
    # Question 5 → A (correct)

    answers = {}

    demo_answers = {
        "4": "C",
        "5": "A"
    }

    for question in quiz:

        question_id = str(
            question["id"]
        )

        answers[question_id] = (
            demo_answers.get(
                question_id,
                ""
            )
        )

    print("✅ Employee answers received.")

    # --------------------------------------------------
    # ANALYZE RESULTS
    # --------------------------------------------------

    analyzer = QuizResultAnalyzer()

    results = analyzer.analyze(
        quiz,
        answers
    )

    # Display results
    display_results(results)

    # --------------------------------------------------
    # SAVE RESULT
    # --------------------------------------------------

    output_file = "quiz_result_analysis.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\n💾 Result saved to: "
        f"{output_file}"
    )

    print("\n" + "=" * 60)
    print(
        "      QUIZ RESULT ANALYZER TEST COMPLETED"
    )
    print("=" * 60)