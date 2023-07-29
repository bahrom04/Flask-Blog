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
        return render_template('index.html')
    return post


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


# Showing all posts from data
@app.route('/index')
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


# New page to create posts
@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is strongly required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, context) VALUES (?, ?)',(title,content))
            conn.commit()
            conn.close()
            return redirect('index')

    return render_template('create.html')


# Edit page
@app.route('/<int:id>/edit>', methods=['GET','POST'])
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is strongly required')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, context = ?'
                         'WHERE id = ?', (title,content,id))
            conn.commit()
            conn.close()
            return redirect('index')

    return render_template('edit.html', post=post)

# Deleting posts
@app.route('/<int:id>/delete', methods=['POST',])
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('{} deleted succesfully'.format(post['title']))
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)