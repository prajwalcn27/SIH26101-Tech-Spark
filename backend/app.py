from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import os


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)
CORS(app)


# =========================================================
# FILE UPLOAD CONFIGURATION
# =========================================================

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "uploads"
)

ALLOWED_EXTENSIONS = {
    "pdf",
    "ppt",
    "pptx",
    "doc",
    "docx"
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================================================
# DATABASE CONNECTION
# =========================================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sih26101_db"
)


# =========================================================
# HELPER - ALLOWED FILE
# =========================================================

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# HOME
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "success": True,
        "message": "SIH26101 Tech Spark Backend is running"
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health", methods=["GET"])
def health_check():

    return jsonify({
        "success": True,
        "message": "Backend is healthy"
    })


# =========================================================
# PROJECT INFORMATION
# =========================================================

@app.route("/api/project", methods=["GET"])
def project_info():

    return jsonify({
        "success": True,
        "project": "AI-enabled Skill Intelligence and Learning Platform",
        "team": "Tech Spark",
        "problem_statement": "SIH26101"
    })


# =========================================================
# USERS
# =========================================================

@app.route("/api/users", methods=["GET"])
def get_users():

    try:

        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                name,
                email,
                role,
                created_at
            FROM users
        """)

        users = cursor.fetchall()

        cursor.close()

        return jsonify({
            "success": True,
            "users": users
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# LOGIN
# =========================================================

@app.route("/api/login", methods=["POST"])
def login():

    try:

        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:

            return jsonify({
                "success": False,
                "message": "Email and password are required"
            }), 400

        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM users
            WHERE email = %s
        """, (email,))

        user = cursor.fetchone()

        cursor.close()

        if not user:

            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        stored_password = user.get("password")

        password_valid = False

        # Hashed password
        try:

            password_valid = check_password_hash(
                stored_password,
                password
            )

        except Exception:

            password_valid = False

        # Prototype fallback for plaintext passwords
        if not password_valid and stored_password == password:
            password_valid = True

        if not password_valid:

            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user.get("name"),
                "email": user.get("email"),
                "role": user.get("role")
            }
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# COMPETENCIES
# =========================================================

