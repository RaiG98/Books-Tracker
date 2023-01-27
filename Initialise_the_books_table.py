import sqlite3
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

def initialise_books_table():
    cursor.execute('''
        CREATE TABLE books (
        id INT(4) UNIQUE,
        Title varchar UNIQUE,
        Author varchar,
        QTY INT,
        PRIMARY KEY (id)
    );''')
    insert_into_books_table(3001, 'A Tale of Two Cities', 'Charles Dickens', 30)
    insert_into_books_table(3002, 'Harry Potter and the Philospher\'s Stone', 'J.K. Rowling', 40)
    insert_into_books_table(3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25)
    insert_into_books_table(3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37)
    insert_into_books_table(3005, 'Alice in Wonderland', 'Lewis Carroll', 12)


initialise_books_table()