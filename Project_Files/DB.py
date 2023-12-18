import sqlite3

conn = sqlite3.connect('../databases/testgpt.db', check_same_thread=False)


def Login(username, password):
    query = 'SELECT username, teacher_password FROM teachers WHERE username=? AND teacher_password=?;'
    cursor = conn.execute(query, (username, password))
    user = cursor.fetchone()
    return user is not None

def create(title, note, note_source, teacher_id,category_id):
    notitie = 'INSERT INTO notes (title, note, note_source, teacher_id, category_id) VALUES (?,?,?,?,?)'
    curs = conn.execute(notitie, (title, note, note_source, teacher_id,category_id))
    note = curs.fetchall()
    conn.commit()
    return note is not None

def delete(note_id):
    delete_query = 'DELETE FROM notes WHERE note_id = ?'
    conn.execute(delete_query, (note_id))
    conn.commit()
    return True

def notities():
    query2 = 'SELECT * FROM notes;'
    notes = conn.execute(query2).fetchall()
    return notes





