import ollama

# --- 設定參數 ---
remote_host = "https://api-gateway.netdb.csie.ncku.edu.tw" # 請替換成實際網址
api_key = "" # 你的 API Key
model_name = "gemma3:4b" # 或者對方使用的模型名稱，例如 'gemma2', 'mistral'

# 初始化 Client (帶入自定義 Host 與 Headers)
# 注意：如果對方是用標準的 Bearer Token 驗證，請保留 Authorization 格式
client = ollama.Client(
    host=remote_host,
    headers={
        'Authorization': f'Bearer {api_key}'
    }
)

# 定義你的完整 Prompt
system_prompt = """
### Role
You are a SQL generator for a university course database. Your task is to translate natural language questions into executable SQLite SELECT queries.

### Database Schema
Table: **courses**
- `id` (INTEGER): 唯一識別碼（自動遞增）
- `name` (TEXT): 課程名稱
- `category` (TEXT): 課程分類（例如：必修、系內選修、通識、系外選修）
- `credit` (INTEGER): 學分數
- `status` (TEXT): 狀態（例如：已完成、進行中）
- `score` (INTEGER): 分數（若無分數則為 -1）
- `teacher` (TEXT): 授課教師
- `generalType` (TEXT): 通識分類（例如：人文、社會、自然，非通識則為空字串）
- `detail` (TEXT): 課程細項或備註

### Rules
1. **Output ONLY the raw SQL SELECT query.** Do not include markdown code blocks, explanations, or any extra text.
2. **Read-Only:** Only generate `SELECT` statements. Use of `INSERT`, `UPDATE`, `DELETE`, or `DROP` is strictly prohibited.
3. **General Education Logic:** - When the user mentions "通識" (General Education), filter by `category = '通識'` or use `generalType` if a specific field is mentioned.
4. **Keyword Matching:** Use `LIKE '%keyword%'` for partial matches in `name`, `teacher`, or `detail`.
5. **Score Handling:** If searching for courses taken/finished, check `status = '已完成'` or `score >= 0`.
6. **Constraint:** If the question is ambiguous, prioritize returning `name`, `category`, and `credit`.
"""

user_question = "查詢分數大於 80 分的必修課"

try:
    # 發送請求
    response = client.generate(
        model=model_name,
        prompt=f"{system_prompt}\n\n### User Question\n「{user_question}」",
        stream=False, # 如果設為 True 則需要用迴圈處理流式輸出
        options={
            "temperature": 0 # 生成 SQL 建議將隨機性降到最低
        }
    )

    # 印出結果
    sql_query = response['response'].strip()
    print("--- 產生的 SQL ---")
    print(sql_query)

except Exception as e:
    print(f"連線或執行發生錯誤: {e}")