"""
Learning Profile
SIH26101 - Tech Spark

Maintains the employee's:
- competency scores
- weak topics
- recommendations
- quiz history
"""


class LearningProfile:

    def __init__(
        self,
        employee_id,
        employee_name
    ):

        self.profile = {

            "employee_id": employee_id,

            "employee_name": employee_name,

            "competencies": {},

            "weak_topics": [],

            "recommendations": [],

            "quiz_history": []
        }

    # ========================================================
    # ADD COMPETENCIES
    # ========================================================

    def add_competencies(
        self,
        competencies
    ):

        # ----------------------------------------------------
        # Format 1:
        #
        # {
        #     "Data Cleaning": 50,
        #     "Decision Tree": 50
        # }
        # ----------------------------------------------------

        if isinstance(
            competencies,
            dict
        ):

            for topic, score in competencies.items():

                # If value is a dictionary, try to extract
                # the score from it.

                if isinstance(
                    score,
                    dict
                ):

                    score = score.get(
                        "score",
                        score.get(
                            "updated_score",
                            score.get(
                                "final_score",
                                0
                            )
                        )
                    )

                self.profile[
                    "competencies"
                ][topic] = float(score)

        # ----------------------------------------------------
        # Format 2:
        #
        # [
        #     {
        #         "topic": "Data Cleaning",
        #         "score": 50
        #     }
        # ]
        # ----------------------------------------------------

        elif isinstance(
            competencies,
            list
        ):

            for result in competencies:

                if not isinstance(
                    result,
                    dict
                ):

                    continue

                topic = result.get(
                    "topic"
                )

                score = result.get(
                    "score",
                    result.get(
                        "updated_score",
                        result.get(
                            "final_score",
                            0
                        )
                    )
                )

                if topic is not None:

                    self.profile[
                        "competencies"
                    ][topic] = float(score)

    # ========================================================
    # ADD WEAK TOPICS
    # ========================================================

    def add_weak_topics(
        self,
        weak_topics
    ):

        if not weak_topics:

            return

        self.profile[
            "weak_topics"
        ] = list(
            weak_topics
        )

    # ========================================================
    # ADD RECOMMENDATIONS
    # ========================================================

    def add_recommendations(
        self,
        recommendations
    ):

        if not recommendations:

            return

        self.profile[
            "recommendations"
        ] = list(
            recommendations
        )

    # ========================================================
    # ADD QUIZ RESULT
    # ========================================================

    def add_quiz_result(
        self,
        quiz_result
    ):

        if not quiz_result:

            return

        self.profile[
            "quiz_history"
        ].append(
            quiz_result
        )

    # ========================================================
    # UPDATE COMPETENCIES
    # ========================================================

    def update_competencies(
        self,
        updated_competencies
    ):

        if not updated_competencies:

            return

        # ----------------------------------------------------
        # Dictionary format
        # ----------------------------------------------------

        if isinstance(
            updated_competencies,
            dict
        ):

            for topic, value in (
                updated_competencies.items()
            ):

                if isinstance(
                    value,
                    dict
                ):

                    score = value.get(
                        "updated_score",
                        value.get(
                            "score",
                            value.get(
                                "final_score",
                                0
                            )
                        )
                    )

                else:

                    score = value

                self.profile[
                    "competencies"
                ][topic] = float(score)

        # ----------------------------------------------------
        # List format
        # ----------------------------------------------------

        elif isinstance(
            updated_competencies,
            list
        ):

            for result in (
                updated_competencies
            ):

                if not isinstance(
                    result,
                    dict
                ):

                    continue

                topic = result.get(
                    "topic"
                )

                score = result.get(
                    "updated_score",
                    result.get(
                        "score",
                        result.get(
                            "final_score",
                            0
                        )
                    )
                )

                if topic is not None:

                    self.profile[
                        "competencies"
                    ][topic] = float(score)

    # ========================================================
    # DISPLAY PROFILE
    # ========================================================

    def display_profile(self):

        print("\n" + "=" * 60)

        print(
            "EMPLOYEE LEARNING PROFILE"
        )

        print("=" * 60)

        print(
            f"\nEmployee ID   : "
            f"{self.profile['employee_id']}"
        )

        print(
            f"Employee Name : "
            f"{self.profile['employee_name']}"
        )

        # ----------------------------------------------------
        # Competencies
        # ----------------------------------------------------

        print(
            "\n--- Competency Scores ---"
        )

        if self.profile[
            "competencies"
        ]:

            for topic, score in (
                self.profile[
                    "competencies"
                ].items()
            ):

                if score < 60:

                    status = "GAP"

                elif score < 75:

                    status = "NEEDS_IMPROVEMENT"

                else:

                    status = "STRONG"

                print(
                    f"{topic:<25} "
                    f"{score:.2f}% "
                    f"({status})"
                )

        else:

            print(
                "No competency data."
            )

        # ----------------------------------------------------
        # Weak Topics
        # ----------------------------------------------------

        print(
            "\n--- Weak Topics ---"
        )

        if self.profile[
            "weak_topics"
        ]:

            for topic in self.profile[
                "weak_topics"
            ]:

                print(
                    f"⚠️ {topic}"
                )

        else:

            print(
                "No weak topics."
            )

        # ----------------------------------------------------
        # Recommendations
        # ----------------------------------------------------

        print(
            "\n--- Recommendations ---"
        )

        if self.profile[
            "recommendations"
        ]:

            for recommendation in (
                self.profile[
                    "recommendations"
                ]
            ):

                topic = recommendation.get(
                    "topic",
                    "Unknown"
                )

                section = recommendation.get(
                    "section_id",
                    "Unknown"
                )

                print(
                    f"📘 {topic} "
                    f"→ Section {section}"
                )

        else:

            print(
                "No recommendations."
            )

        # ----------------------------------------------------
        # Quiz History
        # ----------------------------------------------------

        print(
            "\n--- Quiz History ---"
        )

        print(
            f"Total quizzes: "
            f"{len(self.profile['quiz_history'])}"
        )

        print("=" * 60)

    # ========================================================
    # SAVE PROFILE
    # ========================================================

    def save_profile(
        self,
        filename="learning_profile.json"
    ):

        import json

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.profile,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"✅ Learning profile saved: "
            f"{filename}"
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    profile = LearningProfile(
        employee_id="EMP001",
        employee_name="Demo Employee"
    )

    # Initial competencies

    profile.add_competencies({

        "Data Cleaning": 42,

        "Decision Tree": 50,

        "Naive Bayes": 55,

        "Statistics": 76,

        "Excel": 82
    })

    # Weak topics

    profile.add_weak_topics([

        "Data Cleaning",

        "Decision Tree",

        "Naive Bayes"
    ])

    # Recommendations

    profile.add_recommendations([

        {
            "topic": "Data Cleaning",
            "section_id": 9
        },

        {
            "topic": "Decision Tree",
            "section_id": 16
        }
    ])

    # Quiz result

    profile.add_quiz_result({

        "score": 100,

        "topic_results": {

            "Data Cleaning": {

                "correct": 2,

                "total": 2,

                "percentage": 100
            }
        }
    })

    # Updated competency

    profile.update_competencies({

        "Data Cleaning": 65.2

    })

    profile.display_profile()

    profile.save_profile()