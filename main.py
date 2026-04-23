from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from database import get_connection

app = FastAPI(title="Winx Fanbase API")

def seed_if_empty():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        fairy_type TEXT,
        home_world TEXT,
        description TEXT
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM characters")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany("""
        INSERT INTO characters (name, fairy_type, home_world, description)
        VALUES (?, ?, ?, ?)
        """, [
            ("Bloom", "Dragon Flame", "Earth", "Leader of Winx Club"),
            ("Stella", "Sun & Moon", "Solaria", "Princess of light"),
            ("Flora", "Nature", "Lynphea", "Nature fairy"),
        ])

        conn.commit()

    conn.close()

seed_if_empty()


# 🏠 UI Route
@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/characters/{param}")
def get_character(param: str):
    conn = get_connection()
    cursor = conn.cursor()

    # ensure table exists (important on Render)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        fairy_type TEXT,
        home_world TEXT,
        description TEXT
    )
    """)

    # numeric → ID search
    if param.isdigit():
        cursor.execute("SELECT * FROM characters WHERE id = ?", (int(param),))
    else:
        cursor.execute("SELECT * FROM characters WHERE name = ?", (param,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Character not found")

    return dict(row)


# 📌 Get actors
@app.get("/actors")
def get_actors():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT actors.id, actors.name, actors.nationality, characters.name as character
    FROM actors
    JOIN characters ON actors.character_id = characters.id
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]
