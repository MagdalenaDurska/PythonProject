import sqlite3
import os
from functions.config import INSTRUMENTS

DB_PATH = "value_modifier.db"

def initialize_db():
    if os.path.exists(DB_PATH):
        print(f"Database already exists at {DB_PATH}.")
    else:
        print(f"Creating database at {DB_PATH}...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS INSTRUMENT_PRICE_MODIFIER (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT UNIQUE NOT NULL,
        MULTIPLIER REAL NOT NULL
    )
    """)


    modifiers = [
        (INSTRUMENTS["MEAN"], 2.0),
        (INSTRUMENTS["MEAN_DATE"], 1.5),
        (INSTRUMENTS["STDDEV"], 1.0),
    ]

    cursor.executemany("""
    INSERT OR REPLACE INTO INSTRUMENT_PRICE_MODIFIER (NAME, MULTIPLIER)
    VALUES (?, ?)
    """, modifiers)

    conn.commit()
    conn.close()
    print("Database initialized and populated.")

if __name__ == "__main__":
    initialize_db()
