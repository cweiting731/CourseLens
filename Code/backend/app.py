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

# 1. 取得所有課程 (GET)
@app.route("/courses", methods=["GET"])
def list_courses():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, credit, status, score, teacher, generalType, detail FROM courses")
    rows = cursor.fetchall()
    conn.close()
    
    result = [dict(row) for row in rows]
    return jsonify(result), 200

# 2. 新增或更新課程 (POST/PUT)
@app.route("/course", methods=["POST", "PUT"])
def save_course():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == "POST":
        cursor.execute("""
            INSERT INTO courses (name, category, credit, status, score, teacher, generalType, detail)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (data["name"], data["category"], data.get("credit", 0), data["status"], 
              data.get("score", -1), data["teacher"], data["generalType"], data["detail"]))
        msg = "Course inserted"
    else:  # PUT
        cursor.execute("""
            UPDATE courses SET name=?, category=?, credit=?, status=?, score=?, teacher=?, generalType=?, detail=?
            WHERE id=?
        """, (data["name"], data["category"], data["credit"], data["status"], 
              data["score"], data["teacher"], data["generalType"], data["detail"], data["id"]))
        msg = "Course updated"

    conn.commit()
    conn.close()
    return jsonify({"message": msg}), 200

# 3. 刪除課程 (DELETE)
@app.route("/course/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE id=?", (course_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Course deleted"}), 200

# 4. 對話框 API (保留效果)
@app.route("/chat", methods=["POST"])
def chat():
    text = request.json.get("text")
    print(f"Chat received: {text}")
    return jsonify({"message": "Server received your message"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)