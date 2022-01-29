from unittest.mock import NonCallableMock
from psycopg2 import connect, sql
import urllib.parse

def connect_postgres():
    urllib.parse.uses_netloc.append("postgres")
    #url = urllib.parse.urlparse("postgres://dnahfzon:qXIKAdro1glx68jGYpWCigc4C69EzbSH@ella.db.elephantsql.com/dnahfzon")
    url = urllib.parse.urlparse("postgres://hommtnmr:hXFpq-rZYsmbO68dCcE-dw5Se7w31qaT@tyke.db.elephantsql.com/hommtnmr")
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

def get_publishers(conn):
    cursor = conn.cursor()
    sql_object = sql.SQL("SELECT id, nazwa FROM \"Wydawnictwo\"")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        table_data = None
        cursor.close()
    return table_data

def add_book(conn, book, new_genre, new_author, new_publisher):
    if new_genre:
        id_genre = add_genre(conn, book['gatunek'])
    else:
        id_genre = get_genre_id(conn, book['gatunek'])

    if new_author:
        id_author = add_author(conn, book['autor'])
    else:
        id_author = get_author_id(conn, book['autor'])

    if new_publisher:
        id_publisher = add_publisher(conn, book['wydawnictwo'])
    else:
        id_publisher = get_publisher_id(conn, book['wydawnictwo'])

    cursor = conn.cursor()
    book['data_wydania'] = f"{book['data_wydania'][8:10]}-{book['data_wydania'][5:7]}-{book['data_wydania'][0:4]}"
    sql_object = sql.SQL(f"INSERT INTO \"Ksiazka\" (tytul, ilosc_egzemplarzy, data_wydania) VALUES (\'{book['tytul']}\', {int(book['ilosc_egzemplarzy'])}, \'{book['data_wydania']}\') RETURNING ID")
    
    try:
        cursor.execute(sql_object)
        conn.commit()
        inserted_id = cursor.fetchone()[0]
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        inserted_id = -1
        cursor.close()

    cursor = conn.cursor()
    sql_object1 = sql.SQL(f"INSERT INTO \"Gatunek_Ksiazka\" (id_gatunek, id_ksiazka) VALUES ({int(id_genre)}, {int(inserted_id)})")
    sql_object2 = sql.SQL(f"INSERT INTO \"Autor_Ksiazka\" (id_autor, id_ksiazka) VALUES ({int(id_author)}, {int(inserted_id)})")
    sql_object3 = sql.SQL(f"INSERT INTO \"Wydawnictwo_Ksiazka\" (id_wydawnictwo, id_ksiazka) VALUES ({int(id_publisher)}, {int(inserted_id)})")

    try:
        cursor.execute(sql_object1)
        cursor.execute(sql_object2)
        cursor.execute(sql_object3)
        conn.commit()
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        cursor.close()

def add_genre(conn, genre):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Gatunek\" (nazwa) VALUES (\'{genre}\') RETURNING id")

    try:
        cursor.execute(sql_object)
        conn.commit()
        inserted_id = cursor.fetchone()[0]
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        inserted_id = -1
        cursor.close()
    return inserted_id

def add_author(conn, author):
    cursor = conn.cursor()
    author = author.split(' ')
    sql_object = sql.SQL(f"INSERT INTO \"Autor\" (imie, nazwisko) VALUES (\'{author[0]}\', \'{author[1]}\') RETURNING id")

    try:
        cursor.execute(sql_object)
        conn.commit()
        inserted_id = cursor.fetchone()[0]
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        inserted_id = -1
        cursor.close()
    return inserted_id

def add_publisher(conn, publisher):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Wydawnictwo\" (nazwa) VALUES (\'{publisher}\') RETURNING id")

    try:
        cursor.execute(sql_object)
        conn.commit()
        inserted_id = cursor.fetchone()[0]
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        inserted_id = -1
        cursor.close()
    return inserted_id

def get_genre_id(conn, genre):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"SELECT id FROM \"Gatunek\" WHERE nazwa=\'{genre}\'")

    try:
        cursor.execute(sql_object)
        id = int(cursor.fetchall()[0][0])
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        id = -1
        cursor.close()
    return id

def get_author_id(conn, author):
    cursor = conn.cursor()
    author = author.split(' ')
    sql_object = sql.SQL(f"SELECT id FROM \"Autor\" WHERE imie=\'{author[0]}\' AND nazwisko=\'{author[1]}\'")

    try:
        cursor.execute(sql_object)
        id = int(cursor.fetchall()[0][0])
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        id = -1
        cursor.close()
    return id

def get_publisher_id(conn, publisher):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"SELECT id FROM \"Wydawnictwo\" WHERE nazwa=\'{publisher}\'")

    try:
        cursor.execute(sql_object)
        id = int(cursor.fetchall()[0][0])
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        id = -1
        cursor.close()
    return id

def get_book_id(conn, title):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"SELECT id FROM \"Ksiazka\" WHERE tytul=\'{title}\'")

    try:
        cursor.execute(sql_object)
        id = int(cursor.fetchall()[0][0])
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        id = -1
        cursor.close()
    return id

def get_reviews(conn, book=None):
    cursor = conn.cursor()
    if not book:
        sql_object = sql.SQL("SELECT * FROM RecenzjaView")
    else:
        sql_object = sql.SQL(f"SELECT * FROM RecenzjaView WHERE \"Tytul\"=\'{book}\'")
    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        table_data = []
        cursor.close()

    return table_data

def add_review(conn, review):
    book_id = get_book_id(conn, review['tytul'])

    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Recenzja\" (id_ksiazka, ocena, opinia) VALUES ({int(book_id)}, {int(review['ocena'])}, \'{review['opinia']}\')")
    try:
        cursor.execute(sql_object)
        conn.commit()
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        cursor.close()

def get_available_books(conn):
    cursor = conn.cursor()
    sql_object = sql.SQL("SELECT * FROM DostepneKsiazkiView")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        table_data = []
        cursor.close()
    return table_data

def get_clients(conn, active_only=False):
    cursor = conn.cursor()
    if active_only:
        sql_object = sql.SQL('''
                                SELECT \"Imie\", \"Nazwisko\", \"Pesel\", \"Email\", COUNT(\"ID Wypozyczenia\")
                                FROM KlientWypozyczenieView
                                GROUP BY \"Imie\", \"Nazwisko\", \"Pesel\", \"Email\"
                                ORDER BY \"Nazwisko\"
                            ''')
    else:
        sql_object = sql.SQL("SELECT * FROM KlienciView")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        table_data = []
        cursor.close()
    return table_data

def add_client(conn, client):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Klient\" (imie, nazwisko, pesel, email) VALUES (\'{client['imie']}\', \'{client['nazwisko']}\', \'{client['pesel']}\', \'{client['email']}\')")
    try:
        cursor.execute(sql_object)
        conn.commit()
        cursor.close()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        cursor.close()