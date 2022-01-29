from unittest.mock import NonCallableMock
from psycopg2 import connect, sql
import urllib.parse

def connect_postgres():
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse("postgres://dnahfzon:qXIKAdro1glx68jGYpWCigc4C69EzbSH@ella.db.elephantsql.com/dnahfzon")
    print ("\nconnecting to PostgreSQL")
    try:
        conn = connect (
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except Exception as err:
        print ("PostgreSQL Connect() ERROR:", err)
        conn = None

    return conn

def get_books(conn, genre=None, author=None):
    cursor = conn.cursor()
    if not genre and not author:
        sql_object = sql.SQL("SELECT * FROM KsiazkiView")
    elif genre and author:
        author = author.split(' ')
        sql_object = sql.SQL(f"SELECT * FROM KsiazkiView WHERE \"Gatunek\"='{genre}' AND \"Imie\"='{author[0]}' AND \"Nazwisko\"='{author[1]}'")
    elif genre:
        sql_object = sql.SQL(f"SELECT * FROM KsiazkiView WHERE \"Gatunek\"='{genre}'")
    elif author:
        author = author.split(' ')
        sql_object = sql.SQL(f"SELECT * FROM KsiazkiView WHERE \"Imie\"='{author[0]}' AND \"Nazwisko\"='{author[1]}'")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        table_data = []
        cursor.close()
    print(table_data)
    return table_data

def get_genres(conn):
    cursor = conn.cursor()
    sql_object = sql.SQL("SELECT id, nazwa FROM \"Gatunek\"")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        table_data = None
        cursor.close()
    return table_data

def get_authors(conn):
    cursor = conn.cursor()
    sql_object = sql.SQL("SELECT id, imie, nazwisko FROM \"Autor\"")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        table_data = None
        cursor.close()
    return table_data
