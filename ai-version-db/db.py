import sqlite3

DB_FILE = "tasks.db"

# a single shared connection, reused across requests
connection = sqlite3.connect(DB_FILE, check_same_thread=False)
connection.row_factory = sqlite3.Row


def init_db():
    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    connection.commit()

    count = connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        connection.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [("Buy groceries", 0), ("Finish FL-01 assignment", 1), ("Push code to GitHub", 0)],
        )
        connection.commit()
