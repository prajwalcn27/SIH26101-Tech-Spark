import json
import os

from topic_matcher import TopicMatcher


# ============================================================
# CONTENT RETRIEVER
# ============================================================

class ContentRetriever:

    def __init__(
        self,
        index_file="content_index.json"
    ):

        self.matcher = TopicMatcher(
            index_file
        )

    # ========================================================
    # GET RELEVANT CONTENT
    # ========================================================

    def get_relevant_content(
        self,
        topic,
        top_k=3,
        max_words=1200
    ):

        results = self.matcher.search(
            topic,
            top_k=top_k
        )

        if not results:
            return {
                "topic": topic,
                "matches": [],
                "combined_text": ""
            }

        matches = []

        total_words = 0

        for result in results:

            text = result.get(
                "text",
                ""
            )

            word_count = len(
                text.split()
            )

            # ------------------------------------------------
            # Don't exceed requested content size
            # ------------------------------------------------

            if total_words + word_count > max_words:

                remaining_words = (
                    max_words - total_words
                )

                if remaining_words <= 0:
                    break

                words = text.split()

                text = " ".join(
                    words[:remaining_words]
                )

                word_count = len(
                    text.split()
                )

            matches.append({

                "section_id":
                    result["section_id"],

                "pages":
                    result["pages"],

                "score":
                    result["final_score"],

                "text":
                    text
            })

            total_words += word_count

            if total_words >= max_words:
                break

        # ----------------------------------------------------
        # Combine content
        # ----------------------------------------------------

        combined_parts = []

        for match in matches:

            combined_parts.append(
                f"--- Section "
                f"{match['section_id']} "
                f"| Pages: "
                f"{', '.join(map(str, match['pages']))} ---\n"
                f"{match['text']}"
            )

        combined_text = "\n\n".join(
            combined_parts
        )

        return {

            "topic": topic,

            "matches": matches,

            "combined_text":
                combined_text,

            "total_words":
                len(combined_text.split())
        }


# ============================================================
# DISPLAY CONTENT
# ============================================================

def display_content(data):

    print("\n" + "=" * 60)
    print("RETRIEVED LEARNING CONTENT")
    print("=" * 60)

    print(
        f"\n🔎 Topic: "
        f"{data['topic']}"
    )

    print(
        f"📚 Matching sections: "
        f"{len(data['matches'])}"
    )

    print(
        f"📝 Retrieved words: "
        f"{data.get('total_words', 0)}"
    )

    for match in data["matches"]:

        pages = ", ".join(
            str(page)
            for page in match["pages"]
        )

        print("\n" + "-" * 60)

        print(
            f"Section: "
            f"{match['section_id']}"
        )

        print(
            f"Pages: {pages}"
        )

        print(
            f"Relevance Score: "
            f"{match['score']}"
        )

    print("\n" + "-" * 60)
    print("CONTENT PREVIEW")
    print("-" * 60)

    print(
        data["combined_text"][:3000]
    )

    if len(data["combined_text"]) > 3000:
        print("\n... [content continues] ...")


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("              CONTENT RETRIEVER")
    print("=" * 60)

    try:

        retriever = ContentRetriever(
            "content_index.json"
        )

        # ----------------------------------------------------
        # Test topics
        # ----------------------------------------------------

        test_topics = [
            "Decision Tree",
            "Supervised Learning",
            "Naive Bayes"
        ]

        for topic in test_topics:

            data = retriever.get_relevant_content(
                topic,
                top_k=3,
                max_words=1200
            )

            display_content(data)

    except Exception as error:

        print("\n❌ Error:")
        print(error)

    print("\n" + "=" * 60)
    print("✅ CONTENT RETRIEVER TEST COMPLETED!")
    print("=" * 60)