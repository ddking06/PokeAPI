import sqlite3

def create_tables():
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

def create_user(new_user_name, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Returns 1 if that username is already on the database, else 0
    check_query = "SELECT EXISTS(SELECT 1 FROM users WHERE username = ?)"
    cursor.execute(check_query, (new_user_name,))

    # Grabs the single value from the query
    exists = cursor.fetchone()[0]

    if exists:
        print(f"Sorry,  {new_user_name} is already taken.")
        cursor.close()
        conn.close()
        return None # Informs the other function it failed.

    insert_query = "INSERT INTO users(username, password) VALUES (?, ?)"
    cursor.execute(insert_query, (new_user_name, password))
    user_id = cursor.lastrowid
    
    conn.commit()

    print(f"User {new_user_name} created successfully.")

    cursor.close()
    conn.close()
    return user_id
