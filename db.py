import os
import psycopg

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg.connect(url)
    return connection

def select_all_books():
    connection = get_connection()
    cursor = connection.cursor()

    sql = 'SELECT title, author, publisher, pages FROM books_sample'

    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows

def insert_book(title,author,publisher,pages):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'INSERT INTO books_sample VALUES (default,%s,%s,%s,%s)'
    
    cursor.execute(sql,(title,author,publisher,pages))
    
    connection.commit()
    cursor.close()
    connection.close()