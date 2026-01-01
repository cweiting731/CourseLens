# 專題背景與動機
在大學選課時，學生常需要查詢自己在不同種類的學分中已經修了多少學分了，像是

- 通識類別是否已經選夠3個種類了
- 必修 / 系外選修 / 系內選修 / 國文 / 通識 / 英文 ...
- 授課老師
- 學分數
- 成績
- 等等......

此外，多數系統不支援自然語言搜尋，學生無法直接輸入：
```
「有哪些我已經完成，成績是80分以上的領域通識課程」
```
因此，本專題設計一個 **AI 課程屬性查詢 Agent**，讓我們可以使用自然語言即可查詢自己的課程資料，提供更直覺、高效率的選課體驗

# 系統目標
- **自然語言查詢課程資訊**  
    例如：「幫我找通識自然領域、跟程式設計有關的課」
- **將使用者的問題轉換成 SQL 查詢**  
    使用 AI 模型（LLM）將自然語言 → SQL
- **資料庫中查詢課程資訊**  
    存放課程名稱、學分數、成績、類別、授課老師等
- **以清楚格式回傳查詢結果**  
    提供給使用者列表式的輸出
# 實機畫面
<img width="1778" height="996" alt="image" src="https://github.com/user-attachments/assets/ac49b961-2952-41e6-b58f-285ada3248ec" />

# 流程圖與FSM
<img width="2660" height="1180" alt="流程圖" src="https://github.com/user-attachments/assets/f6b78bd2-fb41-4798-b800-801096b65862" />
<img width="1360" height="800" alt="FSM" src="https://github.com/user-attachments/assets/69551c91-db69-4737-95fa-e79c94472edf" />

# 資料格式
| 欄位名稱        | 資料型態    | 說明                                                                          |
| ----------- | ------- | --------------------------------------------------------------------------- |
| id          | INTEGER | PRIMARY KEY                                                                 |
| name        | TEXT    | 課程名稱                                                                        |
| category    | TEXT    | 課程分類（必修 / 系內選修 / 系外選修 / 領域通識 / 融合通識 / 英文 / 大學國文 / 體育 / 踏溯台南 / 其他）           |
| credit      | INTEGER | 學分數                                                                         |
| status      | TEXT    | 課程狀態（進行中 / 完成）                                                              |
| score       | INTEGER | 修畢分數 (只有 status 為 "完成" 會有修畢分數，無修畢分數以 "-1" 表示) (0-100)                       |
| teacher     | TEXT    | 授課教師                                                                        |
| generalType | TEXT    | 通識分類（人文學、社會科學、自然與工程科學、生命科學與健康、科際整合領域）只有 category 為 "領域通識" 時會有通識分類，無內容以空字串表示 |
| detail      | TEXT    | 選填，填寫其他課程內容（附加資訊、上課方式等等），無內容以 空字串 "" 表示                                     |

## Example Record

| 欄位           | 值    |
| ------------ | ---- |
| name         | 計算理論 |
| category     | 系內選修 |
| credit       | 3    |
| status       | 進行中  |
| score        | -1   |
| teacher      | 莊坤達  |
| general_type | ""   |
| detail       | ""   |

# 專案結構

```
Code/
    backend/
        app.py
        init_db.py
        courses.db (執行 init_db.py 後產生)
        seed_history.py (快速插入課程example)
    frontend/
        index.html
    requirements.txt
    .gitignore
    README.md
    secret.env (設定使用Agent參數)
README.md
```

# 環境需求

- Python 3.10+（建議）
- Windows / macOS / Linux 皆可
- 瀏覽器（Chrome / Edge）

# 安裝與執行（Windows PowerShell）

## 進入專案資料夾
```powershell
cd Code
```
## 建立並啟用虛擬環境（venv）
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
若 PowerShell 不允許執行腳本，請先執行一次：
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## 安裝依賴套件
確認 requirements.txt 內容至少包含：
```txt
Flask
flask-cors
ollama
python-dotenv
```

安裝：
```powershell
pip install -r requirements.txt
```

## 初始化資料庫（會在 backend/ 生成 courses.db）
```powershell
python backend\init_db.py
```
若有需要可以執行
```powershell
python backend\seed_history.py
```
自動填入預設的課程，迅速看到效果

## 設定API_KEY
前往 `Code/secret.env`，在 `API_KEY` 的位置填入實際的金鑰

## 啟動後端伺服器
```powershell
python backend\app.py
```
啟動後預設會在： http://127.0.0.1:5000

# 使用方式
直接用瀏覽器打開：`Code/frontend/index.html`

在前端填寫欄位後按「新增」，即可新增資料到資料庫。
再按「重新整理」可以看到所有課程清單。

> 備註：本專案使用 flask-cors 以允許前端（file://）呼叫後端 API。

# 安裝與執行（macOS / Linux）
```bash
cd Code
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python backend/init_db.py
python backend/app.py
```

