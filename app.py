from webbrowser import get
from flask import Flask, render_template, request
from database import *

conn = connect_postgres()
app = Flask(__name__)

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
    

if __name__ == '__main__':
    app.run()