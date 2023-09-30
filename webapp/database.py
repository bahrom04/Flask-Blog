from flask import render_template
import mysql.connector as mysql 


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
