import json
from pathlib import Path


class TopicMatcher:
    """
    Matches competency topics with learning materials from content_index.json.

    Supports the current Tech Spark content_index.json format:

    {
        "materials": [
            {
                "file": "Data_Cleaning.pdf",
                "title": "Data Cleaning",
                "topics": [
                    "Missing Values",
                    "Duplicate Records",
                    "Data Formatting",
                    "Data Validation",
                    "Data Cleaning"
                ]
            }
        ]
    }

    It also supports an optional "sections" list if a richer index is
    generated later.
    """

    def __init__(self, index_path=None):

        BASE_DIR = Path(__file__).resolve().parent

        if index_path is None:
            index_path = BASE_DIR / "content_index.json"
        else:
            index_path = Path(index_path)

            if not index_path.is_absolute():
                index_path = BASE_DIR / index_path

        self.index_path = index_path
        self.materials = []
        self.sections = []

        self._load_index()

    # =========================================================
    # LOAD CONTENT INDEX
    # =========================================================

    def _load_index(self):

        try:

            if not self.index_path.exists():

                print(
                    f"âŒ Content index not found: "
                    f"{self.index_path}"
                )

                return

            with open(
                self.index_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            # -------------------------------------------------
            # Current format: materials
            # -------------------------------------------------

            materials = data.get(
                "materials",
                []
            )

            if isinstance(materials, list):

                self.materials = materials

            # -------------------------------------------------
            # Optional richer format: sections
            # -------------------------------------------------

            sections = data.get(
                "sections",
                []
            )

            if isinstance(sections, list):

                self.sections = sections

            # -------------------------------------------------
            # If sections exist, use them directly.
            # Otherwise convert materials into searchable
            # material records.
            # -------------------------------------------------

            if self.sections:

                print(
                    f"ðŸ“š Indexed sections: "
                    f"{len(self.sections)}"
                )

            else:

                print(
                    f"ðŸ“š Indexed sections: "
                    f"{len(self.materials)} materials"
                )

            print(
                f"âœ… Content index loaded: "
                f"{self.index_path.name}"
            )

        except json.JSONDecodeError as error:

            print(
                "âŒ Invalid content_index.json:"
            )

            print(error)

        except Exception as error:

            print(
                "âŒ Failed to load content index:"
            )

            print(error)

    # =========================================================
    # NORMALIZE TEXT
    # =========================================================

    @staticmethod
    def _normalize(text):

        if text is None:
            return ""

        return " ".join(
            str(text)
            .lower()
            .strip()
            .split()
        )

    # =========================================================
    # TOPIC RELATIONSHIP
    # =========================================================

    @staticmethod
    def _is_topic_match(
        requested_topic,
        material_topics,
        material_title=""
    ):

        requested = TopicMatcher._normalize(
            requested_topic
        )

        if not requested:
            return False

        topics = [
            TopicMatcher._normalize(topic)
            for topic in material_topics
        ]

        title = TopicMatcher._normalize(
            material_title
        )

        # Exact topic match
        if requested in topics:
            return True

        # Topic contained in a broader topic/title
        for topic in topics:

            if (
                requested in topic
                or topic in requested
            ):
                return True

        if requested in title or title in requested:
            return True

        # Known competency sub-topic mapping.
        # This is important for the current project:
        # Missing Values is part of Data Cleaning.
        related_topics = {

            "missing values": [
                "data cleaning"
            ],

            "duplicate records": [
                "data cleaning"
            ],

            "data formatting": [
                "data cleaning"
            ],

            "data validation": [
                "data cleaning"
            ],

            "data cleaning": [
                "data cleaning"
            ]
        }

        for related_topic in related_topics.get(
            requested,
            []
        ):

            if (
                related_topic in topics
                or related_topic in title
            ):
                return True

        return False

    # =========================================================
    # MATCH TOPIC
    # =========================================================

    def match_topic(
        self,
        topic,
        top_k=2
    ):

        if not topic:
            return []

        results = []

        # -----------------------------------------------------
        # 1. Search richer section index first
        # -----------------------------------------------------

        for index, section in enumerate(
            self.sections
        ):

            if not isinstance(
                section,
                dict
            ):
                continue

            section_topics = (
                section.get("topics")
                or section.get("topic")
                or []
            )

            if isinstance(
                section_topics,
                str
            ):
                section_topics = [
                    section_topics
                ]

            title = (
                section.get("title")
                or section.get("name")
                or ""
            )

            if self._is_topic_match(
                topic,
                section_topics,
                title
            ):

                results.append({

                    "section_id":
                        section.get(
                            "section_id",
                            f"section_{index + 1}"
                        ),

                    "page":
                        section.get(
                            "page"
                        ),

                    "pages":
                        section.get(
                            "pages",
                            []
                        ),

                    "text":
                        section.get(
                            "text",
                            ""
                        ),

                    "file":
                        section.get(
                            "file",
                            ""
                        ),

                    "title":
                        title,

                    "relevance":
                        self._calculate_score(
                            topic,
                            section_topics,
                            title
                        )
                })

        # -----------------------------------------------------
        # 2. Search current materials format
        # -----------------------------------------------------

        for index, material in enumerate(
            self.materials
        ):

            if not isinstance(
                material,
                dict
            ):
                continue

            material_topics = material.get(
                "topics",
                []
            )

            if isinstance(
                material_topics,
                str
            ):
                material_topics = [
                    material_topics
                ]

            title = material.get(
                "title",
                ""
            )

            if not self._is_topic_match(
                topic,
                material_topics,
                title
            ):
                continue

            score = self._calculate_score(
                topic,
                material_topics,
                title
            )

            results.append({

                "section_id":
                    material.get(
                        "section_id",
                        f"material_{index + 1}"
                    ),

                "page":
                    material.get(
                        "page"
                    ),

                "pages":
                    material.get(
                        "pages",
                        []
                    ),

                "text":
                    material.get(
                        "text",
                        ""
                    ),

                "file":
                    material.get(
                        "file",
                        ""
                    ),

                "title":
                    title,

                "relevance":
                    score
            })

        # -----------------------------------------------------
        # Remove duplicates
        # -----------------------------------------------------

        unique = {}

        for result in results:

            key = (
                result.get("file"),
                result.get("section_id")
            )

            unique[key] = result

        results = list(
            unique.values()
        )

        # Highest relevance first
        results.sort(
            key=lambda item:
                item.get(
                    "relevance",
                    0
                ),
            reverse=True
        )

        return results[:top_k]

    # =========================================================
    # RELEVANCE SCORE
    # =========================================================

    @staticmethod
    def _calculate_score(
        requested_topic,
        material_topics,
        title
    ):

        requested = TopicMatcher._normalize(
            requested_topic
        )

        normalized_topics = [
            TopicMatcher._normalize(topic)
            for topic in material_topics
        ]

        normalized_title = (
            TopicMatcher._normalize(title)
        )

        # Exact topic = strongest match
        if requested in normalized_topics:
            return 100.0

        # Sub-topic covered by broader topic
        if requested == "missing values":
            if "data cleaning" in normalized_topics:
                return 95.0

        if requested == "duplicate records":
            if "data cleaning" in normalized_topics:
                return 90.0

        if requested == "data formatting":
            if "data cleaning" in normalized_topics:
                return 90.0

        if requested == "data validation":
            if "data cleaning" in normalized_topics:
                return 90.0

        # Partial topic match
        for item in normalized_topics:

            if (
                requested in item
                or item in requested
            ):
                return 85.0

        if (
            requested in normalized_title
            or normalized_title in requested
        ):
            return 80.0

        return 50.0


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("TOPIC MATCHER TEST")
    print("=" * 60)

    matcher = TopicMatcher()

    test_topics = [
        "Missing Values",
        "Data Cleaning",
        "Duplicate Records",
        "Data Validation"
    ]

    for topic in test_topics:

        print(
            f"\nðŸ” Searching for: {topic}"
        )

        matches = matcher.match_topic(
            topic,
            top_k=2
        )

        if not matches:

            print(
                "   âŒ No matching material."
            )

        else:

            for match in matches:

                print(
                    f"   âœ… {match.get('title')} "
                    f"| {match.get('file')} "
                    f"| Relevance: "
                    f"{match.get('relevance')}%"
                )

    print("\n" + "=" * 60)
    print("âœ… TOPIC MATCHER TEST COMPLETED")
    print("=" * 60)
