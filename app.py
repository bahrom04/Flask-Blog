import sqlite3 as sql
from flask import Flask, render_template
from werkzeug.exceptions import abort


def get_connection_db():
    conn = sql.connect('database.db')
    conn.row_factory = sql.Row
    return conn

def get_post(post_id):
    conn = get_connection_db()
    post = conn.execute("SELECT * FROM posts WHERE id = ?",(post_id)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)


@app.route('/')
def index():
    conn = get_connection_db()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return render_template('index.html', posts=posts)



if __name__ == "__main__":
    app.run(debug=True)