import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "courses.db"

def seed_courses():
    # 歷史課程清單
    historical_data = [
        ("數位系統設計", "必修", 3, "完成", 85, "莊坤達", "", "硬體實驗課程"),
        ("離散數學", "必修", 3, "完成", 70, "林老師", "", "基礎數學"),
        ("通訊原理", "選修", 3, "進行中", -1, "陳教授", "", "通訊領域"),
        ("性別與社會", "通識", 2, "完成", 90, "張老師", "社會", "通識課程"),
        ("人工智慧導論", "系內選修", 3, "完成", 92, "李老師", "", "AI應用")
    ]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 插入資料
    cursor.executemany("""
    INSERT INTO courses (name, category, credit, status, score, teacher, generalType, detail)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, historical_data)

    conn.commit()
    conn.close()
    print(f"已成功匯入 {len(historical_data)} 筆歷史資料到資料庫！")

if __name__ == "__main__":
    seed_courses()