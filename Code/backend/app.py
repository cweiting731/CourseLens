from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import sqlite3

app = Flask(__name__)
CORS(app)
BASE_DIR = Path(__file__).resolve().parent
DB = BASE_DIR / "courses.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# INSERT course
@app.route("/course", methods=["POST"])
def insert_course():
    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO courses
        (name, category, credit, status, score, teacher, generalType, detail)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["category"],
        data["credit"],
        data["status"],
        data["score"],
        data["teacher"],
        data["generalType"],
        data["detail"]
    ))

    print("Inserted course:", data["name"])

    conn.commit()
    conn.close()

    return jsonify({"message": "Course inserted successfully"}), 201


# LIST all courses
@app.route("/courses", methods=["GET"])
def list_courses():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, category, credit, status, score, teacher, generalType, detail FROM courses")
    rows = cursor.fetchall()
    conn.close()

    result = []

    print("Listing all courses, total:", len(rows))

    for r in rows:
        result.append({
            "name": r[0],
            "category": r[1],
            "credit": r[2],
            "status": r[3],
            "score": r[4],
            "teacher": r[5],
            "generalType": r[6],
            "detail": r[7]
        })

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)
