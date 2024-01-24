import sqlite3
from flask import Flask, render_template, request,redirect, url_for
app = Flask(__name__,static_url_path='/static')

def get_db_connection():
    conn = sqlite3.connect('travel-website.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/results',methods= ['POST','GET'])
def results():
    conn = get_db_connection()
    if request.method == 'POST':
        location_name = request.form.get('locationname') 
        if location_name == None:
            return render_template('home.html',warning_message="Please provide destination!")
        #records = conn.execute('SELECT '+location_name+' FROM hotels').fetchall()
        conn.close()
        records = location_name
        return render_template('results.html',records=records)
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)