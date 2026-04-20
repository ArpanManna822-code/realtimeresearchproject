import sqlite3

DB = "leaderboard.db"

def init_db():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        score INTEGER
    )
    """)

    conn.commit()
    conn.close()


def save_score(name, score):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO scores (name, score) VALUES (?,?)",
        (name, score)
    )

    conn.commit()
    conn.close()


def load_scores():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, score FROM scores ORDER BY score DESC LIMIT 10"
    )

    scores = cursor.fetchall()

    conn.close()

    return [{"name": s[0], "score": s[1]} for s in scores]