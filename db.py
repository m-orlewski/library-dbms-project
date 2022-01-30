from unittest.mock import NonCallableMock
from psycopg2 import connect, sql
import urllib.parse

def connect_postgres():
    urllib.parse.uses_netloc.append("postgres")
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
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        table_data = []
    finally:
        cursor.close()

    return table_data

def get_genres(conn):
    cursor = conn.cursor()
    sql_object = sql.SQL("SELECT id, nazwa FROM \"Gatunek\"")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        table_data = []
    finally:
        cursor.close()

    return table_data

def get_authors(conn):
    cursor = conn.cursor()
    sql_object = sql.SQL("SELECT id, imie, nazwisko FROM \"Autor\"")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall() 
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        table_data = []
    finally:
        cursor.close()

    return table_data

def get_publishers(conn):
    cursor = conn.cursor()
    sql_object = sql.SQL("SELECT id, nazwa FROM \"Wydawnictwo\"")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        table_data = []
    finally:
        cursor.close()

    return table_data

def add_book(conn, book):

    id_genre = get_genre_id(conn, book['gatunek'])
    id_author = get_author_id(conn, book['autor'])
    id_publisher = get_publisher_id(conn, book['wydawnictwo'])

    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Ksiazka\" (tytul, ilosc_egzemplarzy, data_wydania) VALUES (\'{book['tytul']}\', {int(book['ilosc_egzemplarzy'])}, \'{book['data_wydania']}\') RETURNING ID")
    
    try:
        cursor.execute(sql_object)
        conn.commit()
        book_id = cursor.fetchone()[0]
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

    cursor = conn.cursor()
    sql_object1 = sql.SQL(f"INSERT INTO \"Gatunek_Ksiazka\" (id_gatunek, id_ksiazka) VALUES ({int(id_genre)}, {int(book_id)})")
    sql_object2 = sql.SQL(f"INSERT INTO \"Autor_Ksiazka\" (id_autor, id_ksiazka) VALUES ({int(id_author)}, {int(book_id)})")
    sql_object3 = sql.SQL(f"INSERT INTO \"Wydawnictwo_Ksiazka\" (id_wydawnictwo, id_ksiazka) VALUES ({int(id_publisher)}, {int(book_id)})")

    try:
        cursor.execute(sql_object1)
        cursor.execute(sql_object2)
        cursor.execute(sql_object3)
        conn.commit()
        return True
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def add_genre(conn, genre):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Gatunek\" (nazwa) VALUES (\'{genre}\') RETURNING id")

    try:
        cursor.execute(sql_object)
        conn.commit()
        return True
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def add_author(conn, author):
    cursor = conn.cursor()
    fname, lname = author.split(' ')
    sql_object = sql.SQL(f"INSERT INTO \"Autor\" (imie, nazwisko) VALUES (\'{fname}\', \'{lname}\') RETURNING id")

    try:
        cursor.execute(sql_object)
        conn.commit()
        return True
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def add_publisher(conn, publisher):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Wydawnictwo\" (nazwa) VALUES (\'{publisher}\') RETURNING id")

    try:
        cursor.execute(sql_object)
        conn.commit()
        return True
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def add_status(conn, status):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Status\" (status) VALUES (\'{status}\') RETURNING id")

    try:
        cursor.execute(sql_object)
        conn.commit()
        return True
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def get_genre_id(conn, genre):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"SELECT id FROM \"Gatunek\" WHERE nazwa=\'{genre}\'")

    try:
        cursor.execute(sql_object)
        id = cursor.fetchall()[0][0]
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        id = 0
    finally:
        cursor.close()

    return id

def get_author_id(conn, author):
    cursor = conn.cursor()
    author = author.split(' ')
    sql_object = sql.SQL(f"SELECT id FROM \"Autor\" WHERE imie=\'{author[0]}\' AND nazwisko=\'{author[1]}\'")

    try:
        cursor.execute(sql_object)
        id = cursor.fetchall()[0][0]
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        id = 0
    finally:
        cursor.close()

    return id

def get_publisher_id(conn, publisher):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"SELECT id FROM \"Wydawnictwo\" WHERE nazwa=\'{publisher}\'")

    try:
        cursor.execute(sql_object)
        id = cursor.fetchall()[0][0]
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        id = 0
    finally:
        cursor.close()

    return id

