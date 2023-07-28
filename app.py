import sqlite3 as sql
from flask import Flask, render_template, redirect, request, url_for, flash
from werkzeug.exceptions import abort

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bahromoken@githubbahrombek'


# Creating connection with db
def get_db_connection():
    conn = sql.connect('database.db')
    conn.row_factory = sql.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

# Editing posts
def edit():
    pass


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


# Showing all posts from data
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET','POST'])
def create():
    return render_template('create.html')

if __name__ == "__main__":
    app.run(debug=True)