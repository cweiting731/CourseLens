from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import sqlite3
import ollama

app = Flask(__name__)
CORS(app)
BASE_DIR = Path(__file__).resolve().parent
DB = BASE_DIR / "courses.db"

remote_host = "https://api-gateway.netdb.csie.ncku.edu.tw"
api_key = "API_KEY"
model_name = "gemma3:4b"

# 初始化 AI 客戶端
client = ollama.Client(
    host=remote_host,
    headers={'Authorization': f'Bearer {api_key}'}
)

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
    user_question = request.json.get("text")
    if not user_question:
        return jsonify({"message": "請輸入問題"}), 400

    # 1. 準備 System Prompt (從組員程式碼複製過來)
    system_prompt = """
    ### Role
    You are a SQL generator for a university course database. Your task is to translate natural language questions into executable SQLite SELECT queries.
    ### Database Schema
    Table: **courses**
    - id, name, category, credit, status, score, teacher, generalType, detail
    ### Rules
    1. Output ONLY the raw SQL SELECT query. No markdown.
    2. Read-Only: Only generate `SELECT` statements.
    3. Keyword Matching: Use `LIKE '%keyword%'`.
    """

    try:
        # 2. 呼叫 AI (對應流程圖：發送 API /chat -> LLM 返還搜尋指令)
        response = client.generate(
            model=model_name,
            prompt=f"{system_prompt}\n\n### User Question\n「{user_question}」",
            stream=False,
            options={"temperature": 0}
        )

        raw_sql = response['response'].strip()
        sql_query = raw_sql.replace("```sqlite", "").replace("```sql", "").replace("```", "").strip()
        
        print(f"清理後的 SQL: {sql_query}")

        # 3. 執行 SQL (對應流程圖：根據指令搜尋資料庫)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        conn.close()

        # 4. 回傳結果 (對應流程圖：response json 格式資料 200)
        result = [dict(row) for row in rows]
        return jsonify(result), 200

    except Exception as e:
        print(f"錯誤: {e}")
        return jsonify({"error": "AI 轉譯或資料庫查詢失敗"}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)