def get_status_id(conn, status):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"SELECT id FROM \"Status\" WHERE nazwa=\'{status}\'")

    try:
        cursor.execute(sql_object)
        id = cursor.fetchall()[0][0]
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        id = 0
    finally:
        cursor.close()

    return id

def get_book_id(conn, title):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"SELECT id FROM \"Ksiazka\" WHERE tytul=\'{title}\'")

    try:
        cursor.execute(sql_object)
        id = cursor.fetchall()[0][0]
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        id = 0
    finally:
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
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        table_data = []
    finally:
        cursor.close()

    return table_data

def add_review(conn, review):
    cursor = conn.cursor()
    book_id = get_book_id(conn, review['tytul'])
    sql_object = sql.SQL(f"INSERT INTO \"Recenzja\" (id_ksiazka, ocena, opinia) VALUES ({int(book_id)}, {int(review['ocena'])}, \'{review['opinia']}\')")

    try:
        cursor.execute(sql_object)
        conn.commit()
        return True
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        return False
    finally:    
        cursor.close()

def get_available_books(conn):
    cursor = conn.cursor()
    sql_object = sql.SQL("SELECT * FROM DostepneKsiazkiView")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        table_data = []
    finally:
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
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        table_data = []
    finally:
        cursor.close()

    return table_data

def add_client(conn, client):
    cursor = conn.cursor()

    sql_object = sql.SQL(f"INSERT INTO \"Klient\" (imie, nazwisko, pesel, email) VALUES (\'{client['imie']}\', \'{client['nazwisko']}\', \'{client['pesel']}\', \'{client['email']}\')")
    
    try:
        cursor.execute(sql_object)
        conn.commit()
        return True
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def add_reservation(conn, book, pesel, data_rezerwacji):
    cursor = conn.cursor()

    client_id = get_client_id(conn, pesel)
    sql_object = sql.SQL(f"INSERT INTO \"Rezerwacja\" (id_ksiazka, id_klient, data_rezerwacji) VALUES ({int(book[0])}, {client_id}, \'{data_rezerwacji}\')")

    try:
        cursor.execute(sql_object)
        conn.commit()
        return True
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def add_rent(conn, book, pesel, data_wypozyczenia, data_oddania):
    cursor = conn.cursor()

    client_id = get_client_id(conn, pesel)
    sql_object = sql.SQL(f"INSERT INTO \"Wypozyczenie\" (id_ksiazka, id_klient, data_wypozyczenia, data_oddania) VALUES ({int(book[0])}, {client_id}, \'{data_wypozyczenia}\', \'{data_oddania}\')")

    try:
        cursor.execute(sql_object)
        conn.commit()
        return True
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
    finally:
        cursor.close()

def get_client_id(conn, pesel):
    cursor = conn.cursor()

    sql_object = sql.SQL(f"SELECT id FROM \"Klient\" WHERE pesel = \'{pesel}\'")

    try:
        cursor.execute(sql_object)
        id = cursor.fetchall()[0][0]
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        id = 0
    finally:
        cursor.close()
    return id

def get_statuses(conn):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"SELECT id, status FROM \"Status\"")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        table_data = []
    finally:
        cursor.close()

    return table_data

def get_reservations(conn):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"SELECT * FROM RezerwacjeView")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        table_data = []
    finally:
        cursor.close()

    return table_data

def change_status(conn, id, status_id):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"UPDATE \"Rezerwacja\" SET id_status = {status_id} WHERE id = {id}")

    try:
        cursor.execute(sql_object)
        conn.commit()
        return True
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def get_rented(conn):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"SELECT * FROM \"Wypozyczenie\" WHERE aktualne = \'TRUE\'")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        table_data = []
    finally:
        cursor.close()

    return table_data

def return_book(conn, rent_id):
    cursor = conn.cursor()
    sql_object = sql.SQL(f"UPDATE \"Wypozyczenie\" SET aktualne = \'FALSE\' WHERE id = {rent_id}")

    try:
        cursor.execute(sql_object)
        conn.commit()
        return True
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def get_detailed_rental(conn):
    cursor = conn.cursor()
    sql_object = sql.SQL("SELECT * FROM WypozyczenieView")

    try:
        cursor.execute(sql_object)
        table_data = cursor.fetchall()
    except Exception as e:
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", e)
        conn.rollback()
        table_data = []
    finally:
        cursor.close()

    return table_data       


