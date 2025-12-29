from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from dotenv import load_dotenv
import sqlite3
import ollama
import os

app = Flask(__name__)
CORS(app)
BASE_DIR = Path(__file__).resolve().parent
DB = BASE_DIR / "courses.db"

load_dotenv(BASE_DIR / ".." / "secret.env")
remote_host = os.getenv("REMOTE_HOST")
api_key = os.getenv("API_KEY")
model_name = os.getenv("MODEL_NAME")

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
    You are a specialized SQL generator for a university course database. Your goal is to convert natural language into valid SQLite SELECT queries.

    ### Database Schema (Table: courses)
    - id: INTEGER (Primary Key)
    - name: TEXT (Course name)
    - category: TEXT (Options: '必修', '系內選修', '系外選修', '領域通識', '融合通識', '大學國文', '體育', '英文', '踏溯台南', '其他')
    - credit: INTEGER (Credits)
    - status: TEXT (Options: '進行中', '待定', '完成')
    - score: INTEGER (Finished score, -1 if no score yet)
    - teacher: TEXT (Instructor name)
    - generalType: TEXT (Options: '人文學', '社會科學', '自然與工程科學', '生命科學與健康', '科技整合領域'. Only if category is '領域通識')
    - detail: TEXT (Additional course info)

    ### Critical Rules
    1. ALWAYS use "SELECT *" to ensure the frontend UI receives all necessary fields (name, category, id, etc.) for rendering.
    2. Output ONLY the raw SQL string. No markdown backticks (e.g., no ```sql), no explanations.
    3. Use LIKE '%keyword%' for any search involving teacher names, course names, or details.
    4. For GE courses:If the user use "通識", you **MUST** use: (category = '領域通識' OR category = '融合通識').This is a hard requirement.
    5. For completed courses: Filter by status = '完成'.
    6. Read-Only: Only generate SELECT statements. No UPDATE, DELETE, or INSERT.
    7. '大學國文', '英文', '體育', '踏溯台南' are NOT considered "通識" in this logic.
    8. The "Exclusion (排除)" Rule (Priority):
    -If the user specifies "非", "不是", "除了...以外", "未", "還沒"or "except", you MUST add an AND condition with != or NOT LIKE.
    -Example: "非領域通識的通識課" -> SELECT * FROM courses WHERE (category = '領域通識' OR category = '融合通識') AND category != '領域通識';
    9. If user says "還沒完成", "沒修過", "未過", "未完成", ALWAYS use status != '完成'.

    ### Examples
    - Question: "找莊坤達教的課" -> SELECT * FROM courses WHERE teacher LIKE '%莊坤達%';
    - Question: "我想找人文通識" -> SELECT * FROM courses WHERE generalType LIKE '%人文學%' AND category = '領域通識';
    - Question: "列出我完成的必修" -> SELECT * FROM courses WHERE status = '完成' AND category = '必修';
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