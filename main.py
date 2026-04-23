from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import get_connection

app = FastAPI(title="Winx Fanbase API")

templates = Jinja2Templates(directory="templates")

# 🏠 UI Route
@app.get("/")
def home():
    return FileResponse("static/index.html")


# API ROUTES (same as before)

@app.get("/characters")
def get_characters():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM characters")
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]


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
