import sqlite3

conn = sqlite3.connect('databases/testgpt.db')

def login(username,password):
    query= 'SELECT username, teacher_password FROM teachers WHERE username=? AND teacher_password=?;'
    cursor= conn.execute(query, (username,password))
    user = cursor.fetchone()
    return user is not None
