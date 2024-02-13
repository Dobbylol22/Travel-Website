from flask import Flask, render_template, request,redirect, url_for,session
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
    
@app.route("/chat")
def chat():
    return render_template("chat.html")
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

if __name__ == '__main__':
    app.run()