import sqlite3

# Создание подключения к базе данных
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы пользователей, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    state TEXT DEFAULT 'StartState'
                )''')


# Вставка нового пользователя
def insert_user(user_id):
    if not user_in_db(user_id):
        cursor.execute('''INSERT OR IGNORE INTO users (user_id, state) VALUES (?, ?)''', (user_id, "StartState"))
        conn.commit()


# Получение информации о пользователе по его ID
def get_data(user_id):
    cursor.execute('''SELECT * FROM users WHERE user_id = ?''', (user_id,))
    return cursor.fetchone()


# Установка состояния пользователя в базе данных
def set_state(user_id, state):
    cursor.execute('''UPDATE users SET state = ? WHERE user_id = ?''', (state, user_id))
    conn.commit()


# Проверка существования пользователя в базе данных
def user_in_db(user_id):
    cursor.execute('''SELECT * FROM users WHERE user_id = ?''', (user_id,))
    return cursor.fetchone() is not None


def delete_user(user_id):
    cursor.execute('''DELETE FROM users WHERE user_id = ?''', (user_id,))
    conn.commit()


# Закрытие соединения с базой данных
def close_connection():
    conn.close()
