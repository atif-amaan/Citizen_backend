from config import get_db_connection
import psycopg2
import psycopg2.extras

def create_report(user_id, issue_type, description, latitude, longitude, image_url):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO reports (user_id, issue_type, description, latitude, longitude, image_url, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
    """
    cur.execute(sql, (user_id, issue_type, description, latitude, longitude, image_url, "Pending"))
    report_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return report_id

def get_all_reports():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM reports ORDER BY created_at DESC")
    reports = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in reports]

def update_report_status(report_id, status):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = "UPDATE reports SET status = %s WHERE id = %s"
    cur.execute(sql, (status, report_id))
    conn.commit()
    cur.close()
    conn.close()
    return True

# models/report_model.py
def get_reports_by_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM reports WHERE user_id = %s ORDER BY created_at DESC"
    cur.execute(query, (user_id,))
    reports = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in reports]   # 👈 convert to list of dicts