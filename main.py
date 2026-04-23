from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from database import get_connection

app = FastAPI(title="Winx Fanbase API")

# 🏠 UI Route
@app.get("/")
def home():
    return FileResponse("static/index.html")


# 📌 Get all characters
@app.get("/characters/{param}")
def get_character(param: str):
    conn = get_connection()
    cursor = conn.cursor()

    # If numeric → treat as ID
    if param.isdigit():
        cursor.execute("SELECT * FROM characters WHERE id = ?", (param,))
    else:
        cursor.execute("SELECT * FROM characters WHERE name = ?", (param,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Character not found")

    return dict(row)


# 📌 Get specific character
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
