from webbrowser import get
from flask import Flask, render_template, request, flash, redirect, url_for
from database import *
import os
from datetime import date

conn = connect_postgres()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

@app.route("/")
def home():
    return render_template('base.html')

@app.route("/listBooks", methods=['GET'])
def list_books_get():
    table_data = get_books(conn)
    genres = get_genres(conn)
    authors = get_authors(conn)

    return render_template('books.html', data=table_data, genres=genres, authors=authors)

@app.route("/listBooks", methods=['POST'])
def list_books_post():
    genres = get_genres(conn)
    authors = get_authors(conn)

    choosen_genre = request.form.get('select-genre')
    choosen_author = request.form.get('select-author')

    if choosen_genre == '0':
        choosen_genre = None
    if choosen_author == '0':
        choosen_author = None

    table_data = get_books(conn, choosen_genre, choosen_author)

    return render_template('books.html', data=table_data, genres=genres, authors=authors)

@app.route("/addBook", methods=['GET'])
def add_book_get():
    genres = get_genres(conn)
    authors = get_authors(conn)
    publishers = get_publishers(conn)

    return render_template('add_book.html', genres=genres, authors=authors, publishers=publishers)

@app.route("/addBook", methods=['POST'])
def add_book_post():

    book = {}
    book['tytul'] = request.form.get('tytul')
    
    book['gatunek'] = request.form.get('select-genre')
    book['autor'] = request.form.get('select-author')
    book['wydawnictwo'] = request.form.get('select-publisher')

    if book['gatunek'] == '0' and book['autor'] == '0' and book['wydawnictwo'] == '0':
        flash('Formularz wypełniony niepoprawnie. Spróbuj ponownie.')
        return redirect(url_for('add_book_get'))

    book['data_wydania'] = request.form.get('date')
    book['ilosc_egzemplarzy'] = request.form.get('count')
    
    for val in book.values():
        if val == '':
            flash('Formularz wypełniony niepoprawnie. Spróbuj ponownie.')
            return redirect(url_for('add_book_get'))
    
    if not add_book(conn, book):
        flash('Nie udało się dodać książki. Spróbuj ponownie.')
        return redirect(url_for('add_book_get'))
    else:
        flash('Książka dodana do bazy.')
        return redirect(url_for('list_books_get'))
    
@app.route("/listReviews", methods=['GET'])
def list_reviews_get():
    reviews = get_reviews(conn)
    books = get_books(conn)

    return render_template('reviews.html', books=books, reviews=reviews)

@app.route("/listReviews", methods=['POST'])
def list_reviews_post():
    book = request.form.get('select-book')

    if book != '0':
        reviews = get_reviews(conn, book)
    else:
        reviews = get_reviews(conn)
    books = get_books(conn)

    return render_template('reviews.html', books=books, reviews=reviews)

@app.route("/addReview", methods=['GET'])
def add_review_get():
    books = get_books(conn)

    return render_template('add_review.html', books=books)

@app.route("/addReview", methods=['POST'])
def add_review_post():
    review = {}

    review['tytul'] = request.form.get('select-book')
    review['ocena'] = request.form.get('rating')
    review['opinia'] = request.form.get('review')

    if review['ocena'] == '' or review['opinia'] is None:
        flash('Formularz wypełniony niepoprawnie. Spróbuj ponownie.')
        return redirect(url_for('add_review_get'))

    if not add_review(conn, review):
        flash('Nie udało się dodać recenzji. Spróbuj ponownie.')
        return redirect(url_for('add_review_get'))
    else:
        flash('Recenzja dodana do bazy.')
        return redirect(url_for('list_reviews_get'))

@app.route("/listClients", methods=['GET'])
def list_clients_get():
    active_clients = get_clients(conn, True)
    all_clients = get_clients(conn)

    return render_template('clients.html', active_clients=active_clients, all_clients=all_clients)

@app.route("/addClient", methods=['GET'])
def add_client_get():
    return render_template('add_client.html')

@app.route("/addClient", methods=['POST'])
def add_client_post():
    client = {}

    client['pesel'] = request.form.get('pesel')
    client['imie'] = request.form.get('imie')
    client['nazwisko'] = request.form.get('nazwisko')
    client['email'] = request.form.get('email')

    for el in client.values():
        if el == '':
            flash('Formularz wypełniony niepoprawnie. Spróbuj ponownie.')
            return redirect(url_for('add_client_get'))

    if not add_client(conn, client):
        flash('Nie udało się dodać klienta. Spróbuj ponownie.')
        return redirect(url_for('add_client_get'))
    else:
        flash('Klient dodany do bazy.')
        return redirect(url_for('list_clients_get'))

