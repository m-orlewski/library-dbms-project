from webbrowser import get
from flask import Flask, render_template, request, flash, redirect, url_for
from database import *
import os

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

    new_genre = False
    new_author = False
    new_publisher = False

    book = {}
    book['tytul'] = request.form.get('tytul')
    
    book['gatunek'] = request.form.get('select-genre')
    if book['gatunek'] == '0':
        book['gatunek'] = request.form.get('add-genre')
        new_genre = True

    book['autor'] = request.form.get('select-author')
    if book['autor'] == '0':
        book['autor'] = request.form.get('add-author')
        new_author = True

    book['wydawnictwo'] = request.form.get('select-publisher')
    if book['wydawnictwo'] == '0':
        book['wydawnictwo'] = request.form.get('add-publisher')
        new_publisher = True

    book['data_wydania'] = request.form.get('date')
    book['ilosc_egzemplarzy'] = request.form.get('count')
    
    for val in book.values():
        if val == '':
            flash('Formularz wypełniony niepoprawnie. Spróbuj ponownie.')
            return redirect(url_for('add_book_get'))

    add_book(conn, book, new_genre, new_author, new_publisher)

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

    add_review(conn, review)
    return redirect(url_for('lind_reviews_get'))

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

    add_client(conn, client)
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
        msg += f'nowy gatunek({genre}), '
        add_genre(conn, genre)
    if author != '':
        msg += f'nowy autor({author}), '
        add_author(conn, author)
    if publisher != '':
        msg += f'nowe wydawnictwo({publisher}), '
        add_publisher(conn, publisher)
    if status != '':
        msg += f'nowy status({status}), '
        add_status(conn, status)

    if msg == '':
        flash('Formularz wypełniony niepoprawnie. Spróbuj ponownie.')
    else:
        msg = 'Dodano ' + msg
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

    add_reservation(conn, book, pesel, data_rezerwacji)
    return redirect(url_for('add_reservation_get'))

@app.route("/addRent", methods=['GET'])
def add_rent_get():
    books = get_available_books(conn)
    return render_template('add_rent.html', books=books)

@app.route("/addRent", methods=['POST'])
def add_rent_get():
    books = get_available_books(conn)
    return render_template('add_rent.html', books=books)


if __name__ == '__main__':
    app.run()