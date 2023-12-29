import sqlite3

conn = sqlite3.connect('../databases/testgpt.db')

def delete(note_id):
    delete_query = 'DELETE FROM notes WHERE note_id = ?'
    conn = sqlite3.connect('../databases/testgpt.db')
    conn.execute(delete_query, (note_id, ))
    conn.commit()
    return True


def Login(username, password):
    query = 'SELECT username, teacher_password, teacher_id FROM teachers WHERE username=? AND teacher_password=?;'
    conn = sqlite3.connect('../databases/testgpt.db')
    cursor = conn.execute(query, (username, password))
    user = cursor.fetchone()
    if user is None:
        return False
    return user[2]

def check_admin(teacher_id):
    print(teacher_id)
    query = 'SELECT teacher_id, is_admin FROM teachers WHERE teacher_id=? AND is_admin=1'
    conn = sqlite3.connect('../databases/testgpt.db')
    cursor = conn.execute(query, (str(teacher_id),))
    user = cursor.fetchone()
    return user is not None

def create(title, note, note_source, teacher_id,category_id):
    notitie = 'INSERT INTO notes (title, note, note_source, teacher_id, category_id) VALUES (?,?,?,?,?)'
    conn = sqlite3.connect('../databases/testgpt.db')
    curs = conn.execute(notitie, (title, note, note_source, teacher_id,category_id))
    note = curs.fetchall()
    conn.commit()
    return note is not None

def notities():
    query2 = 'SELECT notes.note_id, notes.note, notes.title, notes.note_source, teachers.display_name, notes.date_created, categories.omschrijving  FROM notes INNER JOIN categories ON notes.category_id = categories.category_id INNER JOIN teachers on teachers.teacher_id = notes.teacher_id;'
    conn = sqlite3.connect('../databases/testgpt.db')
    notes = conn.execute(query2).fetchall()
    return notes

def get_categories():
    query = 'SELECT category_id, omschrijving FROM categories;'
    conn = sqlite3.connect('../databases/testgpt.db')
    categories = conn.execute(query).fetchall()
    return categories

def get_teacher():
    query = 'SELECT teacher_id, display_name FROM teachers;'
    conn = sqlite3.connect('../databases/testgpt.db')
    teachers = conn.execute(query).fetchone()
    return teachers

def adminmenu(username, teacher_password, display_name):
    query3 = 'INSERT INTO teachers (username, teacher_password, display_name) VALUES (?,?,?)'
    conn = sqlite3.connect('../databases/testgpt.db')
    conn.execute(query3, (username, teacher_password, display_name))
    conn.commit()

def adminscherm():
    query = 'SELECT display_name, username, teacher_password, teacher_id FROM teachers;'
    conn = sqlite3.connect('../databases/testgpt.db')
    gebruikers = conn.execute(query).fetchall()
    return gebruikers

def delete_gebruiker(teacher_id):
    query = 'DELETE FROM teachers WHERE teacher_id = ?'
    conn = sqlite3.connect('../databases/testgpt.db')
    conn.execute(query, (teacher_id, ))
    conn.commit()
    return True

def categoriesaanmaken(omschrijving):
    query4 = 'INSERT INTO categories (omschrijving) VALUES (?)'
    conn = sqlite3.connect('../databases/testgpt.db')
    conn.execute(query4, (omschrijving,))
    conn.commit()

def categories():
    query10 = 'SELECT category_id, omschrijving, date_created FROM categories;'
    conn = sqlite3.connect('../databases/testgpt.db')
    conn.row_factory = sqlite3.Row
    categories = conn.execute(query10).fetchall()
    return categories

def aantalnotities():
    query5 = 'SELECT COUNT(note_id) FROM notes;'
    conn = sqlite3.connect('../databases/testgpt.db')
    result = conn.execute(query5).fetchone()
    count = result[0] if result else 0
    return count

def get_note_id(note_id):
    query = 'SELECT note_id, title, note, note_source, category_id FROM notes WHERE note_id=?;'
    conn = sqlite3.connect('../databases/testgpt.db')
    cursor = conn.execute(query, (note_id,))
    note = cursor.fetchone()
    return note

def update_note(note_id,title,note,note_source,category_id):
    conn = sqlite3.connect('../databases/testgpt.db')
    update_query = '''
    UPDATE notes
    SET title=?, note=?, note_source=?, category_id=?
    WHERE note_id=?
    '''

    conn.execute(update_query,(title,note,note_source,category_id,note_id))
    conn.commit()

