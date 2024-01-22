import sqlite3
from flask import Flask, render_template
app = Flask(__name__,static_url_path='/static')

def get_db_connection():
    conn = sqlite3.connect('travel-website.db')



@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)