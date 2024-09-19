import sqlite3
import bcrypt


def hash_passwords(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.execute('SELECT teacher_id, teacher_password FROM teachers')
    users = cursor.fetchall()

    for user in users:
        teacher_id, plain_password = user
        if not plain_password.startswith('$2b$'):
            hashed_password = bcrypt.hashpw(
                plain_password.encode('utf-8'), bcrypt.gensalt())
            conn.execute('UPDATE teachers SET teacher_password = ? WHERE teacher_id = ?',
                         (hashed_password.decode('utf-8'), teacher_id))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    database_path = 'testgpt.db'
    hash_passwords(database_path)
    print("✅ Wachtwoorden zijn gehashed en opnieuw opgeslagen in de database.")
