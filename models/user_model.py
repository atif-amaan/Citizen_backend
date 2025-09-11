from config import get_db_connection
import psycopg2
import psycopg2.extras

def create_user(name, email, password, role="citizen"):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s) RETURNING id"
    cur.execute(sql, (name, email, password, role))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return user_id

def get_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return dict(user) if user else None
