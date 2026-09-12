import json
import os

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

    # ---------------------------------------------------------
    # GENERATE RECOMMENDATIONS
    # ---------------------------------------------------------
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

            print("❌ No gap analysis provided.")

            return []

        recommendations = []

        # -----------------------------------------------------
        # READ GAP ANALYSIS
        # -----------------------------------------------------
        for gap in gap_analysis:

            # Support different possible field names
            topic = (
                gap.get("topic")
                or gap.get("competency")
                or gap.get("name")
            )

            if not topic:
                continue

            level = (
                gap.get("level")
                or gap.get("gap_level")
                or gap.get("status")
                or "UNKNOWN"
            )

            score = (
                gap.get("score")
                or gap.get("percentage")
                or gap.get("competency_score")
            )

            # -------------------------------------------------
            # SEARCH RELEVANT CONTENT
            # -------------------------------------------------
            results = self.matcher.search(
                topic,
                top_k=top_k
            )

            # -------------------------------------------------
            # CREATE RECOMMENDATION
            # -------------------------------------------------
            topic_recommendation = {
                "topic": topic,
                "gap_level": level,
                "current_score": score,
                "recommended_materials": []
            }

            for result in results:

                topic_recommendation[
                    "recommended_materials"
                ].append({

                    "section_id": result.get(
                        "section_id"
                    ),

                    "pages": result.get(
                        "pages",
                        []
                    ),

                    "relevance_score": result.get(
                        "final_score",
                        0
                    ),

                    "tfidf_score": result.get(
                        "tfidf_score",
                        0
                    ),

                    "keyword_score": result.get(
                        "keyword_score",
                        0
                    ),

                    "phrase_score": result.get(
                        "phrase_score",
                        0
                    ),

                    "text_preview": result.get(
                        "text",
                        ""
                    )[:300]
                })

            recommendations.append(
                topic_recommendation
            )

        return recommendations

    # ---------------------------------------------------------
    # DISPLAY RECOMMENDATIONS
    # ---------------------------------------------------------
    def display_recommendations(
        self,
        recommendations
    ):

        print("\n" + "=" * 60)
        print("PERSONALIZED LEARNING RECOMMENDATIONS")
        print("=" * 60)

        if not recommendations:

            print("\n❌ No recommendations generated.")

            return

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            print(
                f"\nRecommendation {index}"
            )

            print("-" * 60)

            print(
                f"Topic: "
                f"{recommendation.get('topic')}"
            )

            print(
                f"Gap Level: "
                f"{recommendation.get('gap_level')}"
            )

            print(
                f"Current Score: "
                f"{recommendation.get('current_score')}"
            )

            materials = recommendation.get(
                "recommended_materials",
                []
            )

            if not materials:

                print(
                    "\nNo matching learning material found."
                )

                continue

            print(
                "\nRecommended Learning Sections:"
            )

            for material_index, material in enumerate(
                materials,
                start=1
            ):

                print(
                    f"\n  Material {material_index}"
                )

                print(
                    f"  Section ID: "
                    f"{material.get('section_id')}"
                )

                print(
                    f"  Pages: "
                    f"{material.get('pages', [])}"
                )

                print(
                    f"  Relevance Score: "
                    f"{material.get('relevance_score', 0)}"
                )

                print(
                    f"  Text: "
                    f"{material.get('text_preview', '')}..."
                )


# =============================================================
# TEST RECOMMENDATION ENGINE
# =============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("          RECOMMENDATION ENGINE")
    print("=" * 60)

    # ---------------------------------------------------------
    # Create recommendation engine
    # ---------------------------------------------------------
    engine = RecommendationEngine(
        "content_index.json"
    )

    # ---------------------------------------------------------
    # Sample gap analysis
    #
    # This simulates the output of GapAnalyzer.
    # In the complete system, this data will come from
    # the employee's assessment results.
    # ---------------------------------------------------------
    sample_gap_analysis = [

        {
            "topic": "Data Cleaning",
            "score": 45,
            "level": "HIGH"
        }

    ]

    print("\n[STEP 1] Gap Analysis")
    print("-" * 60)

    print(
        json.dumps(
            sample_gap_analysis,
            indent=4
        )
    )

    # ---------------------------------------------------------
    # Generate recommendations
    # ---------------------------------------------------------
    print("\n[STEP 2] Generating Recommendations")
    print("-" * 60)

    recommendations = (
        engine.generate_recommendations(
            sample_gap_analysis,
            top_k=2
        )
    )

    print(
        "✅ Recommendation generation completed."
    )

    # ---------------------------------------------------------
    # Display recommendations
    # ---------------------------------------------------------
    print("\n[STEP 3] Recommendations")

    engine.display_recommendations(
        recommendations
    )

    # ---------------------------------------------------------
    # Save result
    # ---------------------------------------------------------
    output_file = (
        "recommendation_result.json"
    )

    final_result = {

        "gap_analysis":
            sample_gap_analysis,

        "recommendations":
            recommendations
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            final_result,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 60)

    print(
        f"✅ Recommendation result saved as: "
        f"{output_file}"
    )

    print("=" * 60)