@app.route("/api/competencies", methods=["GET"])
def get_competencies():

    try:

        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                name,
                domain,
                description
            FROM competencies
            ORDER BY id
        """)

        competencies = cursor.fetchall()

        cursor.close()

        return jsonify({
            "success": True,
            "competencies": competencies
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# LEARNING MATERIALS - GET ALL
# =========================================================

@app.route("/api/learning-materials", methods=["GET"])
def get_learning_materials():

    try:

        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                title,
                description,
                file_name,
                file_path,
                file_type,
                uploaded_by,
                source,
                created_at
            FROM learning_materials
            ORDER BY id DESC
        """)

        materials = cursor.fetchall()

        cursor.close()

        return jsonify({
            "success": True,
            "materials": materials
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# LEARNING MATERIAL - UPLOAD
# =========================================================

@app.route(
    "/api/learning-materials/upload",
    methods=["POST"]
)
def upload_learning_material():

    try:

        # Check file
        if "file" not in request.files:

            return jsonify({
                "success": False,
                "message": "No file provided"
            }), 400

        file = request.files["file"]

        if file.filename == "":

            return jsonify({
                "success": False,
                "message": "No file selected"
            }), 400

        # Check file type
        if not allowed_file(file.filename):

            return jsonify({
                "success": False,
                "message": "File type not allowed"
            }), 400

        # Get form data
        title = request.form.get("title")
        description = request.form.get(
            "description",
            ""
        )

        uploaded_by = request.form.get(
            "uploaded_by"
        )

        source = request.form.get(
            "source",
            "Local"
        )

        if not title:

            return jsonify({
                "success": False,
                "message": "Title is required"
            }), 400

        if not uploaded_by:

            return jsonify({
                "success": False,
                "message": "uploaded_by is required"
            }), 400

        # Secure filename
        original_filename = secure_filename(
            file.filename
        )

        # Save file
        file.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                original_filename
            )
        )

        # File extension
        file_type = original_filename.rsplit(
            ".",
            1
        )[1].lower()

        # Database insert
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO learning_materials
            (
                title,
                description,
                file_name,
                file_path,
                file_type,
                uploaded_by,
                source
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
        """, (
            title,
            description,
            original_filename,
            os.path.join(
                "uploads",
                original_filename
            ),
            file_type,
            uploaded_by,
            source
        ))

        material_id = cursor.lastrowid

        db.commit()

        cursor.close()

        return jsonify({

            "success": True,

            "message":
                "Learning material uploaded successfully",

            "material": {

                "id": material_id,

                "title": title,

                "description": description,

                "file_name":
                    original_filename,

                "file_type":
                    file_type,

                "source":
                    source,

                "status":
                    "Uploaded"
            }

        }), 201

    except Exception as e:

        db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# QUIZ - CREATE
# =========================================================

@app.route("/api/quizzes", methods=["POST"])
def create_quiz():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "JSON body is required"
            }), 400

        material_id = data.get(
            "material_id"
        )

        title = data.get(
            "title"
        )

        description = data.get(
            "description",
            ""
        )

        total_questions = data.get(
            "total_questions",
            0
        )

        # -----------------------------
        # VALIDATION
        # -----------------------------

        if not material_id:

            return jsonify({
                "success": False,
                "message": "material_id is required"
            }), 400

        if not title:

            return jsonify({
                "success": False,
                "message": "Quiz title is required"
            }), 400

        try:

            total_questions = int(
                total_questions
            )

        except (TypeError, ValueError):

            return jsonify({
                "success": False,
                "message":
                    "total_questions must be a number"
            }), 400

        if total_questions < 0:

            return jsonify({
                "success": False,
                "message":
                    "total_questions cannot be negative"
            }), 400

        # -----------------------------
        # DATABASE
        # -----------------------------

        cursor = db.cursor(
            dictionary=True
        )

        # Check learning material
        cursor.execute("""
            SELECT
                id,
                title,
                file_name
            FROM learning_materials
            WHERE id = %s
        """, (material_id,))

        material = cursor.fetchone()

        if not material:

            cursor.close()

            return jsonify({
                "success": False,
                "message":
                    "Learning material not found"
            }), 404

        # Create quiz
        cursor.execute("""
            INSERT INTO quizzes
            (
                material_id,
                title,
                description,
                total_questions
            )
            VALUES
            (%s, %s, %s, %s)
        """, (
            material_id,
            title,
            description,
            total_questions
        ))

        quiz_id = cursor.lastrowid

        db.commit()

        cursor.close()

        # -----------------------------
        # RESPONSE
        # -----------------------------

        return jsonify({

            "success": True,

            "message":
                "Quiz created successfully",

            "quiz": {

                "id":
                    quiz_id,

                "material_id":
                    material_id,

                "material_title":
                    material["title"],

                "title":
                    title,

                "description":
                    description,

                "total_questions":
                    total_questions
            }

        }), 201

    except Exception as e:

        db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# =========================================================
# QUIZ - ADD QUESTION
# =========================================================

@app.route("/api/quizzes/<int:quiz_id>/questions", methods=["POST"])
def add_quiz_question(quiz_id):

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "JSON body is required"
            }), 400

        question_id = data.get("question_id")

        if not question_id:
            return jsonify({
                "success": False,
                "message": "question_id is required"
            }), 400

        cursor = db.cursor(dictionary=True)

        # -------------------------------------------------
        # Check whether quiz exists
        # -------------------------------------------------

        cursor.execute("""
            SELECT id, title
            FROM quizzes
            WHERE id = %s
        """, (quiz_id,))

        quiz = cursor.fetchone()

        if not quiz:

            cursor.close()

            return jsonify({
                "success": False,
                "message": "Quiz not found"
            }), 404

        # -------------------------------------------------
        # Check whether question exists
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                id,
                question_text,
                competency_id
            FROM questions
            WHERE id = %s
        """, (question_id,))

        question = cursor.fetchone()

        if not question:

            cursor.close()

            return jsonify({
                "success": False,
                "message": "Question not found"
            }), 404

        # -------------------------------------------------
        # Check duplicate question
        # -------------------------------------------------

        cursor.execute("""
            SELECT id
            FROM quiz_questions
            WHERE quiz_id = %s
            AND question_id = %s
        """, (
            quiz_id,
            question_id
        ))

        existing = cursor.fetchone()

        if existing:

            cursor.close()

            return jsonify({
                "success": False,
                "message":
                    "Question is already added to this quiz"
            }), 409

        # -------------------------------------------------
        # Add question to quiz
        # -------------------------------------------------

        cursor.execute("""
            INSERT INTO quiz_questions
            (
                quiz_id,
                question_id
            )
            VALUES
            (%s, %s)
        """, (
            quiz_id,
            question_id
        ))

        link_id = cursor.lastrowid

        # -------------------------------------------------
        # Update quiz question count
        # -------------------------------------------------

        cursor.execute("""
            UPDATE quizzes
            SET total_questions = (
                SELECT COUNT(*)
                FROM quiz_questions
                WHERE quiz_id = %s
            )
            WHERE id = %s
        """, (
            quiz_id,
            quiz_id
        ))

        db.commit()

        cursor.close()

        return jsonify({

            "success": True,

            "message":
                "Question added to quiz successfully",

            "quiz_question": {

                "id":
                    link_id,

                "quiz_id":
                    quiz_id,

                "quiz_title":
                    quiz["title"],

                "question_id":
                    question_id,

                "question_text":
                    question["question_text"],

                "competency_id":
                    question["competency_id"]
            }

        }), 201

    except Exception as e:

        db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

        # =========================================================
