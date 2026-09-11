from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json


# --------------------------------------------------
# 1. Recommend materials for one weak topic
# --------------------------------------------------

def recommend_material(weak_topic, materials):

    material_texts = [
        " ".join(material["topics"])
        for material in materials
    ]

    vectorizer = TfidfVectorizer()

    material_vectors = vectorizer.fit_transform(material_texts)
    weak_topic_vector = vectorizer.transform([weak_topic])

    similarity_scores = cosine_similarity(
        weak_topic_vector,
        material_vectors
    )[0]

    recommendations = []

    for i, score in enumerate(similarity_scores):

        if score >= 0.1:

            recommendations.append({
                "title": materials[i]["title"],
                "file": materials[i]["file"],
                "score": float(f"{score * 100:.2f}"),
                "reason": (
                    f"Recommended because it covers "
                    f"the weak topic: {weak_topic}"
                )
            })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:1]


# --------------------------------------------------
# 2. Get best recommendation
# --------------------------------------------------

def get_recommendation(weak_topic, materials):

    results = recommend_material(
        weak_topic,
        materials
    )

    if results:
        return results[0]

    return None


# --------------------------------------------------
# 3. Get recommendations for multiple weak topics
# --------------------------------------------------

def get_all_recommendations(weak_topics, materials):

    all_recommendations = []

    for weak_topic in weak_topics:

        best_material = get_recommendation(
            weak_topic,
            materials
        )

        if best_material:

            all_recommendations.append({
                "weak_topic": weak_topic,
                "title": best_material["title"],
                "file": best_material["file"],
                "similarity": best_material["score"],
                "reason": best_material["reason"]
            })

    return all_recommendations


# --------------------------------------------------
# 4. Learning materials
# --------------------------------------------------

materials = [

    {
        "title": "Data Cleaning",
        "file": "Data_Cleaning.pdf",
        "topics": [
            "Missing Values",
            "Duplicate Records",
            "Incorrect Data",
            "Inconsistent Formats",
            "Outliers",
            "Standardization",
            "Validation",
            "Data Quality",
            "Data Cleaning"
        ]
    },

    {
        "title": "Excel Basics",
        "file": "Excel_Basics.pdf",
        "topics": [
            "Excel",
            "Formulas",
            "Charts",
            "Data Analysis"
        ]
    },

    {
        "title": "Statistics Basics",
        "file": "Statistics_Basics.pdf",
        "topics": [
            "Statistics",
            "Mean",
            "Median",
            "Probability",
            "Data Analysis"
        ]
    }

]


# --------------------------------------------------
# 5. Run only when this file is executed directly
# --------------------------------------------------

if __name__ == "__main__":

    # Read weak topics
    with open(
        "weak_topics.txt",
        "r",
        encoding="utf-8"
    ) as file:

        weak_topics = [
            line.strip()
            for line in file
            if line.strip()
        ]


    # Generate recommendations
    all_recommendations = get_all_recommendations(
        weak_topics,
        materials
    )


    # Display recommendations
    print("\n===================================")
    print("     TECH SPARK RECOMMENDATIONS")
    print("===================================\n")


    for recommendation in all_recommendations:

        print("Weak Topic:",
              recommendation["weak_topic"])

        print("Recommended Material:",
              recommendation["title"])

        print("File:",
              recommendation["file"])

        print("Similarity:",
              recommendation["similarity"], "%")

        print("Reason:",
              recommendation["reason"])

        print("-----------------------------------")


    # Save recommendations as JSON
    with open(
        "recommendations.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_recommendations,
            file,
            indent=4
        )


    print("\nRecommendations saved to:")
    print("recommendations.json")