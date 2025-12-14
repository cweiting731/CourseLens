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
