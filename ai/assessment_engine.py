import json


class AssessmentEngine:

    def __init__(self):
        print("✅ Assessment Engine initialized.")

    def calculate_results(self, questions, answers):
        """
        Calculate overall score and topic-wise scores.

        questions:
            List of questions from QuestionManager

        answers:
            Dictionary:
            {
                question_id: selected_answer
            }
        """

        if not questions:
            print("❌ No questions provided.")
            return None

        total_questions = len(questions)
        correct_answers = 0

        topic_scores = {}

        for question in questions:

            question_id = str(question["id"])
            topic = question.get("topic", "General")
            correct_answer = question["correct_answer"]

            user_answer = answers.get(question_id)

            # Create topic entry if it doesn't exist
            if topic not in topic_scores:
                topic_scores[topic] = {
                    "correct": 0,
                    "total": 0
                }

            topic_scores[topic]["total"] += 1

            # Check answer
            if user_answer == correct_answer:
                correct_answers += 1
                topic_scores[topic]["correct"] += 1

        # Overall percentage
        overall_percentage = (
            correct_answers / total_questions
        ) * 100

        # Calculate topic percentages
        for topic in topic_scores:

            correct = topic_scores[topic]["correct"]
            total = topic_scores[topic]["total"]

            percentage = (correct / total) * 100

            topic_scores[topic]["percentage"] = round(
                percentage, 2
            )

        result = {
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "wrong_answers": total_questions - correct_answers,
            "overall_percentage": round(
                overall_percentage, 2
            ),
            "topic_scores": topic_scores
        }

        return result


def display_results(results):

    if not results:
        print("❌ No assessment results.")
        return

    print("\n")
    print("=" * 60)
    print("                 ASSESSMENT RESULTS")
    print("=" * 60)

    print(f"\n📊 Total Questions : {results['total_questions']}")
    print(f"✅ Correct Answers : {results['correct_answers']}")
    print(f"❌ Wrong Answers   : {results['wrong_answers']}")
    print(
        f"🎯 Overall Score   : "
        f"{results['overall_percentage']}%"
    )

    print("\n📚 TOPIC-WISE SCORES")
    print("-" * 60)

    for topic, data in results["topic_scores"].items():

        print(
            f"📘 {topic:<20} "
            f"{data['correct']}/{data['total']} "
            f"→ {data['percentage']}%"
        )

    print("=" * 60)


def load_question_bank(file_path="question_bank.json"):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        # Support both formats:
        # {"questions": [...]}
        # [...]
        if isinstance(data, dict):
            questions = data.get("questions", [])
        else:
            questions = data

        return questions

    except FileNotFoundError:

        print(
            f"❌ Question bank not found: {file_path}"
        )

        return []

    except json.JSONDecodeError:

        print(
            "❌ Invalid JSON format in question bank."
        )

        return []


if __name__ == "__main__":

    print("=" * 60)
    print("                 ASSESSMENT ENGINE")
    print("=" * 60)

    # Load question bank
    questions = load_question_bank()

    print(
        f"\n✅ Loaded {len(questions)} questions."
    )

    # Demo answers
    #
    # Question IDs:
    # 1 → Decision Tree
    # 2 → Decision Tree
    # 3 → Naive Bayes
    # 4 → Data Cleaning
    # 5 → Data Cleaning
    # 6 → Naive Bayes

    answers = {
        "1": "B",
        "2": "A",
        "3": "A",
        "4": "C",
        "5": "B",
        "6": "D"
    }

    # Create assessment engine
    engine = AssessmentEngine()

    # Calculate results
    results = engine.calculate_results(
        questions,
        answers
    )

    # Display results
    display_results(results)

    # Save results
    output_file = "assessment_results.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )

    print(
        f"\n💾 Results saved to: {output_file}"
    )

    print("\n" + "=" * 60)
    print("          ASSESSMENT ENGINE TEST COMPLETED")
    print("=" * 60)