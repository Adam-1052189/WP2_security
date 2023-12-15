import sqlite3

conn = sqlite3.connect('../databases/testgpt.db', check_same_thread=False)

def login(username, password):
    query = 'SELECT username, teacher_password FROM teachers WHERE username=? AND teacher_password=?;'
    cursor = conn.execute(query, (username, password))
    user = cursor.fetchone()
    return user is not None

def create(title, note, vakken):
    query1 = "INSERT INTO notes VALUES('', '{title}', '', '', '', '{note}', '{vakken}', '');"
    cursor = conn.execute(query1, (title, note, vakken))
    cursor.execute(query1)
    conn.commit()