# QUIZ - GET WITH QUESTIONS
# =========================================================

@app.route("/api/quizzes/<int:quiz_id>", methods=["GET"])
def get_quiz(quiz_id):

    try:
        cursor = db.cursor(dictionary=True)

        # Get quiz details
        cursor.execute("""
            SELECT
                q.id,
                q.material_id,
                q.title,
                q.description,
                q.total_questions,
                q.created_at,
                lm.title AS material_title
            FROM quizzes q
            LEFT JOIN learning_materials lm
                ON q.material_id = lm.id
            WHERE q.id = %s
        """, (quiz_id,))

        quiz = cursor.fetchone()

        if not quiz:
            cursor.close()

            return jsonify({
                "success": False,
                "message": "Quiz not found"
            }), 404

        # Get questions belonging to this quiz
        cursor.execute("""
            SELECT
                qq.id AS quiz_question_id,
                qu.id AS question_id,
                qu.question_text,
                qu.option_a,
                qu.option_b,
                qu.option_c,
                qu.option_d,
                qu.competency_id
            FROM quiz_questions qq
            JOIN questions qu
                ON qq.question_id = qu.id
            WHERE qq.quiz_id = %s
            ORDER BY qq.id
        """, (quiz_id,))

        questions = cursor.fetchall()

        cursor.close()

        return jsonify({
            "success": True,
            "quiz": quiz,
            "questions": questions
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

        # =========================================================
# QUIZ - START ATTEMPT
# =========================================================

@app.route("/api/quizzes/<int:quiz_id>/attempts", methods=["POST"])
def start_quiz_attempt(quiz_id):

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "JSON body is required"
            }), 400

        employee_id = data.get("employee_id")

        if not employee_id:
            return jsonify({
                "success": False,
                "message": "employee_id is required"
            }), 400

        cursor = db.cursor(dictionary=True)

        # -------------------------------------------------
        # Check whether quiz exists
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                id,
                title,
                total_questions
            FROM quizzes
            WHERE id = %s
        """, (quiz_id,))

        quiz = cursor.fetchone()

        if not quiz:
            cursor.close()

            return jsonify({
                "success": False,
                "message": "Quiz not found"
            }), 404

        # -------------------------------------------------
        # Check whether employee exists
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                id,
                name,
                email
            FROM users
            WHERE id = %s
        """, (employee_id,))

        employee = cursor.fetchone()

        if not employee:
            cursor.close()

            return jsonify({
                "success": False,
                "message": "Employee not found"
            }), 404

        # -------------------------------------------------
        # Get actual number of questions
        # -------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS question_count
            FROM quiz_questions
            WHERE quiz_id = %s
        """, (quiz_id,))

        question_result = cursor.fetchone()

        question_count = question_result["question_count"]

        # -------------------------------------------------
        # Create quiz attempt
        # -------------------------------------------------

        cursor.execute("""
            INSERT INTO quiz_attempts
            (
                quiz_id,
                employee_id,
                score,
                total_questions
            )
            VALUES
            (%s, %s, %s, %s)
        """, (
            quiz_id,
            employee_id,
            0,
            question_count
        ))

        attempt_id = cursor.lastrowid

        db.commit()

        cursor.close()

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "message":
                "Quiz attempt started successfully",

            "attempt": {

                "id":
                    attempt_id,

                "quiz_id":
                    quiz_id,

                "quiz_title":
                    quiz["title"],

                "employee_id":
                    employee_id,

                "employee_name":
                    employee["name"],

                "total_questions":
                    question_count,

                "score":
                    0
            }

        }), 201

    except Exception as e:

        db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

        # =========================================================
# QUIZ - SUBMIT ATTEMPT
# =========================================================

@app.route("/api/quizzes/attempts/<int:attempt_id>/submit", methods=["POST"])
def submit_quiz_attempt(attempt_id):

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "JSON body is required"
            }), 400

        answers = data.get("answers")

        if not answers or not isinstance(answers, list):
            return jsonify({
                "success": False,
                "message": "answers must be a non-empty list"
            }), 400

        cursor = db.cursor(dictionary=True)

        # -------------------------------------------------
        # CHECK ATTEMPT
        # -------------------------------------------------
        cursor.execute("""
            SELECT
                id,
                quiz_id,
                employee_id,
                score,
                total_questions
            FROM quiz_attempts
            WHERE id = %s
        """, (attempt_id,))

        attempt = cursor.fetchone()

        if not attempt:
            cursor.close()
            return jsonify({
                "success": False,
                "message": "Quiz attempt not found"
            }), 404

        quiz_id = attempt["quiz_id"]
        employee_id = attempt["employee_id"]

        # -------------------------------------------------
        # GET QUIZ QUESTIONS
        # -------------------------------------------------
        cursor.execute("""
            SELECT
                qq.question_id,
                q.question_text,
                q.correct_answer,
                q.competency_id
            FROM quiz_questions qq
            JOIN questions q
                ON qq.question_id = q.id
            WHERE qq.quiz_id = %s
        """, (quiz_id,))

        quiz_questions = cursor.fetchall()

        question_map = {
            q["question_id"]: q
            for q in quiz_questions
        }

        if not question_map:
            cursor.close()
            return jsonify({
                "success": False,
                "message": "No questions found for this quiz"
            }), 400

        # -------------------------------------------------
        # PREVENT DUPLICATE SUBMISSION
        # -------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS answer_count
            FROM quiz_answers
            WHERE attempt_id = %s
        """, (attempt_id,))

        existing_answers = cursor.fetchone()

        if existing_answers["answer_count"] > 0:
            cursor.close()
            return jsonify({
                "success": False,
                "message": "This quiz attempt has already been submitted"
            }), 409

        # -------------------------------------------------
        # PROCESS ANSWERS
        # -------------------------------------------------
        correct_count = 0
        processed_count = 0
        results = []
        competency_results = {}

        for answer in answers:
            question_id = answer.get("question_id")
            selected_answer = (
                answer.get("selected_answer") or ""
            ).upper()

            if selected_answer not in ["A", "B", "C", "D"]:
                cursor.close()
                return jsonify({
                    "success": False,
                    "message":
                        f"Invalid answer for question {question_id}. "
                        "Use A, B, C or D."
                }), 400

            question = question_map.get(question_id)

            if not question:
                continue

            is_correct = (
                selected_answer == question["correct_answer"]
            )

            if is_correct:
                correct_count += 1

            processed_count += 1

            competency_id = question["competency_id"]

            if competency_id:
                if competency_id not in competency_results:
                    competency_results[competency_id] = {
                        "total": 0,
                        "correct": 0
                    }

                competency_results[competency_id]["total"] += 1

                if is_correct:
                    competency_results[competency_id]["correct"] += 1

            # Store answer
            cursor.execute("""
                INSERT INTO quiz_answers
                (
                    attempt_id,
                    question_id,
                    selected_answer,
                    is_correct
                )
                VALUES
                (%s, %s, %s, %s)
            """, (
                attempt_id,
                question_id,
                selected_answer,
                1 if is_correct else 0
            ))

            results.append({
                "question_id": question_id,
                "selected_answer": selected_answer,
                "is_correct": is_correct,
                "competency_id": competency_id
            })

        # -------------------------------------------------
        # CALCULATE OVERALL QUIZ SCORE
        # -------------------------------------------------
        total_questions = len(question_map)

        score = (
            (correct_count / total_questions) * 100
            if total_questions > 0
            else 0
        )

        # -------------------------------------------------
        # UPDATE QUIZ ATTEMPT
        # -------------------------------------------------
        cursor.execute("""
            UPDATE quiz_attempts
            SET
                score = %s,
                total_questions = %s
            WHERE id = %s
        """, (
            score,
            total_questions,
            attempt_id
        ))

        # -------------------------------------------------
        # UPDATE EMPLOYEE COMPETENCIES + GAPS
        # -------------------------------------------------
        competency_updates = []

        for competency_id, result in competency_results.items():

            competency_total = result["total"]
            competency_correct = result["correct"]

            competency_score = (
                (competency_correct / competency_total) * 100
                if competency_total > 0
                else 0
            )

            required_score = 70
            gap_score = max(required_score - competency_score, 0)

            if gap_score == 0:
                gap_level = "No Gap"
            elif gap_score >= 30:
                gap_level = "High"
            elif gap_score >= 15:
                gap_level = "Medium"
            else:
                gap_level = "Low"

            # Update existing competency or create it
            cursor.execute("""
                SELECT id
                FROM employee_competencies
                WHERE employee_id = %s
                AND competency_id = %s
            """, (
                employee_id,
                competency_id
            ))

            existing_competency = cursor.fetchone()

            if existing_competency:
                cursor.execute("""
                    UPDATE employee_competencies
                    SET
                        score = %s,
                        last_assessed_at = NOW()
                    WHERE id = %s
                """, (
                    competency_score,
                    existing_competency["id"]
                ))
            else:
                cursor.execute("""
                    INSERT INTO employee_competencies
                    (
                        employee_id,
                        competency_id,
                        score,
                        last_assessed_at
                    )
                    VALUES
                    (%s, %s, %s, NOW())
                """, (
                    employee_id,
                    competency_id,
                    competency_score
                ))

            # Store or update the employee's current competency score
            # competency_scores has a UNIQUE(employee_id, competency_id) constraint.
            cursor.execute("""
                INSERT INTO competency_scores
                (
                    employee_id,
                    competency_id,
                    score,
                    assessed_from
                )
                VALUES
                (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    score = VALUES(score),
                    assessed_from = VALUES(assessed_from),
                    updated_at = NOW()
            """, (
                employee_id,
                competency_id,
                competency_score,
                "Quiz"
            ))

            # Save/update competency gap.
            # competency_gaps has a UNIQUE constraint for employee + competency.
            cursor.execute("""
                INSERT INTO competency_gaps
                (
                    employee_id,
                    competency_id,
                    current_score,
                    required_score,
                    gap_score,
                    gap_level
                )
                VALUES
                (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    current_score = VALUES(current_score),
                    required_score = VALUES(required_score),
                    gap_score = VALUES(gap_score),
                    gap_level = VALUES(gap_level),
                    identified_at = CURRENT_TIMESTAMP
            """, (
                employee_id,
                competency_id,
                competency_score,
                required_score,
                gap_score,
                gap_level
            ))

            competency_updates.append({
                "competency_id": competency_id,
                "score": round(competency_score, 2),
                "required_score": required_score,
                "gap_score": round(gap_score, 2),
                "gap_level": gap_level
            })

        # -------------------------------------------------
        # COMMIT
        # -------------------------------------------------
        db.commit()
        cursor.close()

        return jsonify({
            "success": True,
            "message": "Quiz submitted successfully",
            "result": {
                "attempt_id": attempt_id,
                "quiz_id": quiz_id,
                "employee_id": employee_id,
                "total_questions": total_questions,
                "answered_questions": processed_count,
                "correct_answers": correct_count,
                "score": round(score, 2),
                "competency_updates": competency_updates,
                "results": results
            }
        })

    except Exception as e:
        db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# EMPLOYEE PROFILE
