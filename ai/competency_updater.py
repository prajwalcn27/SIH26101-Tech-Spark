"""
Competency Updater
SIH26101 - Tech Spark

Updates employee competency scores after completing a quiz.

Formula:

Updated Score =
Previous Score Ã— (1 - learning_weight)
+
Quiz Score Ã— learning_weight
"""


class CompetencyUpdater:

    def __init__(
        self,
        learning_weight=0.6
    ):

        self.learning_weight = (
            learning_weight
        )

    # ========================================================
    # UPDATE COMPETENCY
    # ========================================================

    def update_competency(
        self,
        previous_scores,
        quiz_results
    ):

        updated_competencies = {}

        # ----------------------------------------------------
        # Process every competency
        # ----------------------------------------------------

        for topic, previous_score in (
            previous_scores.items()
        ):

            previous_score = float(
                previous_score
            )

            # ------------------------------------------------
            # Check whether employee took a quiz for this
            # topic.
            # ------------------------------------------------

            quiz_data = quiz_results.get(
                topic
            )

            quiz_score = None

            # ------------------------------------------------
            # Quiz result can be:
            #
            # 100
            #
            # OR
            #
            # {
            #     "percentage": 100
            # }
            #
            # OR
            #
            # {
            #     "score": 100
            # }
            # ------------------------------------------------

            if quiz_data is not None:

                if isinstance(
                    quiz_data,
                    dict
                ):

                    quiz_score = quiz_data.get(
                        "percentage"
                    )

                    if quiz_score is None:

                        quiz_score = quiz_data.get(
                            "score"
                        )

                    if quiz_score is None:

                        quiz_score = quiz_data.get(
                            "quiz_score"
                        )

                else:

                    quiz_score = quiz_data

                # Convert to number

                if quiz_score is not None:

                    try:

                        quiz_score = float(
                            quiz_score
                        )

                    except (
                        TypeError,
                        ValueError
                    ):

                        quiz_score = None

            # ------------------------------------------------
            # Calculate updated score
            # ------------------------------------------------

            if quiz_score is not None:

                updated_score = (
                    previous_score
                    * (1 - self.learning_weight)
                    +
                    quiz_score
                    * self.learning_weight
                )

            else:

                updated_score = (
                    previous_score
                )

            # ------------------------------------------------
            # Determine status
            # ------------------------------------------------

            if updated_score < 60:

                status = "GAP"

            elif updated_score < 75:

                status = "NEEDS_IMPROVEMENT"

            else:

                status = "STRONG"

            updated_competencies[
                topic
            ] = {

                "previous_score":
                    previous_score,

                "quiz_score":
                    quiz_score,

                "updated_score":
                    round(
                        updated_score,
                        2
                    ),

                "status":
                    status
            }

        return {

            "updated_competencies":
                updated_competencies
        }


# ============================================================
# DISPLAY
# ============================================================

def display_updated_competencies(
    result
):

    print(
        "\n" + "=" * 60
    )

    print(
        "UPDATED COMPETENCY SCORES"
    )

    print(
        "=" * 60
    )

    competencies = result[
        "updated_competencies"
    ]

    for topic, data in (
        competencies.items()
    ):

        print(
            f"{topic:<25} "
            f"{data['previous_score']:.2f}% "
            f"â†’ "
            f"{data['updated_score']:.2f}% "
            f"({data['status']})"
        )

    print(
        "=" * 60
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    updater = CompetencyUpdater(
        learning_weight=0.4
    )

    previous_scores = {

        "Data Cleaning": 50,

        "Decision Tree": 50,

        "Naive Bayes": 100
    }

    quiz_results = {

        "Data Cleaning": {

            "correct": 2,

            "total": 2,

            "percentage": 100
        }
    }

    result = updater.update_competency(
        previous_scores,
        quiz_results
    )

    display_updated_competencies(
        result
    )