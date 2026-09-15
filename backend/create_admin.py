"""Create a local user without storing a default password in source."""

import argparse
import getpass
import os

import mysql.connector
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", choices=("admin", "employee"), default="admin")
    role = parser.parse_args().role

    name = input(f"{role.title()} name: ").strip()
    email = input(f"{role.title()} email: ").strip().lower()
    password = getpass.getpass(f"{role.title()} password: ")

    if not name or not email or len(password) < 8:
        raise SystemExit("Name, email, and a password of at least 8 characters are required.")

    db = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3308")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "sih26101_db")
    )
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            raise SystemExit("A user with that email already exists.")

        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            (name, email, generate_password_hash(password), role)
        )
        db.commit()
        print(f"{role.title()} created successfully.")
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    main()
