import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="blog"
)

cursor = db.cursor()

def create_table():
    cursor.execute("""CREATE TABLE posts(
                   id INT AUTO_INCREMENT PRIMARY KEY, 
                   title VARCHAR(255) NOT NULL,
                   context VARCHAR(255) NOT NULL, 
                   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
                   photo VARCHAR(255) NOT NULL)""")


#Changing data type of photo
#cursor.execute("ALTER TABLE posts MODIFY photo VARCHAR(255)")

# cursor.execute("INSERT INTO posts (title, context) VALUES (%s, %s)", ('Mysql_4', 'Out of context 4 one'))
# db.commit()


# cursor.execute("SELECT * FROM posts")



def get_post(post_id):
    conn = db
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts WHERE id = %s',
                        (post_id,))
    post = cur.fetchone()

    conn.close()
    return post



print(get_post(5))



