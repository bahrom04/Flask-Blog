from webapp import app
from flask import render_template, flash, redirect, url_for, request, session
import os
from webapp.forms import RegistrationForm, LoginForm
from webapp import db
from webapp.models import Accounts
from webapp.database import get_mysql_connection, get_post

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


# About Page
@app.route('/about')
def about():
    return render_template('about.html')


# Post by id
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)
    



# New page to register
@app.route('/')
@app.route('/register', methods=['GET','POST'])
def register():
    # resister class from forms.py
    form = RegistrationForm()
    if form.validate_on_submit():
        
        user_create = Accounts(username=form.username.data,
                               password_decode=form.password1.data)
        db.session.add(user_create)
        db.session.commit()
        return redirect(url_for('index'))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'There was an error with creating a user: {error}')
        
    return render_template('register.html', form=form)



# Login page auth
@app.route('/login', methods=['GET','POST'])
def login():
    # Login class
    form = LoginForm()
    return render_template('login.html', form=form)


     
# Logout page
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for('login'))


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
    # flash('{} deleted succesfully'.format(post['title']))
    with get_mysql_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM posts WHERE id = %s', (id,))
        conn.commit()
    return redirect(url_for('index'))
