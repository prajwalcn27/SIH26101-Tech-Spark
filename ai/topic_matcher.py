import json
import re
from pathlib import Path


class TopicMatcher:

    def __init__(self, index_path=None):

        # Always locate content_index.json relative
        # to this Python file.
        BASE_DIR = Path(__file__).resolve().parent

        if index_path is None:
            self.index_path = BASE_DIR / "content_index.json"
        else:
            self.index_path = Path(index_path)

        self.index = None
        self.sections = []

        self.load_index()

    # =========================================================
    # LOAD CONTENT INDEX
    # =========================================================

    def load_index(self):

        if not self.index_path.exists():

            raise FileNotFoundError(
                f"Content index not found: {self.index_path}"
            )

        try:

            with open(
                self.index_path,
                "r",
                encoding="utf-8"
            ) as file:

                self.index = json.load(file)

        except json.JSONDecodeError as error:

            raise ValueError(
                f"Invalid content_index.json: {error}"
            )

        # -----------------------------------------------------
        # Read sections from the actual index structure
        # -----------------------------------------------------

        if isinstance(self.index, dict):

            self.sections = self.index.get(
                "sections",
                []
            )

        elif isinstance(self.index, list):

            self.sections = self.index

        else:

            self.sections = []

        print(
            f"✅ Content index loaded: "
            f"{self.index_path.name}"
        )

        print(
            f"📚 Indexed sections: "
            f"{len(self.sections)}"
        )

    # =========================================================
    # GET ALL CONTENT
    # =========================================================

    def get_all_content(self):

        return self.sections

    # =========================================================
    # NORMALIZE TEXT
    # =========================================================

    def normalize_text(self, text):

        if text is None:

            return ""

        text = str(text).lower()

        # Remove extra spaces
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # =========================================================
    # MATCH TOPIC
    # =========================================================

    def match_topic(
        self,
        topic,
        top_k=5
    ):
        """
        Find sections relevant to a topic.

        Returns:
            section_id
            pages
            text
            relevance
        """

        if not topic:

            return []

        topic_text = self.normalize_text(topic)

        results = []

        for section in self.sections:

            if not isinstance(section, dict):

                continue

            section_text = self.normalize_text(
                section.get("text", "")
            )

            if not section_text:

                continue

            score = 0

            # -------------------------------------------------
            # Exact phrase match
            # -------------------------------------------------

            if topic_text in section_text:

                score += 50

            # -------------------------------------------------
            # Individual keyword matching
            # -------------------------------------------------

            words = topic_text.split()

            matched_words = 0

            for word in words:

                if len(word) < 3:

                    continue

                if word in section_text:

                    matched_words += 1

            if words:

                keyword_score = (
                    matched_words / len(words)
                ) * 50

                score += keyword_score

            # -------------------------------------------------
            # Topic-specific keywords
            # -------------------------------------------------

            topic_keywords = {

                "data cleaning": [
                    "data cleaning",
                    "missing values",
                    "duplicate",
                    "incorrect data",
                    "inconsistent",
                    "outliers",
                    "standardization",
                    "validation"
                ],

                "data validation": [
                    "data validation",
                    "validation",
                    "required fields",
                    "unique",
                    "valid numbers"
                ],

                "decision tree": [
                    "decision tree",
                    "node",
                    "root",
                    "leaf",
                    "classification"
                ],

                "naive bayes": [
                    "naive bayes",
                    "bayes",
                    "probability",
                    "conditional probability"
                ],

                "statistics": [
                    "statistics",
                    "mean",
                    "median",
                    "mode",
                    "variance",
                    "standard deviation"
                ]
            }

            keywords = topic_keywords.get(
                topic_text,
                []
            )

            keyword_matches = 0

            for keyword in keywords:

                if keyword in section_text:

                    keyword_matches += 1

            if keywords:

                score += (
                    keyword_matches /
                    len(keywords)
                ) * 50

            # -------------------------------------------------
            # Add matching section
            # -------------------------------------------------

            if score > 0:

                pages = section.get(
                    "pages",
                    []
                )

                section_id = section.get(
                    "section_id"
                )

                word_count = section.get(
                    "word_count",
                    0
                )

                results.append({

                    "section_id": section_id,

                    "pages": pages,

                    "page": (
                        pages[0]
                        if pages
                        else None
                    ),

                    "text": section.get(
                        "text",
                        ""
                    ),

                    "word_count": word_count,

                    "relevance": round(
                        min(score, 100),
                        2
                    ),

                    "score": round(
                        min(score, 100),
                        2
                    ),

                    "topic": topic

                })

        # Sort highest relevance first
        results.sort(
            key=lambda item: item.get(
                "relevance",
                0
            ),
            reverse=True
        )

        return results[:top_k]

    # =========================================================
    # SEARCH
    # =========================================================

    def search(
        self,
        query,
        top_k=5
    ):
        """
        Search for a word or phrase
        across all indexed sections.
        """

        if not query:

            return []

        query_text = self.normalize_text(
            query
        )

        results = []

        for section in self.sections:

            if not isinstance(section, dict):

                continue

            text = self.normalize_text(
                section.get(
                    "text",
                    ""
                )
            )

            if query_text in text:

                pages = section.get(
                    "pages",
                    []
                )

                results.append({

                    "section_id": section.get(
                        "section_id"
                    ),

                    "pages": pages,

                    "page": (
                        pages[0]
                        if pages
                        else None
                    ),

                    "text": section.get(
                        "text",
                        ""
                    ),

                    "relevance": 100,

                    "score": 100

                })

        return results[:top_k]


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("TOPIC MATCHER TEST")
    print("=" * 60)

    try:

        matcher = TopicMatcher()

        print(
            "\n✅ TopicMatcher initialized successfully."
        )

        print(
            f"📚 Total indexed sections: "
            f"{len(matcher.sections)}"
        )

        # -----------------------------------------------------
        # Test Data Cleaning
        # -----------------------------------------------------

        test_topic = "Data Cleaning"

        results = matcher.match_topic(
            test_topic,
            top_k=5
        )

        print(
            f"\n🔎 Search topic: {test_topic}"
        )

        print(
            f"✅ Matches found: {len(results)}"
        )

        for index, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\n{index}. "
                f"Section {result.get('section_id')}"
            )

            print(
                f"   Pages: "
                f"{result.get('pages')}"
            )

            print(
                f"   Relevance: "
                f"{result.get('relevance')}%"
            )

            preview = result.get(
                "text",
                ""
            )[:200]

            print(
                f"   Preview: "
                f"{preview}..."
            )

        print("\n" + "=" * 60)
        print("✅ TOPIC MATCHER TEST COMPLETED")
        print("=" * 60)

    except Exception as error:

        print(
            "\n❌ Topic Matcher Test Failed:"
        )

        print(error)