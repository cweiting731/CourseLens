# Course Query Agent (MVP)

本專案為「課程屬性查詢 Agent」的 MVP：
- 後端：Python Flask + SQLite
- 前端：純 HTML + JavaScript
- 功能：
    1. 新增課程（INSERT）
    2. 列出所有課程（LIST ALL）

## 專案結構

```
Code/
    backend/
        app.py
        init_db.py
        courses.db (執行 init_db.py 後產生)
    frontend/
        index.html
requirements.txt
.gitignore
```

## 環境需求

- Python 3.10+（建議）
- Windows / macOS / Linux 皆可
- 瀏覽器（Chrome / Edge）

## 安裝與執行（Windows PowerShell）

### 進入專案資料夾
```powershell
cd Code
```
### 建立並啟用虛擬環境（venv）
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
若 PowerShell 不允許執行腳本，請先執行一次：
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 安裝依賴套件
確認 requirements.txt 內容至少包含：
```txt
Flask
flask-cors
```

安裝：
```powershell
pip install -r requirements.txt
```

### 初始化資料庫（會在 backend/ 生成 courses.db）
```powershell
python backend\init_db.py
```

### 啟動後端伺服器
```powershell
python backend\app.py
```
啟動後預設會在： http://127.0.0.1:5000

## 使用方式
直接用瀏覽器打開：`Code/frontend/index.html`

在前端填寫欄位後按「新增」，即可新增資料到資料庫。
再按「重新整理」可以看到所有課程清單。

> [!note] 備註：本專案使用 flask-cors 以允許前端（file://）呼叫後端 API。

## 安裝與執行（macOS / Linux）
```bash
cd Code
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python backend/init_db.py
python backend/app.py
```

---
# 向LLM發送prompt格式範例
```
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

### User Question
「{{查詢分數大於 80 分的必修課}}」
```
