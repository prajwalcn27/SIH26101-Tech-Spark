import random


class QuizManager:

    def __init__(self, question_manager):
        """
        QuizManager uses QuestionManager
        to select questions for quizzes.
        """

        self.question_manager = question_manager

        print("✅ Quiz Manager initialized.")

    def create_quiz(
        self,
        number_of_questions=5,
        topic=None,
        difficulty=None
    ):
        """
        Create a quiz using questions from
        the QuestionManager.

        topic:
            Optional topic filter.

        difficulty:
            Optional difficulty filter.

        number_of_questions:
            Number of questions required.
        """

        questions = self.question_manager.get_questions(
            topic=topic,
            difficulty=difficulty
        )

        if not questions:

            print("❌ No questions available for quiz.")

            return []

        # If requested number is greater than
        # available questions, use all available.
        number_of_questions = min(
            number_of_questions,
            len(questions)
        )

        selected_questions = random.sample(
            questions,
            number_of_questions
        )

        return selected_questions

    def create_targeted_quiz(
        self,
        topic,
        number_of_questions=5
    ):
        """
        Create a quiz specifically for
        a weak topic.
        """

        print(
            f"\n🎯 Creating targeted quiz "
            f"for: {topic}"
        )

        return self.create_quiz(
            number_of_questions=number_of_questions,
            topic=topic
        )

    def create_difficulty_quiz(
        self,
        difficulty,
        number_of_questions=5
    ):
        """
        Create a quiz based on difficulty.
        """

        print(
            f"\n📈 Creating {difficulty} "
            f"difficulty quiz..."
        )

        return self.create_quiz(
            number_of_questions=number_of_questions,
            difficulty=difficulty
        )

    def create_topic_difficulty_quiz(
        self,
        topic,
        difficulty,
        number_of_questions=5
    ):
        """
        Create a quiz using both topic
        and difficulty.
        """

        print(
            f"\n🎯 Creating quiz:"
            f"\n   Topic      : {topic}"
            f"\n   Difficulty : {difficulty}"
        )

        return self.create_quiz(
            number_of_questions=number_of_questions,
            topic=topic,
            difficulty=difficulty
        )

    def display_quiz(self, questions):
        """
        Display quiz questions without
        showing the correct answers.
        """

        if not questions:

            print("❌ No quiz questions.")

            return

        print("\n")
        print("=" * 60)
        print("                    QUIZ")
        print("=" * 60)

        for index, question in enumerate(
            questions,
            start=1
        ):

            print(
                f"\n📘 Question {index}"
            )

            print(
                f"   Topic      : "
                f"{question.get('topic', 'General')}"
            )

            print(
                f"   Difficulty : "
                f"{question.get('difficulty', 'Unknown')}"
            )

            print(
                f"   {question['question']}"
            )

            options = question.get(
                "options",
                {}
            )

            for option, value in options.items():

                print(
                    f"      {option}. {value}"
                )

        print("\n" + "=" * 60)


if __name__ == "__main__":

    print("=" * 60)
    print("                  QUIZ MANAGER")
    print("=" * 60)

    # Import QuestionManager
    from question_manager import QuestionManager

    # Create QuestionManager
    question_manager = QuestionManager()

    # Remove duplicate questions
    question_manager.remove_duplicates()

    # Create QuizManager
    quiz_manager = QuizManager(
        question_manager
    )

    # --------------------------------------------------
    # TEST 1: General Quiz
    # --------------------------------------------------

    print("\n📝 TEST 1: General Quiz")

    quiz = quiz_manager.create_quiz(
        number_of_questions=3
    )

    quiz_manager.display_quiz(quiz)

    # --------------------------------------------------
    # TEST 2: Targeted Quiz
    # --------------------------------------------------

    print("\n🎯 TEST 2: Data Cleaning Quiz")

    targeted_quiz = (
        quiz_manager.create_targeted_quiz(
            topic="Data Cleaning",
            number_of_questions=2
        )
    )

    quiz_manager.display_quiz(
        targeted_quiz
    )

    # --------------------------------------------------
    # TEST 3: Difficulty Quiz
    # --------------------------------------------------

    print("\n📈 TEST 3: Easy Quiz")

    easy_quiz = (
        quiz_manager.create_difficulty_quiz(
            difficulty="Easy",
            number_of_questions=3
        )
    )

    quiz_manager.display_quiz(
        easy_quiz
    )

    # --------------------------------------------------
    # TEST 4: Topic + Difficulty
    # --------------------------------------------------

    print(
        "\n🎯 TEST 4: Easy Decision Tree Quiz"
    )

    topic_difficulty_quiz = (
        quiz_manager.create_topic_difficulty_quiz(
            topic="Decision Tree",
            difficulty="Easy",
            number_of_questions=2
        )
    )

    quiz_manager.display_quiz(
        topic_difficulty_quiz
    )

    print("\n" + "=" * 60)
    print("        QUIZ MANAGER TEST COMPLETED")
    print("=" * 60)