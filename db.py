import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "todo.db")


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def row_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }


def get_all_todos():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM todos ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()
    return [row_to_dict(row) for row in rows]


def add_todo(title):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO todos (title, done, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (title, 0, now, now)
    )

    conn.commit()
    todo_id = cur.lastrowid
    conn.close()

    return {
        "id": todo_id,
        "title": title,
        "done": False,
        "created_at": now,
        "updated_at": now
    }


def toggle_todo(todo_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    row = cur.fetchone()

    if row is None:
        conn.close()
        return None

    new_done = 0 if row["done"] else 1
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute(
        "UPDATE todos SET done = ?, updated_at = ? WHERE id = ?",
        (new_done, now, todo_id)
    )

    conn.commit()

    cur.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    updated = cur.fetchone()

    conn.close()
    return row_to_dict(updated)


def delete_todo(todo_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()

    deleted_count = cur.rowcount
    conn.close()

    return deleted_count > 0