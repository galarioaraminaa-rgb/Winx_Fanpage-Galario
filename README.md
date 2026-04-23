# Winx Club Fanbase API

A FastAPI + SQLite powered fanbase API for the magical universe of **Winx Club**.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | HTML frontend (fairy browser + API explorer) |
| GET | `/characters` | List all Winx Club fairies |
| GET | `/characters/{name}` | Get a single fairy by name (case-insensitive) |
| GET | `/actors` | Voice cast list (EN + IT voice actors) |
| GET | `/docs` | Auto-generated Swagger UI |

### Query Parameters for `/characters`
- `?home_world=Domino` — filter by home world
- `?season_debut=1` — filter by season they debuted in

## Local Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit: http://localhost:8000

## Project Structure

```
winx-api/
├── main.py          # FastAPI app + SQLite DB init + all endpoints
├── requirements.txt
├── render.yaml
└── static/
    └── index.html   # Frontend UI
```

> **Important:** `index.html` must live inside the `static/` folder.

## Deploy to Render

1. Push this folder to a GitHub repository
2. Go to [render.com](https://render.com) → **New** → **Web Service**
3. Connect your GitHub repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3
5. Click **Deploy**

The `render.yaml` is already included — Render will auto-detect it.

## Example Response

### `GET /characters/bloom`
```json
{
  "id": 1,
  "name": "Bloom",
  "fairy_type": "Fairy of the Dragon Flame",
  "home_world": "Domino",
  "school": "Alfea",
  "transformation": "Sirenix",
  "power": "Dragon Flame — the most ancient and powerful magic in existence",
  "description": "...",
  "hair_color": "Auburn / Red",
  "eye_color": "Blue",
  "season_debut": 1,
  "abilities": [
    { "name": "Dragon Flame Burst", "description": "..." },
    ...
  ]
}
```

---
Winx Club © Rainbow S.r.l. — Unofficial fan project.
