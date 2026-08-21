import sqlite3
import bcrypt

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

def verify_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, password
    FROM users
    WHERE username = ?
    """

    cursor.execute(query, (username,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        return None

    user_id = result[0]
    stored_hash = result[1]

    if bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    ):
        return user_id

    return None

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

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    insert_query = "INSERT INTO users(username, password) VALUES (?, ?)"
    cursor.execute(
        insert_query,
        (new_user_name, hashed_password)
    )

    user_id = cursor.lastrowid
    
    conn.commit()

    print(f"User {new_user_name} created successfully.")

    cursor.close()
    conn.close()
    return user_id

def add_fav_to_db(user_id, fav_pk):
    conn = get_connection()
    cursor = conn.cursor()

    check_query = "SELECT EXISTS(SELECT 1 FROM favourites WHERE user_id = ? and pokemon_name = ?)"
    cursor.execute(check_query, (user_id, fav_pk))
    
    exists = cursor.fetchone()[0]

    if exists:
        print(f"{fav_pk} is already on the list of favourites.")
        return False

    insert_query = "INSERT INTO favourites(user_id, pokemon_name) VALUES (?, ?)"
    cursor.execute(insert_query, (user_id, fav_pk))    
    print(f"{fav_pk} added to favourites.")
    conn.commit()
    cursor.close()
    conn.close()

    return True

def get_user_favourites(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT pokemon_name
    FROM favourites
    WHERE user_id = ?
    """

    cursor.execute(query, (user_id,))

    favourites = cursor.fetchall()

    cursor.close()
    conn.close()

    return favourites