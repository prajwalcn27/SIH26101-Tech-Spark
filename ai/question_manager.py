import json
import random
from pathlib import Path


class QuestionManager:

    def __init__(self, question_bank_path=None):

        BASE_DIR = Path(__file__).resolve().parent

        if question_bank_path is None:
            self.question_bank_path = BASE_DIR / "question_bank.json"
        else:
            self.question_bank_path = Path(question_bank_path)

            if not self.question_bank_path.is_absolute():
                self.question_bank_path = (
                    BASE_DIR / self.question_bank_path
                )

        self.questions = []

        self.load_questions()

    # =========================================================
    # LOAD QUESTIONS
    # =========================================================

    def load_questions(self):

        try:

            if not self.question_bank_path.exists():

                print(
                    f"❌ Question bank not found: "
                    f"{self.question_bank_path}"
                )

                self.questions = []
                return

            with open(
                self.question_bank_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, list):

                self.questions = data

            elif isinstance(data, dict):

                if "questions" in data:

                    self.questions = data["questions"]

                elif "question_bank" in data:

                    self.questions = data["question_bank"]

                else:

                    self.questions = []

            else:

                self.questions = []

            print(
                f"✅ Loaded {len(self.questions)} "
                f"questions from question bank."
            )

        except json.JSONDecodeError as error:

            print(
                f"❌ Invalid question_bank.json: {error}"
            )

            self.questions = []

        except Exception as error:

            print(
                f"❌ Error loading question bank: {error}"
            )

            self.questions = []

    # =========================================================
    # GET ALL QUESTIONS
    # =========================================================

    def get_all_questions(self):

        return self.questions

    # =========================================================
    # GET QUESTIONS
    # =========================================================

    def get_questions(
        self,
        topic=None,
        difficulty=None,
        number_of_questions=None,
        count=None
    ):
        """
        Flexible question retrieval method.

        Supports:

            get_questions()

            get_questions(topic="Data Cleaning")

            get_questions(
                topic="Data Cleaning",
                number_of_questions=2
            )

            get_questions(count=5)
        """

        selected_questions = self.questions.copy()

        # -----------------------------------------------------
        # Filter by topic
        # -----------------------------------------------------

        if topic:

            topic_lower = str(
                topic
            ).strip().lower()

            selected_questions = [

                question

                for question in selected_questions

                if str(
                    question.get(
                        "topic",
                        ""
                    )
                ).strip().lower()
                == topic_lower

            ]

        # -----------------------------------------------------
        # Filter by difficulty
        # -----------------------------------------------------

        if difficulty:

            difficulty_lower = str(
                difficulty
            ).strip().lower()

            selected_questions = [

                question

                for question in selected_questions

                if str(
                    question.get(
                        "difficulty",
                        ""
                    )
                ).strip().lower()
                == difficulty_lower

            ]

        # -----------------------------------------------------
        # Determine requested number
        # -----------------------------------------------------

        if number_of_questions is not None:

            requested_count = number_of_questions

        elif count is not None:

            requested_count = count

        else:

            # If no number is specified,
            # return all matching questions.
            requested_count = len(
                selected_questions
            )

        try:

            requested_count = int(
                requested_count
            )

        except (
            ValueError,
            TypeError
        ):

            requested_count = len(
                selected_questions
            )

        # -----------------------------------------------------
        # Randomize only when a limited number is requested
        # -----------------------------------------------------

        if requested_count < len(
            selected_questions
        ):

            random.shuffle(
                selected_questions
            )

        return selected_questions[
            :requested_count
        ]

    # =========================================================
    # GET QUESTION COUNT
    # =========================================================

    def get_question_count(self):

        return len(
            self.questions
        )

    # =========================================================
    # REMOVE DUPLICATES
    # =========================================================

    def remove_duplicates(self):

        unique_questions = []

        seen = set()

        for question in self.questions:

            question_text = str(
                question.get(
                    "question",
                    ""
                )
            ).strip().lower()

            if (
                question_text
                and question_text not in seen
            ):

                seen.add(
                    question_text
                )

                unique_questions.append(
                    question
                )

        self.questions = unique_questions

        return self.questions

    # =========================================================
    # GET RANDOM QUESTIONS
    # =========================================================

    def get_random_questions(
        self,
        count=None,
        number_of_questions=None
    ):
        """
        Get random questions.

        Supports both:

            get_random_questions(count=5)

        and:

            get_random_questions(
                number_of_questions=5
            )
        """

        if number_of_questions is not None:

            count = number_of_questions

        if count is None:

            count = 5

        if not self.questions:

            return []

        try:

            count = int(count)

        except (
            ValueError,
            TypeError
        ):

            count = 5

        available_questions = (
            self.questions.copy()
        )

        random.shuffle(
            available_questions
        )

        return available_questions[
            :min(
                count,
                len(available_questions)
            )
        ]

    # =========================================================
    # GET QUESTIONS BY TOPIC
    # =========================================================

    def get_questions_by_topic(
        self,
        topic
    ):

        if not topic:

            return []

        topic_lower = str(
            topic
        ).strip().lower()

        return [

            question

            for question in self.questions

            if str(
                question.get(
                    "topic",
                    ""
                )
            ).strip().lower()
            == topic_lower

        ]

    # =========================================================
    # GET QUESTIONS BY DIFFICULTY
    # =========================================================

    def get_questions_by_difficulty(
        self,
        difficulty
    ):

        if not difficulty:

            return []

        difficulty_lower = str(
            difficulty
        ).strip().lower()

        return [

            question

            for question in self.questions

            if str(
                question.get(
                    "difficulty",
                    ""
                )
            ).strip().lower()
            == difficulty_lower

        ]

    # =========================================================
    # GET TARGETED QUESTIONS
    # =========================================================

    def get_targeted_questions(
        self,
        topic=None,
        difficulty=None,
        count=5
    ):

        return self.get_questions(
            topic=topic,
            difficulty=difficulty,
            count=count
        )


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("QUESTION MANAGER TEST")
    print("=" * 60)

    manager = QuestionManager()

    print(
        f"\n📚 Total Questions: "
        f"{manager.get_question_count()}"
    )

    manager.remove_duplicates()

    print(
        f"📚 After duplicate removal: "
        f"{manager.get_question_count()}"
    )

    # Test normal get_questions()
    questions = manager.get_questions()

    print(
        f"\n✅ get_questions(): "
        f"{len(questions)} questions"
    )

    # Test limited questions
    questions = manager.get_questions(
        number_of_questions=3
    )

    print(
        f"✅ get_questions(number_of_questions=3): "
        f"{len(questions)} questions"
    )

    # Test topic
    questions = manager.get_questions(
        topic="Data Cleaning",
        number_of_questions=2
    )

    print(
        f"✅ Data Cleaning questions: "
        f"{len(questions)}"
    )

    # Test random questions
    questions = manager.get_random_questions(
        number_of_questions=3
    )

    print(
        f"✅ Random questions: "
        f"{len(questions)}"
    )

    print("\n" + "=" * 60)
    print("✅ QUESTION MANAGER TEST COMPLETED")
    print("=" * 60)