from flask import Flask, render_template, request,redirect, url_for,session
import sqlite3
app = Flask(__name__,static_url_path='/static')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS USERS (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT, password TEXT UNIQUE,email TEXT, phonenumber INTEGER)''')
    return conn


@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/results',methods= ['POST','GET'])
def results():
    if request.method == 'POST':
        location_name = request.form.get('locationname') 
        if location_name == None:
            return render_template('home.html',warning_message="Please provide destination!")
        records = location_name
        return render_template('results.html',records=records)
    return render_template('home.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        email = request.form['email']
        phnum = request.form['phnum']
        conn = get_db_connection()
        conn.execute('''INSERT INTO USERS (username,password,email,phonenumber) VALUES (?,?,?,?)''',(username,pwd,email,phnum))
        conn.commit()
        return render_template('login.html')
    else:
        return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    conn = get_db_connection()
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        user = conn.execute(f'SELECT username,password FROM USERS WHERE username=? and password=?',(username,pwd)).fetchone()
        if user is not None:
            if user[1] == pwd:
                conn.close()
                return redirect(url_for('home'))          
            else:
                conn.close()
                return render_template('login.html')
        else:
            conn.close()
            return render_template('login.html')
    else:
        conn.close()
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)