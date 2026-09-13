from pathlib import Path

from topic_matcher import TopicMatcher


class RecommendationEngine:

    def __init__(self, index_path=None):

        BASE_DIR = Path(__file__).resolve().parent

        if index_path is None:
            index_path = BASE_DIR / "content_index.json"
        else:
            index_path = Path(index_path)

            if not index_path.is_absolute():
                index_path = BASE_DIR / index_path

        print(
            f"📂 Recommendation index: {index_path}"
        )

        self.matcher = TopicMatcher(
            index_path=index_path
        )

    # =========================================================
    # GENERATE RECOMMENDATIONS
    # =========================================================

    def generate_recommendations(
        self,
        gap_analysis,
        top_k=2
    ):

        recommendations = []

        if not gap_analysis:
            return recommendations

        # -----------------------------------------------------
        # Handle different gap-analysis formats
        # -----------------------------------------------------

        if isinstance(gap_analysis, dict):

            if "competency_results" in gap_analysis:

                gaps = gap_analysis[
                    "competency_results"
                ]

            elif "weak_topics" in gap_analysis:

                gaps = []

                for topic in gap_analysis[
                    "weak_topics"
                ]:

                    gaps.append({
                        "topic": topic,
                        "competency": topic,
                        "name": topic,
                        "score": 0,
                        "percentage": 0,
                        "competency_score": 0,
                        "status": "GAP",
                        "gap_level": "HIGH"
                    })

            else:

                gaps = [gap_analysis]

        elif isinstance(gap_analysis, list):

            gaps = gap_analysis

        else:

            return recommendations

        # -----------------------------------------------------
        # Process each competency gap
        # -----------------------------------------------------

        for gap in gaps:

            if not isinstance(gap, dict):
                continue

            topic = (
                gap.get("topic")
                or gap.get("competency")
                or gap.get("name")
            )

            if not topic:
                continue

            # -------------------------------------------------
            # Current competency score
            # -------------------------------------------------

            if gap.get("score") is not None:

                current_score = gap.get("score")

            elif gap.get("percentage") is not None:

                current_score = gap.get("percentage")

            else:

                current_score = gap.get(
                    "competency_score",
                    0
                )

            # -------------------------------------------------
            # Gap level
            # -------------------------------------------------

            gap_level = (
                gap.get("gap_level")
                or gap.get("priority")
                or gap.get("level")
                or gap.get("status")
                or "MEDIUM"
            )

            # -------------------------------------------------
            # Find relevant learning material
            # -------------------------------------------------

            matched_materials = self.matcher.match_topic(
                topic,
                top_k=top_k
            )

            recommended_materials = []

            for material in matched_materials:

                relevance = material.get(
                    "relevance",
                    material.get(
                        "score",
                        0
                    )
                )

                pages = material.get(
                    "pages",
                    []
                )

                page = material.get(
                    "page"
                )

                text = material.get(
                    "text",
                    ""
                )

                # Short preview
                preview = text[:250]

                recommended_materials.append({

                    "section_id": material.get(
                        "section_id"
                    ),

                    "page": page,

                    "pages": pages,

                    # Keep both field names
                    # for compatibility
                    "relevance": relevance,

                    "relevance_score": relevance,

                    "score": relevance,

                    "preview": preview,

                    "text": text,

                    "topic": topic

                })

            # -------------------------------------------------
            # Create recommendation
            # -------------------------------------------------

            recommendation = {

                "topic": topic,

                "gap_level": gap_level,

                "current_score": current_score,

                "recommended_materials":
                    recommended_materials

            }

            recommendations.append(
                recommendation
            )

        # -----------------------------------------------------
        # Weakest competency first
        # -----------------------------------------------------

        recommendations.sort(
            key=lambda item: item.get(
                "current_score",
                100
            )
        )

        return recommendations


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("RECOMMENDATION ENGINE TEST")
    print("=" * 60)

    try:

        engine = RecommendationEngine()

        test_gap_analysis = {

            "competency_results": [

                {
                    "topic": "Data Cleaning",
                    "score": 0,
                    "percentage": 0,
                    "status": "GAP",
                    "gap_level": "HIGH"
                },

                {
                    "topic": "Decision Tree",
                    "score": 50,
                    "percentage": 50,
                    "status": "GAP",
                    "gap_level": "HIGH"
                }

            ],

            "weak_topics": [
                "Data Cleaning",
                "Decision Tree"
            ]

        }

        recommendations = (
            engine.generate_recommendations(
                test_gap_analysis,
                top_k=2
            )
        )

        print(
            f"\n✅ Recommendations generated: "
            f"{len(recommendations)}"
        )

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            print(
                f"\n{index}. "
                f"{recommendation['topic']}"
            )

            print(
                f"   Gap Level: "
                f"{recommendation['gap_level']}"
            )

            print(
                f"   Current Score: "
                f"{recommendation['current_score']}%"
            )

            materials = recommendation.get(
                "recommended_materials",
                []
            )

            print(
                f"   Materials Found: "
                f"{len(materials)}"
            )

            for material in materials:

                print(
                    f"      • Section "
                    f"{material.get('section_id')} "
                    f"| Relevance: "
                    f"{material.get('relevance_score')}%"
                )

        print("\n" + "=" * 60)
        print("✅ RECOMMENDATION ENGINE TEST COMPLETED")
        print("=" * 60)

    except Exception as error:

        print(
            "\n❌ Recommendation Engine Test Failed:"
        )

        print(error)