@app.route("/addTables", methods=['GET'])
def add_tables_get():
    return render_template('add_tables.html')

@app.route("/addTables", methods=['POST'])
def add_tables_post():
    genre = request.form.get('add-genre')
    author = request.form.get('add-author')
    publisher = request.form.get('add-publisher')
    status = request.form.get('add-status')

    msg = ''
    if genre != '':
        if add_genre(conn, genre):
            msg += f'dodano nowy gatunek({genre}), '
        else:
            msg += f'nie udało się dodać nowego gatunku({genre}), '
    if author != '':
        if add_author(conn, author):
            msg += f'dodano nowego autora({author}), '
        else:
            msg += f'nie udało się dodać nowego autora({author}), '
    if publisher != '':
        if add_publisher(conn, publisher):
            msg += f'dodano nowe wydawnictwo({publisher}), '
        else:
            msg += f'nie udało się dodać nowego wydawnictwa({publisher}), '
    if status != '':
        if add_status(conn, status):
            msg += f'dodano nowy status({status}), '
        else:
            msg += f'nie udało się dodań nowego statusu({status}), '

    if msg == '':
        flash('Formularz wypełniony niepoprawnie. Spróbuj ponownie.')
    else:
        msg = 'Rezultat: ' + msg
        flash(msg[:-2])

    return redirect(url_for('add_tables_get'))

@app.route("/addReservation", methods=['GET'])
def add_reservation_get():
    books = get_available_books(conn)

    return render_template('add_reservation.html', books=books)

@app.route("/addReservation", methods=['POST'])
def add_reservation_post():
    book = request.form.get('select-book')
    pesel = request.form.get('pesel')
    data_rezerwacji = request.form.get('date')

    if book == '' or pesel == '' or data_rezerwacji == '':
        flash('Formularz wypełniony niepoprawnie. Spróbuj ponownie.')
        return redirect(url_for('add_reservation_get'))

    if not add_reservation(conn, book, pesel, data_rezerwacji):
        flash('Nie udało się dodać rezerwacji. Spróbuj ponownie.')
        return redirect(url_for('add_reservation_get'))
    else:
        flash('Rezerwacja dodana do bazy.')
        return redirect(url_for('add_reservation_get'))

@app.route("/addRent", methods=['GET'])
def add_rent_get():
    books = get_available_books(conn)
    return render_template('add_rent.html', books=books)

@app.route("/addRent", methods=['POST'])
def add_rent_post():
    book = request.form.get('select-book')
    print(book)
    pesel = request.form.get('pesel')
    data_wypozyczenia = date.today()
    data_oddania = request.form.get('return-date')
    
    if book == '' or pesel == '' or data_oddania == '':
        flash('Formularz wypełniony niepoprawnie. Spróbuj ponownie.')
        return redirect(url_for('add_rent_get'))

    if not add_rent(conn, book, pesel, data_wypozyczenia, data_oddania):
        flash('Nie udało się dodać wypożyczenia. Spróbuj ponownie.')
        return redirect(url_for('add_rent_get'))
    else:
        flash('Wypożyczenie dodane do bazy.')
        return redirect(url_for('add_rent_get'))

@app.route("/changeStatus", methods=['GET'])
def change_status_get():
    statuses = get_statuses(conn)
    reservations = get_reservations(conn)
    return render_template('update_status.html', reservations=reservations, statuses=statuses)

@app.route("/changeStatus", methods=['POST'])
def change_status_post():
    reservation_id = int(request.form.get('reservation-id'))
    new_status = request.form.get('select-status')

    reservations = get_reservations(conn)
    ids = [int(reservations[i][0]) for i in range(len(reservations))]

    if new_status == '0' or reservation_id not in ids:
        flash('Formularz wypełniony niepoprawnie. Spróbuj ponownie.')
        return redirect(url_for('change_status_get'))

    if not change_status(conn, reservation_id, new_status):
        flash('Nie udało się zmienić statusu rezerwacji. Spróbuj ponownie.')
        return redirect(url_for('change_status_get'))
    else:
        flash('Status rezerwacji zmieniony.')
        return redirect(url_for('change_status_get'))



if __name__ == '__main__':
    app.run()