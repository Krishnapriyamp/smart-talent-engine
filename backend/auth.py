import hashlib
import sqlite3

def create_user_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        company TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()

def hash_password(password):
    if password is None:
        return None
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(user):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        hashed_password = hash_password(user["password"])
        c.execute("""
        INSERT INTO users (name, email, password, company, role)
        VALUES (?, ?, ?, ?, ?)
        """, (
            user["name"].strip(),
            user["email"].strip().lower(),
            hashed_password,
            user["company"].strip(),
            user["role"].strip()
        ))

        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    hashed_password = hash_password(password)
    c.execute("SELECT * FROM users WHERE email=? AND password=?",
              (email.strip().lower(), hashed_password))

    user = c.fetchone()
    conn.close()

    return user is not None