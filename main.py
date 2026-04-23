from fastapi import FastAPI, HTTPException
from database import get_connection

app = FastAPI(title="Winx Fanbase API")

# Root check
@app.get("/")
def root():
    return {"message": "Winx Fanbase API is running 🧚"}

# 1️⃣ Get All Characters
@app.get("/characters")
def get_characters():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM characters")
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]


# 2️⃣ Get Specific Character
@app.get("/characters/{character_id}")
def get_character(character_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM characters WHERE id = ?", (character_id,))
    row = cursor.fetchone()

    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Character not found")

    return dict(row)


# 3️⃣ Get Actors
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
