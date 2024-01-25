import sqlite3 as sql

def insertUser(username,pwd):
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('INSERT INTO users VALUES (?,?)',(username,pwd))
    con.commit()
    con.close()

def retrieveUsers():
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT username,pwd FROM users")
    users = cur.fetchall()
    return users