import sqlite3

conn = sqlite3.connect('bot.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY,
        username TEXT,
        chat_id INTEGER)
    ''')

conn.commit()
conn.close()
