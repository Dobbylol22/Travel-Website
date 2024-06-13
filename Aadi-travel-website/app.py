from flask import Flask, render_template, request,redirect, url_for,session, jsonify
from datetime import datetime
import sqlite3
app = Flask(__name__,static_url_path='/static')
import nltk
#nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('model.h5')
import json
import random
intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence,words,show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s"%w)
    return(np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

def get_db_connection():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS USERS (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT, password TEXT UNIQUE,email TEXT, phonenumber INTEGER)''')
    return conn

def get_db_connection1():
    conn = sqlite3.connect('travel-website.db')
    cur = conn.cursor()
    return conn

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/results',methods= ['POST','GET'])
def results():
    conn = get_db_connection1()
    if request.method == 'POST':
        location_name = request.form.get('locationname').capitalize()
        if location_name == None:
            return render_template('home.html',warning_message="Please provide destination!")
        else:
            result = conn.execute(f'SELECT * FROM hotels WHERE hotel_location = ?',(location_name,)).fetchall()
            conn.commit()
        return render_template('results.html',result=result)
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
    
@app.route("/hotel")
def hotel():
    conn = get_db_connection1()
    hotel_name = request.args.get('str')
    result = conn.execute(f'SELECT * FROM hotels WHERE hotel_name LIKE ?',('%'+hotel_name+'%',)).fetchone()
    conn.commit()
    return render_template("hotel.html", result=result)

@app.route('/calculate_days', methods=['POST'])
def calculate_days():
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    # Convert date strings to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Calculate the number of days
    num_days = (end_date - start_date).days
    return jsonify({'num_days': num_days})

@app.route("/chat")
def chat():
    return render_template("chat.html")
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

if __name__ == '__main__':
    app.run()