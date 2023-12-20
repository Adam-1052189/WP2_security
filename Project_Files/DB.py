import sqlite3

conn = sqlite3.connect('../databases/testgpt.db', check_same_thread=False)

def delete(note_id):
    delete_query = 'DELETE FROM notes WHERE note_id = ?'
    conn.execute(delete_query, (note_id, ))
    conn.commit()
    return True


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

def notities():
    query2 = 'SELECT notes.note_id, notes.note, notes.title, notes.note_source, notes.teacher_id, notes.date_created, categories.omschrijving  FROM notes INNER JOIN categories ON notes.category_id = categories.category_id;'
    notes = conn.execute(query2).fetchall()
    return notes

def get_categories():
    query = 'SELECT category_id, omschrijving FROM categories;'
    categories = conn.execute(query).fetchall()
    return categories

def adminmenu(username, teacher_password, display_name):
    query3 = 'INSERT INTO teachers (username, teacher_password, display_name) VALUES (?,?,?)'
    conn.execute(query3, (username, teacher_password, display_name))
    conn.commit()


def categoriesaanmaken(omschrijving):
    query4 = 'INSERT INTO categories (omschrijving) VALUES (?)'
    conn.execute(query4, (omschrijving,))
    conn.commit()

def aantalnotities():
    query5 = 'SELECT COUNT(note_id) FROM notes;'
    result = conn.execute(query5).fetchone()
    count = result[0] if result else 0
    return count





