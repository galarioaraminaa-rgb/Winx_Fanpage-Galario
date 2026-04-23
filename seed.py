from database import get_connection

conn = get_connection()
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    fairy_type TEXT,
    home_world TEXT,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS actors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    nationality TEXT,
    character_id INTEGER,
    FOREIGN KEY(character_id) REFERENCES characters(id)
)
""")

# Insert data
cursor.execute("DELETE FROM characters")
cursor.execute("DELETE FROM actors")

characters = [
    ("Bloom", "Dragon Flame", "Earth", "Leader of the Winx Club with fire powers"),
    ("Stella", "Sun and Moon", "Solaria", "Princess with light-based powers"),
    ("Flora", "Nature", "Lynphea", "Controls plants and nature"),
    ("Musa", "Music", "Melody", "Uses sound and music magic"),
    ("Tecna", "Technology", "Zenith", "Highly logical fairy of technology"),
    ("Aisha", "Waves", "Andros", "Fairy of fluids and water")
]

cursor.executemany(
    "INSERT INTO characters (name, fairy_type, home_world, description) VALUES (?, ?, ?, ?)",
    characters
)

actors = [
    ("Molly Quinn", "American", 1),
    ("Amy Gross", "American", 2),
    ("Helena Evangeliou", "American", 3),
    ("Romina Marrocco", "Italian", 4),
    ("Morgan Decker", "American", 5),
    ("Keke Palmer", "American", 6)
]

cursor.executemany(
    "INSERT INTO actors (name, nationality, character_id) VALUES (?, ?, ?)",
    actors
)

conn.commit()
conn.close()

print("Database seeded!")
