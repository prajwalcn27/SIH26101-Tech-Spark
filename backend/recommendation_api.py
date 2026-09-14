from flask import Flask, request, jsonify, send_from_directory
import os
import sys


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)

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
    """Check whether the uploaded file is supported."""

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

        print(
            "Starting complete AI learning cycle..."
        )

        result = run_complete_learning_cycle()

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
            "learning_cycle": result
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

    # Check whether file exists
    if "file" not in request.files:

        return jsonify({
            "status": "error",
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    # Check filename
    if file.filename == "":

        return jsonify({
            "status": "error",
            "message": "No file selected"
        }), 400

    # Check file format
    if not allowed_file(file.filename):

        return jsonify({
            "status": "error",
            "message": (
                "Unsupported file format. "
                "Allowed formats: PDF, PPTX, DOCX"
            )
        }), 400

    # Secure filename
    filename = os.path.basename(
        file.filename
    )

    # Save uploaded file
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

        file_name_without_extension = os.path.splitext(
            filename
        )[0]

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

        if isinstance(materials, list):

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
            "text_length": len(cleaned_text)
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

    if isinstance(materials, list):

        for material in materials:

            material_list.append({
                "title":
                    material.get("title"),

                "file":
                    material.get("file"),

                "topics":
                    material.get("topics", [])
            })

    return jsonify({
        "status": "success",
        "count": len(material_list),
        "materials": material_list
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
            "weak_topic": weak_topic,
            "recommendation": None
        }), 200

    return jsonify({
        "status": "success",
        "weak_topic": weak_topic,
        "recommendation": recommendation
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
        "weak_topics": weak_topics,
        "recommendations": recommendations
    }), 200


# ==========================================
# ERROR: FILE TOO LARGE
# ==========================================

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({
        "status": "error",
        "message": (
            "File too large. "
            "Maximum allowed size is 10 MB."
        )
    }), 413


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    print()
    print("===================================")
    print("       TECH SPARK API")
    print("===================================")
    print()

    print(
        "Supported formats:"
    )

    print(
        "PDF | PPTX | DOCX"
    )

    print()

    print(
        "AI endpoint:"
    )

    print(
        "POST /ai/learning-cycle"
    )

    print()

    print(
        "Server running on "
        "http://127.0.0.1:5000"
    )

    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )