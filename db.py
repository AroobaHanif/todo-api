import sqlite3

DB_FILE = "tasks.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        seed = [
            ("Buy groceries", 0),
            ("Finish FL-01 assignment", 1),
            ("Push code to GitHub", 0),
        ]
        conn.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", seed)
        conn.commit()

    conn.close()
