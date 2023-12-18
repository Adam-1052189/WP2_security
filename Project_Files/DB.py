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

def notities():
    query2 = 'SELECT * FROM notes;'
    notes = conn.execute(query2).fetchall()
    return notes

def docenten():
    query2 = 'SELECT * FROM teachers;'
    teachers = conn.execute(query2).fetchall()
    return teachers
def admindeleteteacher(teacher_id):
    try:
        cursor = conn.cursor()
        query = 'DELETE FROM teachers WHERE teacher_id=?;'
        cursor.execute(query, (teacher_id,))
        conn.commit()
        return "Teacher deleted successfully"
    except Exception as e:
        return f"Error deleting teacher: {str(e)}"
    finally:
        if conn:
            conn.close()
def createteacher(display_name, username, teacher_password, date_created, is_admin):
    try:
        cursor = conn.cursor()
        query = '''
            INSERT INTO teachers (display_name, username, teacher_password, date_created, is_admin)
            VALUES (?, ?, ?, ?, ?);
        '''
        cursor.execute(query, (display_name, username, teacher_password, date_created, is_admin))
        conn.commit()
        return "Teacher created successfully"
    except Exception as e:
        return f"Error creating teacher: {str(e)}"
    finally:
        if conn:
            conn.close()






