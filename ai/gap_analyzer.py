"""
Competency Gap Analyzer
SIH26101 - Tech Spark

Identifies weak competencies/topics based on employee scores.
"""


class GapAnalyzer:

    def __init__(self, gap_threshold=60):

        self.gap_threshold = gap_threshold

    # ========================================================
    # ANALYZE COMPETENCY SCORES
    # ========================================================

    def analyze(self, topic_scores):

        competency_results = []

        weak_topics = []

        for topic, score in topic_scores.items():

            # Make sure score is numeric
            try:
                score = float(score)
            except (TypeError, ValueError):

                print(
                    f"⚠️ Invalid score for {topic}: {score}"
                )

                continue

            # ------------------------------------------------
            # Determine status and priority
            # ------------------------------------------------

            if score < self.gap_threshold:

                status = "GAP"
                priority = "HIGH"

                weak_topics.append(topic)

            elif score < 75:

                status = "NEEDS_IMPROVEMENT"
                priority = "MEDIUM"

                weak_topics.append(topic)

            else:

                status = "STRONG"
                priority = "LOW"

            # ------------------------------------------------
            # Store result
            # ------------------------------------------------

            competency_results.append({

                "topic": topic,

                "score": score,

                "status": status,

                "priority": priority
            })

        # ----------------------------------------------------
        # Sort lowest score first
        # ----------------------------------------------------

        competency_results.sort(
            key=lambda item: item["score"]
        )

        return {

            "competency_results":
                competency_results,

            "weak_topics":
                weak_topics
        }


# ============================================================
# DISPLAY GAP ANALYSIS
# ============================================================

def display_gap_analysis(gap_analysis):

    print("\n" + "=" * 60)
    print("COMPETENCY GAP ANALYSIS")
    print("=" * 60)

    print("\nCompetency Results:")

    for result in gap_analysis[
        "competency_results"
    ]:

        print(
            f"  {result['topic']:<25} "
            f"{result['score']:.2f}% "
            f"-> {result['status']} "
            f"[{result['priority']}]"
        )

    print("\nWeak Topics:")

    if gap_analysis["weak_topics"]:

        for topic in gap_analysis[
            "weak_topics"
        ]:

            print(
                f"  ⚠️ {topic}"
            )

    else:

        print(
            "  ✅ No weak topics found."
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    analyzer = GapAnalyzer(
        gap_threshold=60
    )

    test_scores = {

        "Decision Tree": 38,

        "Data Cleaning": 42,

        "Naive Bayes": 55,

        "Data Interpretation": 72,

        "Statistics": 76,

        "Excel": 82
    }

    result = analyzer.analyze(
        test_scores
    )

    display_gap_analysis(
        result
    )