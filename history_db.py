import sqlite3
from pathlib import Path

DB_PATH = Path("chat_history.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
    conn.commit()
    conn.close()

def load_messages():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT role, content FROM messages ORDER BY id").fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in rows]

def clear_messages():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