# =========================================================

@app.route(
    "/api/employees/<int:employee_id>/profile",
    methods=["GET"]
)
def get_employee_profile(employee_id):

    try:

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                ep.*,
                u.name,
                u.email,
                u.role
            FROM employee_profiles ep
            JOIN users u
                ON ep.user_id = u.id
            WHERE ep.user_id = %s
        """, (employee_id,))

        profile = cursor.fetchone()

        cursor.close()

        if not profile:

            return jsonify({
                "success": False,
                "message":
                    "Employee profile not found"
            }), 404

        return jsonify({
            "success": True,
            "profile": profile
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# EMPLOYEE COMPETENCIES
# =========================================================

@app.route(
    "/api/employees/<int:employee_id>/competencies",
    methods=["GET"]
)
def get_employee_competencies(employee_id):

    try:

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                ec.id,
                ec.employee_id,
                ec.competency_id,
                c.name AS competency_name,
                c.domain,
                c.description,
                ec.score,
                ec.last_assessed_at
            FROM employee_competencies ec
            JOIN competencies c
                ON ec.competency_id = c.id
            WHERE ec.employee_id = %s
            ORDER BY c.id
        """, (employee_id,))

        competencies = cursor.fetchall()

        cursor.close()

        return jsonify({
            "success": True,
            "employee_id": employee_id,
            "competencies": competencies
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# EMPLOYEE - CALCULATE COMPETENCY GAPS
# =========================================================

@app.route(
    "/api/employees/<int:employee_id>/gaps",
    methods=["GET"]
)
def get_employee_gaps(employee_id):

    try:

        required_score = 70

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                ec.competency_id,
                c.name AS competency_name,
                c.domain,
                ec.score
            FROM employee_competencies ec
            JOIN competencies c
                ON ec.competency_id = c.id
            WHERE ec.employee_id = %s
        """, (employee_id,))

        rows = cursor.fetchall()

        cursor.close()

        gaps = []

        for row in rows:

            current_score = float(
                row["score"] or 0
            )

            gap_score = max(
                required_score - current_score,
                0
            )

            if gap_score == 0:

                gap_level = "No Gap"

            elif gap_score >= 30:

                gap_level = "High"

            elif gap_score >= 15:

                gap_level = "Medium"

            else:

                gap_level = "Low"

            gaps.append({

                "competency_id":
                    row["competency_id"],

                "competency_name":
                    row["competency_name"],

                "domain":
                    row["domain"],

                "current_score":
                    current_score,

                "required_score":
                    required_score,

                "gap_score":
                    gap_score,

                "gap_level":
                    gap_level
            })

        return jsonify({

            "success": True,

            "employee_id":
                employee_id,

            "gaps":
                gaps

        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# STORED COMPETENCY GAPS
# =========================================================

@app.route(
    "/api/employees/<int:employee_id>/stored-gaps",
    methods=["GET"]
)
def get_stored_gaps(employee_id):

    try:

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                cg.*,
                c.name AS competency_name,
                c.domain
            FROM competency_gaps cg
            JOIN competencies c
                ON cg.competency_id = c.id
            WHERE cg.employee_id = %s
            ORDER BY cg.gap_score DESC
        """, (employee_id,))

        gaps = cursor.fetchall()

        cursor.close()

        return jsonify({

            "success": True,

            "employee_id":
                employee_id,

            "gaps":
                gaps
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# RECOMMENDATIONS
# =========================================================

@app.route(
    "/api/employees/<int:employee_id>/recommendations",
    methods=["GET"]
)
def get_recommendations(employee_id):

    try:

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                r.id,
                r.employee_id,
                r.competency_id,
                c.name AS competency_name,
                c.domain,
                r.material_id,
                lm.title AS material_title,
                lm.description AS material_description,
                lm.file_name,
                lm.file_type,
                lm.source,
                r.reason,
                r.priority,
                r.status,
                r.created_at
            FROM recommendations r

            JOIN competencies c
                ON r.competency_id = c.id

            LEFT JOIN learning_materials lm
                ON r.material_id = lm.id

            WHERE r.employee_id = %s

            ORDER BY
                r.priority,
                r.created_at DESC
        """, (employee_id,))

        recommendations = cursor.fetchall()

        cursor.close()

        return jsonify({

            "success": True,

            "employee_id":
                employee_id,

            "recommendations":
                recommendations

        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# TEST RECOMMENDATION
# =========================================================

@app.route(
    "/api/test-recommendations",
    methods=["POST"]
)
def create_test_recommendation():

    try:

        data = request.get_json()

        employee_id = data.get(
            "employee_id"
        )

        competency_id = data.get(
            "competency_id"
        )

        material_id = data.get(
            "material_id"
        )

        reason = data.get(
            "reason",
            "Recommended learning material."
        )

        priority = data.get(
            "priority",
            "Medium"
        )

        if not employee_id:
            return jsonify({
                "success": False,
                "message":
                    "employee_id is required"
            }), 400

        if not competency_id:
            return jsonify({
                "success": False,
                "message":
                    "competency_id is required"
            }), 400

        if not material_id:
            return jsonify({
                "success": False,
                "message":
                    "material_id is required"
            }), 400

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO recommendations
            (
                employee_id,
                competency_id,
                material_id,
                reason,
                priority,
                status
            )
            VALUES
            (%s, %s, %s, %s, %s, %s)
        """, (
            employee_id,
            competency_id,
            material_id,
            reason,
            priority,
            "Pending"
        ))

        recommendation_id = cursor.lastrowid

        db.commit()

        cursor.close()

        return jsonify({

            "success": True,

            "message":
                "Recommendation created successfully",

            "recommendation_id":
                recommendation_id

        }), 201

    except Exception as e:

        db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# ASSESSMENT - CREATE
# =========================================================

@app.route(
    "/api/assessments",
    methods=["POST"]
)
def create_assessment():

    try:

        data = request.get_json()

        employee_id = data.get(
            "employee_id"
        )

        title = data.get(
            "title"
        )

        total_questions = data.get(
            "total_questions",
            0
        )

        if not employee_id:

            return jsonify({
                "success": False,
                "message":
                    "employee_id is required"
            }), 400

        if not title:

            return jsonify({
                "success": False,
                "message":
                    "Assessment title is required"
            }), 400

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO assessments
            (
                employee_id,
                title,
                total_questions
            )
            VALUES
            (%s, %s, %s)
        """, (
            employee_id,
            title,
            total_questions
        ))

        assessment_id = cursor.lastrowid

        db.commit()

        cursor.close()

        return jsonify({

            "success": True,

            "message":
                "Assessment created successfully",

            "assessment": {

                "id":
                    assessment_id,

                "employee_id":
                    employee_id,

                "title":
                    title,

                "total_questions":
                    total_questions
            }

        }), 201

    except Exception as e:

        db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# ASSESSMENT - ADD QUESTION
# =========================================================

@app.route(
    "/api/assessments/<int:assessment_id>/questions",
    methods=["POST"]
)
def add_assessment_question(
    assessment_id
):

    try:

        data = request.get_json()

        question_text = data.get(
            "question_text"
        )

        option_a = data.get(
            "option_a"
        )

        option_b = data.get(
            "option_b"
        )

        option_c = data.get(
            "option_c"
        )

        option_d = data.get(
            "option_d"
        )

        correct_answer = data.get(
            "correct_answer"
        )

        competency_id = data.get(
            "competency_id"
        )

        if not question_text:

            return jsonify({
                "success": False,
                "message":
                    "question_text is required"
            }), 400

        if not all([
            option_a,
            option_b,
            option_c,
            option_d
        ]):

            return jsonify({
                "success": False,
                "message":
                    "All options are required"
            }), 400

        if correct_answer not in [
            "A",
            "B",
            "C",
            "D"
        ]:

            return jsonify({
                "success": False,
                "message":
                    "correct_answer must be A, B, C or D"
            }), 400

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO questions
            (
                assessment_id,
                question_text,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer,
                competency_id
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            assessment_id,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer,
            competency_id
        ))

        question_id = cursor.lastrowid

        db.commit()

        cursor.close()

        return jsonify({

            "success": True,

            "message":
                "Question added successfully",

            "question_id":
                question_id

        }), 201

    except Exception as e:

        db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# ASSESSMENT - GET QUESTIONS
# =========================================================

@app.route(
    "/api/assessments/<int:assessment_id>/questions",
    methods=["GET"]
)
def get_assessment_questions(
    assessment_id
):

    try:

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                id,
                assessment_id,
                question_text,
                option_a,
                option_b,
                option_c,
                option_d,
                competency_id
            FROM questions
            WHERE assessment_id = %s
            ORDER BY id
        """, (assessment_id,))

        questions = cursor.fetchall()

        cursor.close()

        return jsonify({

            "success": True,

            "assessment_id":
                assessment_id,

            "questions":
                questions

        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# ASSESSMENT - SUBMIT
# =========================================================

@app.route(
    "/api/assessments/<int:assessment_id>/submit",
    methods=["POST"]
)
def submit_assessment(
    assessment_id
):

    try:

        data = request.get_json()

        answers = data.get(
            "answers",
            []
        )

        if not answers:

            return jsonify({
                "success": False,
                "message":
                    "Answers are required"
            }), 400

        cursor = db.cursor(
            dictionary=True
        )

        # Get assessment
        cursor.execute("""
            SELECT *
            FROM assessments
            WHERE id = %s
        """, (assessment_id,))

        assessment = cursor.fetchone()

        if not assessment:

            cursor.close()

            return jsonify({
                "success": False,
                "message":
                    "Assessment not found"
            }), 404

        employee_id = assessment[
            "employee_id"
        ]

        # Get questions
        cursor.execute("""
            SELECT *
            FROM questions
            WHERE assessment_id = %s
        """, (assessment_id,))

        questions = cursor.fetchall()

        question_map = {
            q["id"]: q
            for q in questions
        }

        total = len(questions)

        correct = 0

        competency_results = {}

        for answer in answers:

            question_id = answer.get(
                "question_id"
            )

            selected_answer = (
                answer.get("selected_answer")
                or ""
            ).upper()

            question = question_map.get(
                question_id
            )

            if not question:
                continue

            is_correct = (
                selected_answer
                == question["correct_answer"]
            )

            if is_correct:
                correct += 1

            competency_id = question[
                "competency_id"
            ]

            if competency_id:

                if competency_id not in competency_results:

                    competency_results[
                        competency_id
                    ] = {
                        "total": 0,
                        "correct": 0
                    }

                competency_results[
                    competency_id
                ]["total"] += 1

                if is_correct:

                    competency_results[
                        competency_id
                    ]["correct"] += 1

        # Overall score
        overall_score = (
            (correct / total) * 100
            if total > 0
            else 0
        )

        # Update assessment
        cursor.execute("""
            UPDATE assessments
            SET
                total_questions = %s,
                score = %s,
                completed_at = NOW()
            WHERE id = %s
        """, (
            total,
            overall_score,
            assessment_id
        ))

        competency_updates = []

        # -----------------------------------------
        # UPDATE COMPETENCY SCORES + GAPS
        # -----------------------------------------

        for competency_id, result in competency_results.items():

            competency_total = result[
                "total"
            ]

            competency_correct = result[
                "correct"
            ]

            competency_score = (
                (competency_correct
                 / competency_total) * 100
                if competency_total > 0
                else 0
            )

            required_score = 70

            gap_score = max(
                required_score
                - competency_score,
                0
            )

            if gap_score == 0:

                gap_level = "No Gap"

            elif gap_score >= 30:

                gap_level = "High"

            elif gap_score >= 15:

                gap_level = "Medium"

            else:

                gap_level = "Low"

            # -----------------------------------------
            # UPDATE EMPLOYEE COMPETENCY
            # -----------------------------------------
            cursor.execute("""
                SELECT id
                FROM employee_competencies
                WHERE employee_id = %s
                  AND competency_id = %s
            """, (employee_id, competency_id))

            existing_competency = cursor.fetchone()

            if existing_competency:
                cursor.execute("""
                    UPDATE employee_competencies
                    SET score = %s,
                        last_assessed_at = NOW()
                    WHERE employee_id = %s
                      AND competency_id = %s
                """, (
                    competency_score,
                    employee_id,
                    competency_id
                ))
            else:
                cursor.execute("""
                    INSERT INTO employee_competencies
                    (employee_id, competency_id, score, last_assessed_at)
                    VALUES (%s, %s, %s, NOW())
                """, (
                    employee_id,
                    competency_id,
                    competency_score
                ))

            # -----------------------------------------
            # UPDATE COMPETENCY SCORES
            # -----------------------------------------
            cursor.execute("""
                INSERT INTO competency_scores
                (
                    employee_id,
                    competency_id,
                    score,
                    assessed_from
                )
                VALUES
                (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    score = VALUES(score),
                    assessed_from = VALUES(assessed_from),
                    updated_at = NOW()
            """, (
                employee_id,
                competency_id,
                competency_score,
                "Assessment"
            ))

            # -----------------------------------------
            # UPDATE COMPETENCY GAP
            # -----------------------------------------
            cursor.execute("""
                INSERT INTO competency_gaps
                (
                    employee_id,
                    competency_id,
                    current_score,
                    required_score,
                    gap_score,
                    gap_level
                )
                VALUES
                (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    current_score = VALUES(current_score),
                    required_score = VALUES(required_score),
                    gap_score = VALUES(gap_score),
                    gap_level = VALUES(gap_level),
                    identified_at = CURRENT_TIMESTAMP
            """, (
                employee_id,
                competency_id,
                competency_score,
                required_score,
                gap_score,
                gap_level
            ))

            competency_updates.append({

                "competency_id":
                    competency_id,

                "score":
                    round(
                        competency_score,
                        2
                    ),

                "required_score":
                    required_score,

                "gap_score":
                    round(
                        gap_score,
                        2
                    ),

                "gap_level":
                    gap_level
            })

        db.commit()

        cursor.close()

        return jsonify({

            "success": True,

            "message":
                "Assessment submitted successfully",

            "assessment_id":
                assessment_id,

            "employee_id":
                employee_id,

            "total_questions":
                total,

            "correct_answers":
                correct,

            "score":
                round(
                    overall_score,
                    2
                ),

            "competency_updates":
                competency_updates

        })

    except Exception as e:

        db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# MANUAL COMPETENCY SCORE
# =========================================================

@app.route(
    "/api/employees/<int:employee_id>/competency-scores",
    methods=["POST"]
)
def add_competency_score(
    employee_id
):

    try:

        data = request.get_json()

        competency_id = data.get(
            "competency_id"
        )

        score = data.get(
            "score"
        )

        assessed_from = data.get(
            "assessed_from",
            "Manual"
        )

        if competency_id is None:

            return jsonify({
                "success": False,
                "message":
                    "competency_id is required"
            }), 400

        if score is None:

            return jsonify({
                "success": False,
                "message":
                    "score is required"
            }), 400

        score = float(score)

        if score < 0 or score > 100:

            return jsonify({
                "success": False,
                "message":
                    "score must be between 0 and 100"
            }), 400

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO competency_scores
            (
                employee_id,
                competency_id,
                score,
                assessed_from
            )
            VALUES
            (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                score = VALUES(score),
                assessed_from = VALUES(assessed_from),
                updated_at = NOW()
        """, (
            employee_id,
            competency_id,
            score,
            assessed_from
        ))

        score_id = cursor.lastrowid

        db.commit()

        cursor.close()

        return jsonify({

            "success": True,

            "message":
                "Competency score saved",

            "score_id":
                score_id

        }), 201

    except Exception as e:

        db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# MANUAL COMPETENCY GAP
# =========================================================

@app.route(
    "/api/employees/<int:employee_id>/competency-gaps",
    methods=["POST"]
)
def add_competency_gap(
    employee_id
):

    try:

        data = request.get_json()

        competency_id = data.get(
            "competency_id"
        )

        current_score = float(
            data.get(
                "current_score",
                0
            )
        )

        required_score = float(
            data.get(
                "required_score",
                70
            )
        )

        gap_score = max(
            required_score
            - current_score,
            0
        )

        if gap_score == 0:

            gap_level = "No Gap"

        elif gap_score >= 30:

            gap_level = "High"

        elif gap_score >= 15:

            gap_level = "Medium"

        else:

            gap_level = "Low"

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO competency_gaps
            (
                employee_id,
                competency_id,
                current_score,
                required_score,
                gap_score,
                gap_level
            )
            VALUES
            (%s, %s, %s, %s, %s, %s)
        """, (
            employee_id,
            competency_id,
            current_score,
            required_score,
            gap_score,
            gap_level
        ))

        gap_id = cursor.lastrowid

        db.commit()

        cursor.close()

        return jsonify({

            "success": True,

            "message":
                "Competency gap saved",

            "gap": {

                "id":
                    gap_id,

                "employee_id":
                    employee_id,

                "competency_id":
                    competency_id,

                "current_score":
                    current_score,

                "required_score":
                    required_score,

                "gap_score":
                    gap_score,

                "gap_level":
                    gap_level
            }

        }), 201

    except Exception as e:

        db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )