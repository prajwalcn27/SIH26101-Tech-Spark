import json
import random


class QuestionManager:

    def __init__(self, question_bank_file="question_bank.json"):

        self.question_bank_file = question_bank_file

        self.questions = self.load_question_bank()

    # ========================================================
    # LOAD QUESTION BANK
    # ========================================================

    def load_question_bank(self):

        try:

            with open(
                self.question_bank_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            questions = data.get(
                "questions",
                []
            )

            print(
                f"✅ Loaded {len(questions)} questions "
                f"from question bank."
            )

            return questions

        except FileNotFoundError:

            print(
                f"❌ Question bank not found: "
                f"{self.question_bank_file}"
            )

            return []

        except json.JSONDecodeError:

            print(
                "❌ Invalid question_bank.json file."
            )

            return []


    # ========================================================
    # GET ALL QUESTIONS
    # ========================================================

    def get_all_questions(self):

        return self.questions


    # ========================================================
    # GET QUESTIONS BY TOPIC
    # ========================================================

    def get_by_topic(self, topic, limit=None):

        matching_questions = [

            question
            for question in self.questions

            if question.get("topic", "").lower()
            == topic.lower()

        ]

        if limit:

            matching_questions = matching_questions[:limit]

        return matching_questions


    # ========================================================
    # GET QUESTIONS BY DIFFICULTY
    # ========================================================

    def get_by_difficulty(
        self,
        difficulty,
        limit=None
    ):

        matching_questions = [

            question
            for question in self.questions

            if question.get("difficulty", "").lower()
            == difficulty.lower()

        ]

        if limit:

            matching_questions = matching_questions[:limit]

        return matching_questions


    # ========================================================
    # GET QUESTIONS BY TOPIC AND DIFFICULTY
    # ========================================================

    def get_questions(
        self,
        topic=None,
        difficulty=None,
        limit=None
    ):

        matching_questions = self.questions

        # Filter by topic
        if topic:

            matching_questions = [

                question
                for question in matching_questions

                if question.get("topic", "").lower()
                == topic.lower()

            ]

        # Filter by difficulty
        if difficulty:

            matching_questions = [

                question
                for question in matching_questions

                if question.get("difficulty", "").lower()
                == difficulty.lower()

            ]

        # Limit number of questions
        if limit:

            matching_questions = matching_questions[:limit]

        return matching_questions


    # ========================================================
    # RANDOM QUESTION SELECTION
    # ========================================================

    def get_random_questions(
        self,
        number_of_questions=5,
        topic=None,
        difficulty=None
    ):

        matching_questions = self.get_questions(
            topic=topic,
            difficulty=difficulty
        )

        if not matching_questions:

            return []

        number_of_questions = min(
            number_of_questions,
            len(matching_questions)
        )

        return random.sample(
            matching_questions,
            number_of_questions
        )


    # ========================================================
    # REMOVE DUPLICATE QUESTIONS
    # ========================================================

    def remove_duplicates(self):

        unique_questions = []

        seen = set()

        for question in self.questions:

            question_text = question.get(
                "question",
                ""
            ).strip().lower()

            if question_text not in seen:

                seen.add(question_text)

                unique_questions.append(
                    question
                )

        self.questions = unique_questions

        return unique_questions


    # ========================================================
    # DISPLAY QUESTIONS
    # ========================================================

    def display_questions(self, questions):

        print("\n" + "=" * 60)
        print("                 SELECTED QUESTIONS")
        print("=" * 60)

        if not questions:

            print("❌ No questions found.")

            return

        for index, question in enumerate(
            questions,
            start=1
        ):

            print(
                f"\n📘 Question {index}"
            )

            print(
                f"   ID         : "
                f"{question.get('id')}"
            )

            print(
                f"   Topic      : "
                f"{question.get('topic')}"
            )

            print(
                f"   Difficulty : "
                f"{question.get('difficulty')}"
            )

            print(
                f"   Question   : "
                f"{question.get('question')}"
            )

            options = question.get(
                "options",
                {}
            )

            for key, value in options.items():

                print(
                    f"      {key}. {value}"
                )


# ============================================================
# TEST QUESTION MANAGER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("                 QUESTION MANAGER")
    print("=" * 60)

    manager = QuestionManager()

    # --------------------------------------------------------
    # Remove duplicate questions
    # --------------------------------------------------------

    manager.remove_duplicates()

    print(
        f"\n✅ Unique questions: "
        f"{len(manager.get_all_questions())}"
    )

    # --------------------------------------------------------
    # Test 1: Get Decision Tree questions
    # --------------------------------------------------------

    print(
        "\n🔎 Searching for Decision Tree questions..."
    )

    decision_tree_questions = manager.get_by_topic(
        "Decision Tree"
    )

    manager.display_questions(
        decision_tree_questions
    )

    # --------------------------------------------------------
    # Test 2: Get Easy questions
    # --------------------------------------------------------

    print(
        "\n🔎 Searching for Easy questions..."
    )

    easy_questions = manager.get_by_difficulty(
        "Easy"
    )

    manager.display_questions(
        easy_questions
    )

    # --------------------------------------------------------
    # Test 3: Random questions
    # --------------------------------------------------------

    print(
        "\n🎲 Selecting random questions..."
    )

    random_questions = manager.get_random_questions(
        number_of_questions=3
    )

    manager.display_questions(
        random_questions
    )

    # --------------------------------------------------------
    # Test 4: Topic + difficulty
    # --------------------------------------------------------

    print(
        "\n🎯 Searching for Easy Decision Tree questions..."
    )

    filtered_questions = manager.get_questions(
        topic="Decision Tree",
        difficulty="Easy"
    )

    manager.display_questions(
        filtered_questions
    )

    print("\n" + "=" * 60)
    print("           QUESTION MANAGER TEST COMPLETED")
    print("=" * 60)