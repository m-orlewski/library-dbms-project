from flask import Flask, render_template
from database import *

conn = connect_postgres()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()