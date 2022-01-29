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
    
@app.route("/showReviews", methods=['GET'])
def show_reviews_get():
    reviews = get_reviews(conn)
    books = get_books(conn)

    return render_template('reviews.html', books=books, reviews=reviews)

@app.route("/showReviews", methods=['POST'])
def show_reviews_post():

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
    return redirect(url_for('show_reviews_get'))

if __name__ == '__main__':
    app.run()