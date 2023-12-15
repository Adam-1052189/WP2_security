import sqlite3

conn = sqlite3.connect('./databases/testgpt.db', check_same_thread=False)
conn.row_factory = sqlite3.Row

def login(username, password):
    query = 'SELECT username, teacher_password FROM teachers WHERE username=? AND teacher_password=?;'
    cursor = conn.execute(query, (username, password))
    user = cursor.fetchone()
    return user is not None

def create(title, note, note_source, teacher_id,category_id):
    notitie = 'INSERT INTO notes (title, note, note_source, teacher_id, category_id) VALUES (?,?,?,?,?)'
    curs = conn.execute(notitie, (title, note, note_source, teacher_id,category_id))
    note = curs.fetchall()
    conn.commit()
    conn.close()
    return note is not None

def notes():
    notes = conn.execute('Select * FROM notes')
    note = notes.fetchall()
    conn.close()
    return note is not None

