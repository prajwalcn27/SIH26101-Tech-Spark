import json
from topic_matcher import TopicMatcher


class RecommendationEngine:

    def __init__(
        self,
        content_index_file="content_index.json"
    ):

        self.content_index_file = content_index_file

        # Create topic matcher
        self.matcher = TopicMatcher(
            content_index_file
        )

    def generate_recommendations(
        self,
        gap_analysis,
        top_k=2
    ):
        """
        Generate learning recommendations
        for weak topics identified by GapAnalyzer.
        """

        if not gap_analysis:

            print("❌ No gap analysis available.")

            return []

        weak_topics = gap_analysis.get(
            "weak_topics",
            []
        )

        if not weak_topics:

            print(
                "✅ No weak topics found. "
                "No recommendations required."
            )

            return []

        recommendations = []

        for topic in weak_topics:

            print(
                f"\n🔎 Finding learning material "
                f"for: {topic}"
            )

            # Search relevant sections
            results = self.matcher.search(
                topic,
                top_k=top_k
            )

            for result in results:

                recommendation = {

                    "topic": topic,

                    "section_id": result.get(
                        "section_id"
                    ),

                    "pages": result.get(
                        "pages"
                    ),

                    "score": result.get(
                        "score",
                        0
                    ),

                    "final_score": result.get(
                        "final_score",
                        result.get("score", 0)
                    ),

                    "word_count": result.get(
                        "word_count",
                        0
                    ),

                    "preview": result.get(
                        "text",
                        ""
                    )[:500]
                }

                recommendations.append(
                    recommendation
                )

        return recommendations

    def save_recommendations(
        self,
        recommendations,
        output_file="recommendations.json"
    ):

        data = {
            "recommendations": recommendations
        }

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"💾 Recommendations saved to: "
            f"{output_file}"
        )


if __name__ == "__main__":

    print("=" * 60)
    print("             RECOMMENDATION ENGINE")
    print("=" * 60)

    # Load gap analysis
    try:

        with open(
            "gap_analysis.json",
            "r",
            encoding="utf-8"
        ) as file:

            gap_analysis = json.load(file)

    except FileNotFoundError:

        print(
            "❌ gap_analysis.json not found."
        )

        exit()

    # Create engine
    engine = RecommendationEngine()

    # Generate recommendations
    recommendations = (
        engine.generate_recommendations(
            gap_analysis,
            top_k=2
        )
    )

    print("\n📚 RECOMMENDATIONS")
    print("-" * 60)

    for recommendation in recommendations:

        print(
            f"\n📘 Topic: "
            f"{recommendation['topic']}"
        )

        print(
            f"   Section: "
            f"{recommendation['section_id']}"
        )

        print(
            f"   Pages: "
            f"{recommendation['pages']}"
        )

        print(
            f"   Score: "
            f"{recommendation['final_score']}"
        )

    engine.save_recommendations(
        recommendations
    )

    print("\n" + "=" * 60)
    print("      RECOMMENDATION ENGINE TEST COMPLETED")
    print("=" * 60)