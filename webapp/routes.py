from webapp import app
from flask import render_template, flash, redirect, url_for, request, session
import os
import mysql.connector as mysql
from webapp.forms import RegistrationForm

# Mysql connection.l
def get_mysql_connection():
    mysql_connection = mysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="blog"
    )
    return mysql_connection
    

def get_post(post_id):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts WHERE id = %s',
                        (post_id,))
    post = cur.fetchone()

    conn.close()
    if cur is None:
        return render_template('index.html')
    return post

# Showing 404 error
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Showing all posts from data
@app.route('/index')
def index():
    # mysql part
    connect = get_mysql_connection()
    cur = connect.cursor()
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    posts.reverse()
    connect.close()
    return render_template('index.html', posts=posts)



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)
    

@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        conn = get_mysql_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        user = cur.fetchone()

        if user:
            session['logged_in'] = True
            session['username'] = user[1]
            session['id'] = user[0]
            flash('Logged in as ' + user[1])
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        pass




# New page to create posts
@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        photo = request.files['photo']



        if not title:
            flash('Title is strongly required')
        

        if photo is None:
            conn = get_mysql_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO posts (title, context) VALUES (%s, %s)',(title,content))
            conn.commit()
            conn.close()
            return redirect('index')
        else:
            
            filename = f'post_.{photo.filename}'
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash('Post added successfully', 'success')
            conn = get_mysql_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO posts (title, context, photo) VALUES (%s, %s, %s)',(title,content,filename))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
                

    return render_template('create.html')


# Edit page
@app.route('/<int:id>/edit>', methods=['GET','POST'])
def edit(id):
    post = get_post(id)
    conn = get_mysql_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        photo = request.files['photo']

        if not title:
            flash('Title is strongly required')
        else:
            if photo:

                filename = f'post_.{photo.filename}'
                uploads_folder_path = os.path.join('static', 'uploads')
                uploads_folder_path_files = os.listdir(uploads_folder_path)
                for file in uploads_folder_path_files:
                    if file == filename:
                        cur.execute('UPDATE posts SET photo = %s WHERE id = %s',(filename,id))
                        conn.commit()
                        
        
                else:
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cur.execute('UPDATE posts SET photo = %s WHERE id = %s',(filename,id))

            cur.execute('UPDATE posts SET title = %s, context = %s'
                         'WHERE id = %s', (title,content,id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)



# Deleting posts
@app.route('/<int:id>/delete', methods=['POST','GET'])
def delete(id):
    post = get_post(id)
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM posts WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    # flash('{} deleted succesfully'.format(post['title']))
    return redirect(url_for('index'))
