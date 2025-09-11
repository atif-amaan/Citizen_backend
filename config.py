import psycopg2
import psycopg2.extras

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="citizen_app",
        user="my_app_user",
        password="11223344",
        port="5432"
    )
