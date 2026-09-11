import json
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# HYBRID TOPIC MATCHER
# ============================================================

class TopicMatcher:

    def __init__(self, index_file="content_index.json"):

        self.index_file = index_file
        self.index = None
        self.sections = []
        self.vectorizer = None
        self.section_vectors = None

        self.load_index()
        self.build_index()

    # ========================================================
    # LOAD CONTENT INDEX
    # ========================================================

    def load_index(self):

        if not os.path.exists(self.index_file):

            raise FileNotFoundError(
                f"Content index not found: {self.index_file}"
            )

        with open(
            self.index_file,
            "r",
            encoding="utf-8"
        ) as file:

            self.index = json.load(file)

        self.sections = self.index.get(
            "sections",
            []
        )

        if not self.sections:

            raise ValueError(
                "No sections found in content index."
            )

        print(
            f"✅ Loaded {len(self.sections)} sections"
        )

    # ========================================================
    # BUILD TF-IDF INDEX
    # ========================================================

    def build_index(self):

        documents = [
            section.get("text", "")
            for section in self.sections
        ]

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english"
        )

        self.section_vectors = (
            self.vectorizer.fit_transform(documents)
        )

        print("✅ TF-IDF index created")

    # ========================================================
    # NORMALIZE TEXT
    # ========================================================

    def normalize_text(self, text):

        text = text.lower()

        text = re.sub(
            r'[^a-z0-9\s]',
            ' ',
            text
        )

        text = re.sub(
            r'\s+',
            ' ',
            text
        )

        return text.strip()

    # ========================================================
    # GET KEYWORDS
    # ========================================================

    def get_keywords(self, topic):

        normalized = self.normalize_text(topic)

        words = normalized.split()

        # Remove very common words
        stop_words = {
            "the",
            "a",
            "an",
            "of",
            "and",
            "with",
            "for",
            "to",
            "in",
            "on",
            "is",
            "are",
            "using",
            "basic",
            "introduction"
        }

        keywords = [
            word
            for word in words
            if word not in stop_words
        ]

        return keywords

    # ========================================================
    # KEYWORD SCORE
    # ========================================================

    def keyword_score(self, topic, section_text):

        keywords = self.get_keywords(topic)

        if not keywords:
            return 0.0

        section_text = self.normalize_text(
            section_text
        )

        section_words = set(
            section_text.split()
        )

        matched = 0

        for keyword in keywords:

            if keyword in section_words:
                matched += 1

        score = matched / len(keywords)

        return score

    # ========================================================
    # PHRASE SCORE
    # ========================================================

    def phrase_score(self, topic, section_text):

        topic_normalized = self.normalize_text(
            topic
        )

        section_normalized = self.normalize_text(
            section_text
        )

        if topic_normalized in section_normalized:

            return 1.0

        return 0.0

    # ========================================================
    # SEARCH
    # ========================================================

    def search(
        self,
        topic,
        top_k=5,
        min_score=0.05
    ):

        if not topic or not topic.strip():

            return []

        # ----------------------------------------------------
        # TF-IDF similarity
        # ----------------------------------------------------

        topic_vector = self.vectorizer.transform(
            [topic]
        )

        tfidf_scores = cosine_similarity(
            topic_vector,
            self.section_vectors
        )[0]

        results = []

        # ----------------------------------------------------
        # Calculate combined scores
        # ----------------------------------------------------

        for index, tfidf_score in enumerate(
            tfidf_scores
        ):

            section = self.sections[index]

            section_text = section.get(
                "text",
                ""
            )

            keyword_score = self.keyword_score(
                topic,
                section_text
            )

            phrase_score = self.phrase_score(
                topic,
                section_text
            )

            # ------------------------------------------------
            # Hybrid scoring
            #
            # TF-IDF      = 50%
            # Keyword     = 30%
            # Phrase      = 20%
            # ------------------------------------------------

            final_score = (
                (float(tfidf_score) * 0.50)
                +
                (keyword_score * 0.30)
                +
                (phrase_score * 0.20)
            )

            if final_score < min_score:
                continue

            results.append({

                "section_id":
                    section.get(
                        "section_id"
                    ),

                "pages":
                    section.get(
                        "pages",
                        []
                    ),

                "word_count":
                    section.get(
                        "word_count",
                        0
                    ),

                "tfidf_score":
                    round(
                        float(tfidf_score),
                        4
                    ),

                "keyword_score":
                    round(
                        keyword_score,
                        4
                    ),

                "phrase_score":
                    round(
                        phrase_score,
                        4
                    ),

                "final_score":
                    round(
                        final_score,
                        4
                    ),

                "text":
                    section_text
            })

        # ----------------------------------------------------
        # Sort by final score
        # ----------------------------------------------------

        results.sort(
            key=lambda item:
                item["final_score"],
            reverse=True
        )

        return results[:top_k]


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(
    topic,
    results
):

    print("\n" + "=" * 60)
    print("HYBRID TOPIC SEARCH RESULTS")
    print("=" * 60)

    print(f"\n🔎 Topic: {topic}")

    if not results:

        print("\n❌ No relevant sections found.")

        return

    print(
        f"\n📚 Relevant sections: "
        f"{len(results)}"
    )

    for number, result in enumerate(
        results,
        start=1
    ):

        pages = ", ".join(
            str(page)
            for page in result["pages"]
        )

        print(
            "\n" + "-" * 60
        )

        print(
            f"Result {number}"
        )

        print(
            f"Section ID: "
            f"{result['section_id']}"
        )

        print(
            f"Pages: {pages}"
        )

        print(
            f"TF-IDF Score: "
            f"{result['tfidf_score']}"
        )

        print(
            f"Keyword Score: "
            f"{result['keyword_score']}"
        )

        print(
            f"Phrase Score: "
            f"{result['phrase_score']}"
        )

        print(
            f"⭐ Final Score: "
            f"{result['final_score']}"
        )

        print("\nPreview:")

        print(
            result["text"][:500]
        )

        if len(result["text"]) > 500:

            print("...")


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("              HYBRID TOPIC MATCHER")
    print("=" * 60)

    try:

        matcher = TopicMatcher(
            "content_index.json"
        )

        # ----------------------------------------------------
        # Test topics
        # ----------------------------------------------------

        test_topics = [

            "Decision Tree",

            "Supervised Learning",

            "Naive Bayes",

            "Machine Learning"

        ]

        for topic in test_topics:

            results = matcher.search(
                topic,
                top_k=3
            )

            display_results(
                topic,
                results
            )

    except Exception as error:

        print("\n❌ Error:")
        print(error)

    print("\n" + "=" * 60)
    print("✅ HYBRID TOPIC MATCHER TEST COMPLETED!")
    print("=" * 60)