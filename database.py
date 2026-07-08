import sqlite3

conn = sqlite3.connect("pokedex.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               password TEXT NOT NULL)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS favourites (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER,
               pokemon_name TEXT,
               FOREIGN KEY(user_id) REFERENCES users(id)
               )               
""")

conn.commit()
conn.close()

def get_connection():
    return sqlite3.connect("pokedex.db")

def create_user():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users")
    
    user_names = cursor.fetchall()

    print(user_names)
    cursor.close()
    conn.close()

create_user()