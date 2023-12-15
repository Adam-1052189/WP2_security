import sqlite3

conn = sqlite3.connect('../databases/testgpt.db', check_same_thread=False)

def login(username, password):
    query = 'SELECT username, teacher_password FROM teachers WHERE username=? AND teacher_password=?;'
    cursor = conn.execute(query, (username, password))
    user = cursor.fetchone()
    return user is not None

def create(title, note):
    conn.execute('INSERT INTO notes (title, note) VALUES (?, ?)',
                 (title, note))
    conn.commit()
    conn.close()


