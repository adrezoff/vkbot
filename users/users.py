import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    state TEXT DEFAULT 'StartState'
                )''')


def insert_user(user_id):
    if not user_in_db(user_id):
        cursor.execute('''INSERT OR IGNORE INTO users (user_id, state) VALUES (?, ?)''', (user_id, "StartState"))
        conn.commit()


def get_data(user_id):
    cursor.execute('''SELECT * FROM users WHERE user_id = ?''', (user_id,))
    return cursor.fetchone()


def set_state(user_id, state):
    cursor.execute('''UPDATE users SET state = ? WHERE user_id = ?''', (state, user_id))
    conn.commit()


def user_in_db(user_id):
    cursor.execute('''SELECT * FROM users WHERE user_id = ?''', (user_id,))
    return cursor.fetchone() is not None


def delete_user(user_id):
    cursor.execute('''DELETE FROM users WHERE user_id = ?''', (user_id,))
    conn.commit()


def close_connection():
    conn.close()
