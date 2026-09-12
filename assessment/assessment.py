# SIH26101 - Tech Spark
# Member 6 - Assessment, Scoring & Progress


questions = [
    {
        "question": "Which Excel feature is used to summarize large amounts of data?",
        "topic": "Excel",
        "correct_answer": "B"
    },
    {
        "question": "Which Excel function is commonly used to add numbers?",
        "topic": "Excel",
        "correct_answer": "A"
    },
    {
        "question": "What is the process of removing incorrect or duplicate data called?",
        "topic": "Data Cleaning",
        "correct_answer": "C"
    },
    {
        "question": "Which technique can be used to handle missing values?",
        "topic": "Data Cleaning",
        "correct_answer": "B"
    },
    {
        "question": "What is the average value of a dataset called?",
        "topic": "Statistics",
        "correct_answer": "A"
    },
    {
        "question": "Which measure represents the middle value of ordered data?",
        "topic": "Statistics",
        "correct_answer": "C"
    },
    {
        "question": "What does a chart help us do?",
        "topic": "Data Interpretation",
        "correct_answer": "B"
    },
    {
        "question": "What is data interpretation?",
        "topic": "Data Interpretation",
        "correct_answer": "A"
    },
    {
        "question": "Which Excel feature can group and summarize data?",
        "topic": "Excel",
        "correct_answer": "D"
    },
    {
        "question": "Which is an important step before analyzing data?",
        "topic": "Data Cleaning",
        "correct_answer": "C"
    }
]


def calculate_score(questions, answers):

    total_questions = len(questions)
    correct_answers = 0

    topic_total = {}
    topic_correct = {}

    for i, question in enumerate(questions):

        topic = question["topic"]

        # Count total questions for each topic
        topic_total[topic] = topic_total.get(topic, 0) + 1

        # Check employee answer
        if answers[i].upper() == question["correct_answer"]:
            correct_answers += 1
            topic_correct[topic] = topic_correct.get(topic, 0) + 1
        else:
            topic_correct.setdefault(topic, 0)

    # Calculate overall percentage
    overall_percentage = (correct_answers / total_questions) * 100

    # Calculate topic-wise percentage
    topic_scores = {}

    for topic in topic_total:
        score = (
            topic_correct[topic]
            / topic_total[topic]
        ) * 100
        topic_scores[topic] = score
    
    # Find weakest topic
    weakest_topic = min(
        topic_scores,
        key=topic_scores.get
    )

    # Identify whether there is a significant competency gap
    if topic_scores[weakest_topic] >= 70:
        weakest_topic = "No significant gap"

    return overall_percentage, topic_scores, weakest_topic


def get_competency_level(score):
    """
    Convert a percentage score into a competency level.
    """

    if score >= 80:
        return "Strong"
    elif score >= 60:
        return "Moderate"
    else:
        return "Needs Improvement"
    
def run_assessment():

    print("\n======================================")
    print("       SIH26101 EMPLOYEE ASSESSMENT")
    print("======================================")

    print("\nAnswer each question using A, B, C or D.")

    answers = []

    options = {

        1: [
            "A. Filter",
            "B. Pivot Table",
            "C. Sort",
            "D. Format"
        ],

        2: [
            "A. SUM",
            "B. COUNT",
            "C. MAX",
            "D. MIN"
        ],

        3: [
            "A. Data Entry",
            "B. Data Export",
            "C. Data Cleaning",
            "D. Data Storage"
        ],

        4: [
            "A. Delete everything",
            "B. Fill or replace values",
            "C. Ignore data",
            "D. Duplicate data"
        ],

        5: [
            "A. Mean",
            "B. Range",
            "C. Mode",
            "D. Variance"
        ],

        6: [
            "A. Mean",
            "B. Range",
            "C. Median",
            "D. Sum"
        ],

        7: [
            "A. Delete data",
            "B. Visualize data",
            "C. Encrypt data",
            "D. Store passwords"
        ],

        8: [
            "A. Understanding and analyzing data",
            "B. Deleting data",
            "C. Copying data",
            "D. Formatting passwords"
        ],

        9: [
            "A. Filter",
            "B. Sort",
            "C. Chart",
            "D. Pivot Table"
        ],

        10: [
            "A. Printing",
            "B. Formatting",
            "C. Cleaning data",
            "D. Sharing data"
        ]
    }

    # Ask all questions
    for i, question in enumerate(questions, start=1):

        print(f"\nQ{i}. {question['question']}")

        for option in options[i]:
            print(option)

        answer = input("Your answer: ").strip().upper()

        while answer not in ["A", "B", "C", "D"]:

            print("Please enter only A, B, C or D.")

            answer = input(
                "Your answer: "
            ).strip().upper()

        answers.append(answer)

    # Calculate result
    overall, topic_scores, weakest_topic = calculate_score(
        questions,
        answers
    )

    # Display result
    print("\n======================================")
    print("          ASSESSMENT RESULT")
    print("======================================")

    print(f"\nOverall Score: {overall:.2f}%")

    print("\nTopic-wise Performance:")

    for topic, score in topic_scores.items():
        level = get_competency_level(score)

        print(
            f"{topic}: {score:.2f}% → {level}"
        )
    # Create progress data
    progress_data = {
        "overall_score": round(overall, 2),
        "topic_scores": {
            topic: round(score, 2)
            for topic, score in topic_scores.items()
        },
        "competency_levels": {
            topic: get_competency_level(score)
            for topic, score in topic_scores.items()
        },
        "weakest_topic": weakest_topic
    }

    print("\n--------------------------------------")

    if weakest_topic == "No significant gap":

        print("Competency Status: GOOD")
        print("No significant competency gap identified.")

        print("\nRecommendation:")
        print("Continue with the next learning activity.")

    else:

        print(f"Weakest Topic: {weakest_topic}")
        print(f"Competency Gap Identified: {weakest_topic}")

        print("\nRecommendation:")
        print(
            f"Focus on learning materials related to "
            f"{weakest_topic}."
        )

        print("--------------------------------------")

if __name__ == "__main__":
    run_assessment()