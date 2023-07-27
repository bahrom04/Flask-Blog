import sqlite3

conn = sqlite3.connect('database.db')

with open('schema.sql') as f:
    conn.executescript(f.read())


cur = conn.cursor()

cur.execute("INSERT INTO posts (title,context) VALUES (?,?)",
            ('First post', 'Out of context first one')
            )

cur.execute("INSERT INTO posts (title,context) VALUES (?,?)",
            ('Second post', 'Out of context second one')
            )

conn.commit()
conn.close()