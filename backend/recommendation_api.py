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

# Allow imports from document_processing
if DOCUMENT_PROCESSING_DIR not in sys.path:
    sys.path.append(DOCUMENT_PROCESSING_DIR)


# ==========================================
# IMPORT DOCUMENT PROCESSING
# ==========================================

from document_extractor import extract_text
from text_cleaner import clean_text
from topic_extractor import extract_topics


# ==========================================
# IMPORT RECOMMENDATION SYSTEM
# ==========================================

from recommender import (
    get_recommendation,
    get_all_recommendations,
    materials
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

    extension = os.path.splitext(
        filename
    )[1].lower()

    return extension in ALLOWED_EXTENSIONS


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "success",
        "message": "Tech Spark API is running"
    })


# ==========================================
# UPLOAD LEARNING MATERIAL
# ==========================================

@app.route("/upload-material", methods=["POST"])
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

    file.save(file_path)


    try:

        # ==================================
        # EXTRACT TEXT
        # ==================================

        extracted_text = extract_text(
            file_path
        )


        # ==================================
        # CLEAN TEXT
        # ==================================

        cleaned_text = clean_text(
            extracted_text
        )


        # ==================================
        # EXTRACT TOPICS
        # ==================================

        topics = extract_topics(
            cleaned_text
        )


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

        for material in materials:

            if material["file"].lower() == filename.lower():

                material["topics"] = topics

                material_exists = True

                break


        if not material_exists:

            materials.append({

                "title": file_name_without_extension,

                "file": filename,

                "topics": topics

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

@app.route("/materials", methods=["GET"])
def get_materials():

    material_list = []

    for material in materials:

        material_list.append({

            "title": material["title"],

            "file": material["file"],

            "topics": material["topics"]

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

@app.route("/recommend", methods=["POST"])
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


    if not weak_topic:

        return jsonify({

            "status": "error",

            "message": (
                "weak_topic is required"
            )

        }), 400


    # ==================================
    # GET BEST RECOMMENDATION
    # ==================================

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
        "Server running on "
        "http://127.0.0.1:5000"
    )
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )