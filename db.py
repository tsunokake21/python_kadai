import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits

    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password

def insert_user(user_name, password):
    sql = 'INSERT INTO user_sample VALUES(default, %s, %s, %s)'

    salt = get_salt()
    hashed_password = get_hash(password, salt)

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name, hashed_password, salt))
        count = cursor.rowcount 
        connection.commit()

    except psycopg2.DatabaseError :
        count = 0

    finally :
        cursor.close()
        connection.close()

    return count

def login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM user_sample WHERE name = %s'
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name,))
        user = cursor.fetchone()

        if user != None:
            
            salt = user[1]

           
            hashed_password = get_hash(password, salt)

          
            if hashed_password == user[0]:
                flg = True

    except psycopg2.DatabaseError :
        flg = False

    finally :
        cursor.close()
        connection.close()

    return flg


def select_all_book(title, author, pages):
    connetiion = get_connection()
    cursor =connetiion.cursor()
    sql = 'INSERT INTO book_sample VALUES (default, %s, %s, %s)'
    
    cursor.execute(sql, (title, author, pages ))
    
    connetiion.commit()
    cursor.close()
    connetiion.close()


def insert_book(title, author, pages):
    connetiion = get_connection()
    cursor =connetiion.cursor()
    sql = 'INSERT INTO book_sample VALUES (default, %s, %s, %s)'
    
    cursor.execute(sql, (title, author, pages ))
    
    connetiion.commit()
    cursor.close()
    connetiion.close()
    

def dele_book(title):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "delete from book_sample where title=%s"

    cursor.execute(sql, (title,))
    connection.commit()

    cursor.close()
    connection.close()
    
    
def lis_boo():
    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT title, author, pages FROM book_sample"

    cursor.execute(sql)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def book_search(title):
    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT * FROM book_sample WHERE title LIKE %s"

    titles = "%" + title + "%"

    cursor.execute(sql, (title,))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows
    
    
    