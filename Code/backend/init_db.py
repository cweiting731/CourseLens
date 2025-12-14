from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "courses.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    credit INTEGER,
    status TEXT,
    score INTEGER,
    teacher TEXT,
    generalType TEXT,
    detail TEXT
)
""")

conn.commit()
conn.close()
print(f"Database initialized at: {DB_PATH}")
