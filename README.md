# SIH26101 Tech Spark

AI-enabled skill intelligence and learning platform for employees and administrators.

## Architecture

One Flask server serves the static frontend and both API groups at `http://127.0.0.1:5000`:

- `/api/*` - MySQL-backed authentication, competencies, learning materials, quizzes and assessments
- `/ai/*`, `/recommend`, `/quiz/submit`, `/materials` - AI learning-cycle and recommendation services
- `/` — the frontend application

The AI pipeline can use Gemini when `GEMINI_API_KEY` is configured. Do not commit a real `.env` file.

## First-time setup (Windows)

1. Copy `.env.example` to `.env`, set the MySQL values if your server differs from the defaults, and set a long random `FLASK_SECRET_KEY`.
2. Create the database and import `database/sih26101_db.sql` using MySQL Workbench or the MySQL client.
3. Run `start_project.bat`.
4. Open `http://127.0.0.1:5000/`.

The included SQL dump contains the initial employee account and learning data. Use a real database account for sign-in; browser-only demo sign-in is intentionally disabled.

The supplied dump does not include an administrator and does not document a usable employee password. Create accounts once, using password prompts:

```powershell
.\.venv\Scripts\python.exe backend\create_admin.py
.\.venv\Scripts\python.exe backend\create_admin.py --role employee
```

## Manual start

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python backend\app.py
```

## Supported learning documents

PDF, PPTX, and DOCX. Legacy `.ppt` and `.doc` files are rejected because the installed extractor does not support them reliably.
