from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)
CORS(app)

# Maximum upload size = 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

AI_DIR = os.path.join(
    BASE_DIR,
    "ai"
)

DOCUMENT_PROCESSING_DIR = os.path.join(
    BASE_DIR,
    "document_processing"
)

LEARNING_MATERIALS_DIR = os.path.join(
    BASE_DIR,
    "learning_materials"
)

os.makedirs(
    LEARNING_MATERIALS_DIR,
    exist_ok=True
)


# ==========================================
# ADD PROJECT DIRECTORIES TO PYTHON PATH
# ==========================================

if AI_DIR not in sys.path:
    sys.path.insert(0, AI_DIR)

if DOCUMENT_PROCESSING_DIR not in sys.path:
    sys.path.insert(0, DOCUMENT_PROCESSING_DIR)


# ==========================================
# IMPORT AI LEARNING PIPELINE
# ==========================================

try:
    from complete_learning_cycle import (
        run_complete_learning_cycle
    )

except ImportError as error:
    run_complete_learning_cycle = None

    print(
        f"Warning: AI learning cycle import failed: {error}"
    )


# ==========================================
# IMPORT DOCUMENT PROCESSING
# ==========================================

try:
    from document_extractor import extract_text
    from text_cleaner import clean_text
    from topic_extractor import extract_topics

except ImportError as error:
    extract_text = None
    clean_text = None
    extract_topics = None

    print(
        f"Warning: Document processing import failed: {error}"
    )


# ==========================================
# IMPORT EXISTING RECOMMENDATION SYSTEM
# ==========================================

try:
    from recommender import (
        get_recommendation,
        get_all_recommendations,
        materials
    )

except ImportError as error:
    get_recommendation = None
    get_all_recommendations = None
    materials = []

    print(
        f"Warning: Existing recommendation system "
        f"import failed: {error}"
    )


# ==========================================
# ALLOWED FILE TYPES
# ==========================================

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".pptx",
    ".docx"
}


def allowed_file(filename):
    """
    Check whether the uploaded file is supported.
    """

    if not filename:
        return False

    extension = os.path.splitext(
        filename
    )[1].lower()

    return extension in ALLOWED_EXTENSIONS


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route(
    "/health",
    methods=["GET"]
)
def health():

    return jsonify({
        "status": "success",
        "message": "Tech Spark API is running"
    })


# ==========================================
# AI LEARNING CYCLE
# ==========================================

@app.route(
    "/ai/learning-cycle",
    methods=["POST"]
)
def ai_learning_cycle():

    print()
    print("=" * 60)
    print("        AI LEARNING CYCLE API REQUEST")
    print("=" * 60)

    try:

        if run_complete_learning_cycle is None:

            return jsonify({
                "status": "error",
                "message": (
                    "AI learning cycle is not available."
                )
            }), 500


        # ======================================
        # GET REQUEST DATA
        # ======================================

        data = request.get_json(
            silent=True
        ) or {}

        weak_topics = data.get(
            "weak_topics",
            []
        )

        num_questions = data.get(
            "num_questions",
            5
        )

        # Optional material selection sent by the frontend.
        # If not provided, the API automatically finds a material
        # whose topics match the employee's weak topic.
        material_file = str(
            data.get("material_file", "")
        ).strip()

        material_title = str(
            data.get("material_title", "")
        ).strip()


        # ======================================
        # VALIDATE WEAK TOPICS
        # ======================================

        if not isinstance(
            weak_topics,
            list
        ):
            weak_topics = [weak_topics]

        weak_topics = [
            str(topic).strip()
            for topic in weak_topics
            if str(topic).strip()
        ]


        # ======================================
        # VALIDATE NUMBER OF QUESTIONS
        # ======================================

        try:

            num_questions = int(
                num_questions
            )

        except (
            ValueError,
            TypeError
        ):

            num_questions = 5


        if num_questions <= 0:
            num_questions = 5


        print(
            f"Weak Topics: {weak_topics}"
        )

        print(
            f"Number of Questions: {num_questions}"
        )


        # ======================================
        # FIND MATERIAL FOR AI QUIZ GENERATION
        # ======================================

        selected_material = None

        # 1. Prefer the exact file selected by the employee.
        if material_file and isinstance(materials, list):
            for material in materials:
                if str(material.get("file", "")).lower() == material_file.lower():
                    selected_material = material
                    break

        # 2. Otherwise find a material containing the weak topic.
        if selected_material is None and isinstance(materials, list):
            for material in materials:
                material_topics = material.get("topics", []) or []
                material_topics_lower = [
                    str(topic).strip().lower()
                    for topic in material_topics
                ]

                if any(
                    topic.lower() in material_topics_lower
                    or any(
                        topic.lower() in material_topic
                        or material_topic in topic.lower()
                        for material_topic in material_topics_lower
                    )
                    for topic in weak_topics
                ):
                    selected_material = material
                    break

        # 3. If there is still no exact topic match, use the first
        # available uploaded material.
        if selected_material is None and isinstance(materials, list) and materials:
            selected_material = materials[0]

        material_text = None

        if selected_material is not None:
            selected_file = str(
                selected_material.get("file", "")
            ).strip()

            selected_title = str(
                selected_material.get("title", "")
            ).strip()

            if not material_title:
                material_title = selected_title

            if not material_file:
                material_file = selected_file

            selected_base_name = os.path.splitext(
                os.path.basename(selected_file)
            )[0]

            extracted_text_path = os.path.join(
                DOCUMENT_PROCESSING_DIR,
                selected_base_name + "_extracted.txt"
            )

            if os.path.exists(extracted_text_path):
                with open(
                    extracted_text_path,
                    "r",
                    encoding="utf-8"
                ) as material_text_file:
                    material_text = material_text_file.read()

                print(
                    f"AI source material loaded: {selected_file}"
                )
                print(
                    f"AI source text length: {len(material_text)}"
                )
            else:
                print(
                    f"Extracted text not found: {extracted_text_path}"
                )

        if material_text:
            print(
                "AI quiz generation will use the uploaded material."
            )
        else:
            print(
                "No uploaded material text found. "
                "Using the existing quiz question bank fallback."
            )


        # ======================================
        # RUN COMPLETE AI LEARNING CYCLE
        # ======================================

        print(
            "Starting complete AI learning cycle..."
        )

        result = run_complete_learning_cycle(
            weak_topics=weak_topics,
            num_questions=num_questions,
            material_text=material_text,
            material_title=material_title
        )


        if result is None:

            return jsonify({
                "status": "error",
                "message": (
                    "AI learning cycle returned no result."
                )
            }), 500


        print(
            "AI learning cycle completed successfully."
        )


        return jsonify({
            "status": "success",
            "message": (
                "AI learning cycle completed successfully"
            ),
            "learning_cycle": result,
            "material": {
                "file": material_file,
                "title": material_title
            }
        }), 200


    except Exception as error:

        print()
        print(
            "AI LEARNING CYCLE ERROR:"
        )

        print(error)

        return jsonify({
            "status": "error",
            "message": "AI learning cycle failed",
            "error": str(error)
        }), 500


# ==========================================
# UPLOAD LEARNING MATERIAL
# ==========================================

@app.route(
    "/upload-material",
    methods=["POST"]
)
def upload_material():

    # ======================================
    # CHECK WHETHER FILE EXISTS
    # ======================================

    if "file" not in request.files:

        return jsonify({
            "status": "error",
            "message": "No file uploaded"
        }), 400


    file = request.files["file"]


    # ======================================
    # CHECK FILENAME
    # ======================================

    if file.filename == "":

        return jsonify({
            "status": "error",
            "message": "No file selected"
        }), 400


    # ======================================
    # CHECK FILE FORMAT
    # ======================================

    if not allowed_file(file.filename):

        return jsonify({
            "status": "error",
            "message": (
                "Unsupported file format. "
                "Allowed formats: PDF, PPTX, DOCX"
            )
        }), 400


    # ======================================
    # SECURE FILENAME
    # ======================================

    filename = os.path.basename(
        file.filename
    )


    # ======================================
    # SAVE UPLOADED FILE
    # ======================================

    file_path = os.path.join(
        LEARNING_MATERIALS_DIR,
        filename
    )


    try:

        file.save(file_path)


        # ==================================
        # EXTRACT TEXT
        # ==================================

        if extract_text is None:

            raise RuntimeError(
                "Document extraction module is unavailable."
            )


        extracted_text = extract_text(
            file_path
        )


        # ==================================
        # CLEAN TEXT
        # ==================================

        if clean_text is not None:

            cleaned_text = clean_text(
                extracted_text
            )

        else:

            cleaned_text = extracted_text


        # ==================================
        # EXTRACT TOPICS
        # ==================================

        if extract_topics is not None:

            topics = extract_topics(
                cleaned_text
            )

        else:

            topics = []


        # ==================================
        # SAVE EXTRACTED TEXT
        # ==================================

        file_name_without_extension = (
            os.path.splitext(filename)[0]
        )


        text_filename = (
            file_name_without_extension
            + "_extracted.txt"
        )


        text_file_path = os.path.join(
            DOCUMENT_PROCESSING_DIR,
            text_filename
        )


        with open(
            text_file_path,
            "w",
            encoding="utf-8"
        ) as text_file:

            text_file.write(
                cleaned_text
            )


        # ==================================
        # ADD MATERIAL TO RECOMMENDER
        # ==================================

        material_exists = False


        if isinstance(
            materials,
            list
        ):

            for material in materials:

                if material.get(
                    "file",
                    ""
                ).lower() == filename.lower():

                    material["topics"] = topics

                    material_exists = True

                    break


            if not material_exists:

                materials.append({
                    "title":
                        file_name_without_extension,

                    "file":
                        filename,

                    "topics":
                        topics
                })


        # ==================================
        # RESPONSE
        # ==================================

        return jsonify({

            "status": "success",

            "message": (
                "Learning material uploaded "
                "and processed successfully"
            ),

            "file": filename,

            "file_type": os.path.splitext(
                filename
            )[1].lower(),

            "text_file": text_filename,

            "topics": topics,

            "text_length": len(
                cleaned_text
            )

        }), 200


    except Exception as error:

        # Remove file if processing failed
        if os.path.exists(file_path):

            os.remove(file_path)


        return jsonify({

            "status": "error",

            "message": (
                "Document processing failed"
            ),

            "error": str(error)

        }), 500


# ==========================================
# GET ALL MATERIALS
# ==========================================

@app.route(
    "/materials",
    methods=["GET"]
)
def get_materials():

    material_list = []


    if isinstance(
        materials,
        list
    ):

        for material in materials:

            material_list.append({

                "title":
                    material.get("title"),

                "file":
                    material.get("file"),

                "topics":
                    material.get(
                        "topics",
                        []
                    )

            })


    return jsonify({

        "status": "success",

        "count": len(
            material_list
        ),

        "materials":
            material_list

    })


# ==========================================
# SERVE LEARNING MATERIAL
# ==========================================

@app.route(
    "/material/<path:filename>",
    methods=["GET"]
)
def serve_material(filename):

    return send_from_directory(
        LEARNING_MATERIALS_DIR,
        filename
    )


# ==========================================
# RECOMMEND MATERIAL
# ==========================================

@app.route(
    "/recommend",
    methods=["POST"]
)
def recommend():

    data = request.get_json(
        silent=True
    )


    if not data:

        return jsonify({
            "status": "error",
            "message": "JSON data is required"
        }), 400


    weak_topic = data.get(
        "weak_topic"
    )


    # Also support the new "topic" field
    # without breaking the old API.

    if not weak_topic:

        weak_topic = data.get(
            "topic"
        )


    if not weak_topic:

        return jsonify({
            "status": "error",
            "message": (
                "weak_topic or topic is required"
            )
        }), 400


    # ==================================
    # GET BEST RECOMMENDATION
    # ==================================

    if get_recommendation is None:

        return jsonify({
            "status": "error",
            "message": (
                "Recommendation system is unavailable."
            )
        }), 500


    recommendation = get_recommendation(
        weak_topic,
        materials
    )


    if recommendation is None:

        return jsonify({

            "status": "success",

            "message": (
                "No suitable learning "
                "material found"
            ),

            "weak_topic":
                weak_topic,

            "recommendation":
                None

        }), 200


    return jsonify({

        "status": "success",

        "weak_topic":
            weak_topic,

        "recommendation":
            recommendation

    }), 200


# ==========================================
# RECOMMEND FOR MULTIPLE WEAK TOPICS
# ==========================================

@app.route(
    "/recommend-multiple",
    methods=["POST"]
)
def recommend_multiple():

    data = request.get_json(
        silent=True
    )


    if not data:

        return jsonify({
            "status": "error",
            "message": "JSON data is required"
        }), 400


    weak_topics = data.get(
        "weak_topics"
    )


    if not isinstance(
        weak_topics,
        list
    ) or not weak_topics:

        return jsonify({
            "status": "error",
            "message": (
                "weak_topics must be "
                "a non-empty list"
            )
        }), 400


    if get_all_recommendations is None:

        return jsonify({
            "status": "error",
            "message": (
                "Recommendation system is unavailable."
            )
        }), 500


    recommendations = get_all_recommendations(
        weak_topics,
        materials
    )


    return jsonify({

        "status": "success",

        "weak_topics":
            weak_topics,

        "recommendations":
            recommendations

    }), 200

# ==========================================
# SUBMIT EMPLOYEE QUIZ
# ==========================================

@app.route(
    "/quiz/submit",
    methods=["POST"]
)
def submit_quiz():

    print()
    print("=" * 60)
    print("           QUIZ SUBMISSION API")
    print("=" * 60)

    try:

        # ======================================
        # GET REQUEST DATA
        # ======================================

        data = request.get_json(
            silent=True
        ) or {}

        questions = data.get(
            "questions",
            []
        )

        answers = data.get(
            "answers",
            {}
        )

        weak_topic = data.get(
            "weak_topic",
            "Missing Values"
        )


        # ======================================
        # VALIDATION
        # ======================================

        if not questions:

            return jsonify({
                "status": "error",
                "message": "Questions are required"
            }), 400


        if not isinstance(answers, dict):

            return jsonify({
                "status": "error",
                "message": "Answers must be an object"
            }), 400


        # ======================================
        # CALCULATE RESULT
        # ======================================

        total_questions = len(
            questions
        )

        correct_answers = 0

        wrong_answers = 0

        mistakes = []


        for question in questions:

            question_id = str(
                question.get(
                    "id",
                    ""
                )
            )

            correct_answer = str(
                question.get(
                    "correct_answer",
                    ""
                )
            ).strip().upper()

            employee_answer = str(
                answers.get(
                    question_id,
                    ""
                )
            ).strip().upper()


            if (
                employee_answer
                and
                employee_answer == correct_answer
            ):

                correct_answers += 1

            else:

                wrong_answers += 1

                mistakes.append({

                    "question_id":
                        question_id,

                    "question":
                        question.get(
                            "question",
                            ""
                        ),

                    "employee_answer":
                        employee_answer
                        if employee_answer
                        else "Not Answered",

                    "correct_answer":
                        correct_answer,

                    "topic":
                        question.get(
                            "topic",
                            weak_topic
                        )

                })


        # ======================================
        # SCORE
        # ======================================

        if total_questions > 0:

            score_percentage = round(
                (
                    correct_answers
                    /
                    total_questions
                ) * 100,
                2
            )

        else:

            score_percentage = 0


        # ======================================
        # DETERMINE WEAK TOPICS
        # ======================================

        weak_topics = []

        topic_stats = {}


        for question in questions:

            topic = question.get(
                "topic",
                weak_topic
            )

            if topic not in topic_stats:

                topic_stats[topic] = {
                    "total": 0,
                    "correct": 0
                }


            topic_stats[topic]["total"] += 1


            question_id = str(
                question.get(
                    "id",
                    ""
                )
            )

            employee_answer = str(
                answers.get(
                    question_id,
                    ""
                )
            ).strip().upper()

            correct_answer = str(
                question.get(
                    "correct_answer",
                    ""
                )
            ).strip().upper()


            if (
                employee_answer
                and
                employee_answer == correct_answer
            ):

                topic_stats[topic]["correct"] += 1


        for topic, stats in topic_stats.items():

            topic_score = (
                stats["correct"]
                /
                stats["total"]
            ) * 100


            if topic_score < 50:

                weak_topics.append(
                    topic
                )


        # If no topic is below 50%,
        # use the selected weak topic.

        if not weak_topics:

            weak_topics = [
                weak_topic
            ]


        # ======================================
        # UPDATED COMPETENCY
        # ======================================

        updated_competency = round(
            score_percentage,
            2
        )


        # ======================================
        # RESPONSE
        # ======================================

        result = {

            "score_percentage":
                score_percentage,

            "correct_answers":
                correct_answers,

            "wrong_answers":
                wrong_answers,

            "total_questions":
                total_questions,

            "weak_topics":
                weak_topics,

            "mistakes":
                mistakes,

            "topic_statistics":
                topic_stats,

            "updated_competency":
                updated_competency

        }


        print(
            f"Total Questions: "
            f"{total_questions}"
        )

        print(
            f"Correct Answers: "
            f"{correct_answers}"
        )

        print(
            f"Wrong Answers: "
            f"{wrong_answers}"
        )

        print(
            f"Score: "
            f"{score_percentage}%"
        )

        print(
            f"Weak Topics: "
            f"{weak_topics}"
        )

        print(
            "Quiz submission processed successfully."
        )


        return jsonify({

            "status":
                "success",

            "message":
                "Quiz submitted successfully",

            "quiz_result":
                result

        }), 200


    except Exception as error:

        print()
        print(
            "QUIZ SUBMISSION ERROR:"
        )

        print(error)


        return jsonify({

            "status":
                "error",

            "message":
                "Quiz submission failed",

            "error":
                str(error)

        }), 500
        # ==========================================
# START FLASK SERVER
# ==========================================

if __name__ == "__main__":

    print()
    print("===================================")
    print("       TECH SPARK API")
    print("===================================")

    print()
    print("Supported formats:")
    print("PDF | PPTX | DOCX")

    print()
    print("AI endpoint:")
    print("POST /ai/learning-cycle")

    print()
    print("Quiz endpoint:")
    print("POST /quiz/submit")

    print()
    print("Server running on http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )