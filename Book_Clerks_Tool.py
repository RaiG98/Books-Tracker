import sqlite3
from tabulate import tabulate
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

# This class will allow the programme to print coloured text to the screen.
# Logan Meadows mentioned this method on one of the lectures and shared it with the following link from a stackoverflow post:
# https://stackoverflow.com/questions/37384024/how-to-add-colour-to-a-specific-word-in-a-string
class Colour:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# This function will take in a list of tuples and print them out to screen in an easy to read format.
def tabulate_table_rows(lst):
    table = [['id', 'Title', 'Author', 'QTY']]
    for i in lst:
        table.append([i[0], i[1], i[2], i[3]])
    return tabulate(table,headers='firstrow')

# This function will add row to the books table.
def insert_into_books_table(title, author, qty):
    # Finding the last id value in the table
    cursor.execute('''
        SELECT id FROM books;
    ''')
    id = cursor.fetchall()[-1][0]
    cursor.execute('''
        INSERT INTO books
        VALUES (?, ?, ?, ?);
    ''', ((id + 1), title, author, qty))

# This will delete a specified row in the books table
def delete_a_book(id=None, title=None):
    if id != None:
        cursor.execute('''
        DELETE FROM books
        WHERE id = ?;
        ''', (id,))
    elif title != None:
        cursor.execute('''
        DELETE FROM books
        WHERE title = ?;
        ''', (title,))

# This will update the specified rows value in the books table to the value of the parameter 'to'.
def update_a_book(change, to, id_parameter):
    id_parameter = id_parameter[0]
    sql_string = f'''
        UPDATE books
        SET {change}='{to}'
        WHERE id={id_parameter};
        '''
    cursor.execute(sql_string)

# This will find the row or rows with the specified value entered. Only one of the parameters(id/TItle/Author) is need.
def find_book(id=None, title=None, author=None):
    if id != None:
        cursor.execute('''
        SELECT * FROM books
        WHERE id=?;
        ''', (id,))
    elif title != None:
        cursor.execute('''
        SELECT * FROM books
        WHERE Title=?;
        ''', (title,))
    elif author != None:
        cursor.execute('''
        SELECT * FROM books
        WHERE Author=?;
        ''', (author,))
    book = cursor.fetchall()
    return book

# If this function is called, the table will be intialised with all the proper columns.
def initialise_books_table():
    cursor.execute('''
        CREATE TABLE books (
        id INT(4) UNIQUE,
        Title varchar UNIQUE,
        Author varchar,
        QTY INT,
        PRIMARY KEY (id)
    );''')

# This function will print out all of the rows in the books table in an easy to read format.
def print_table():
    cursor.execute('''
        SELECT * FROM books;
    ''')
    print(tabulate_table_rows(cursor.fetchall()))




# This loop will provide the user with a menu from which they will be able to perform various actions on the books table.
while True:
    menu_choice = input("""\nPlease choose one of the menu options below:
a - Add a new book
u - Update a books information
d - Delete a book
s - Search for a book
p - Print books table
e - exit the program  & commit changes\n:""").lower().strip(" ")
    print()
    back_to_main_menu = False
    # This section will run if the user wants to add a book to the table. It will check the values entered by the user and catch user errors.
    # Before adding the book to the system, the programme will print the user entered values to screen and ask the user if they are sure they would like to add that row to the table.
    if menu_choice == 'a':
        while True:
            new_title = input("Enter the title of the book you would like added to the database: ").strip(" ")
            new_author = input("Enter the name of the author who wrote the book: ")
            while True:
                try:
                    new_qty = int(input("Enter the quantity that will be stocked: "))
                except:
                    print("\n" + Colour.RED + "Error. It seems you have not entered a whole number. Try again: \n" + Colour.END)
                else:
                    break
            while True:
                y_n = input(f"\nYou would like to add {new_qty} of {new_title} by {new_author}. Is this correct?\nEnter 'y' for yes, 'n' to re-enter the books details and 'e' to cancel\n:")
                if y_n.lower().strip() == 'y':
                    break_yn = True
                    break
                elif y_n.lower().strip() == 'n':
                    break_yn = False
                    break
                elif y_n.lower().strip() == 'e':
                    break_yn = True
                    back_to_main_menu = True
                    break
                else:
                    print(Colour.RED + "\nError. Please either enter 'y', 'n' or 'e'\n" + Colour.END)
            if break_yn:
                break
            else:
                continue
        if back_to_main_menu:
            continue
        insert_into_books_table(new_title, new_author, new_qty)
        print("\nThe book has been added to the system.")
    
    # This will allow the user to edit a rows values. It will first find the row wither by its id or title, once the the row has been found it will check with the user if it is the row they would like to edit.
    # If the user would like to edit the row, the programme asks the user to specify which value they would like to edit. 
    elif menu_choice == 'u':
        title_or_id = input("Enter 'id' or 'title' to update a book by its id or by its title: ").lower().strip()
        if title_or_id == 'id':
            try:
                entered_id = int(input("Enter the id of the book you would like to update in the database: "))
                to_update = find_book(id=entered_id)
            except:
                print(Colour.RED + "Error. you must enter a whole value. Try again." + Colour.END)
                continue
        elif title_or_id == 'title':
            entered_title = input("Enter the title of the book you would like to update in the database: ")
            to_update = find_book(title=entered_title)
        else:
            print("\nIt seems you have not entered one of the options given, you will be redirected to the main menu.")
            continue
        if len(to_update) == 0:
            print("\nError. The programme could not find a book corresponding to that id/title in the database.")
            continue
        print("\nIs this the book you would like to update?")
        print(tabulate_table_rows(to_update))
        user_y_n = input("\nEnter 'y' if you would like to update the book. ").lower().strip()
        # If the user is happy with editing the selected row, the following code will execute:
        if user_y_n == 'y':
            # The next set of booleans will decide which value in the row should be edited.
            value_to_be_updated = input("Enter 'id' to update id, 'title' to update title, 'author' to update author and 'qty' to update QTY: ").lower().strip(" ")
            if value_to_be_updated == 'id':
                # If the user enters anything other than an integer or an error occurs, the user will be given another chance to enter a valid value.
                while True:
                    try:
                        new_value = int(input("Enter the value you would like to change the id to, it must be a whole number and it must not be a repeat of another books id: "))
                        update_a_book(value_to_be_updated, new_value, id_parameter=to_update[0])
                        print(f"\nThe books {value_to_be_updated} has successfully been updated to {new_value}")
                        break
                    except:
                        print(Colour.RED + "\nError. It seems there has been a mistake somewhere. Try again\n" + Colour.END)
                        continue
            elif value_to_be_updated == 'title':
                new_value = input("Enter the value you would like to change the title to: ")
                update_a_book(value_to_be_updated.capitalize(), new_value, id_parameter=to_update[0])
                print(f"\nThe books {value_to_be_updated} has successfully been updated to {new_value}")
            elif value_to_be_updated == 'author':
                new_value = input("Enter the value you would like to change the author to: ")
                update_a_book(value_to_be_updated.capitalize(), new_value, id_parameter=to_update[0])
                print(f"\nThe books {value_to_be_updated} has successfully been updated to {new_value}")
            # If the user enters anything other than an integer or an error occurs, the user will be given another chance to enter a valid value.
            elif value_to_be_updated == 'qty':
                while True:
                    try:
                        new_value = int(input("Enter the value you would like to change the qty to, it must be a whole number: "))
                        update_a_book(value_to_be_updated.upper(), new_value, id_parameter=to_update[0])
                        print(f"The books {value_to_be_updated} has successfully been updated to {new_value}")
                        break
                    except:
                        print(Colour.RED + "\nError. It seems there has been a mistake somewhere. Try again\n" + Colour.END)
                        continue
            else:
                print(Colour.RED + "\nUpdate canelled. The book has not been updated" + Colour.END)
                continue
        else:
            print(Colour.RED + "\nUpdate canelled. The book has not been updated" + Colour.END)
            continue
        
    # This block will find a row based off of the users input then print it to screen to check if it is indeed the book the user would like deleted. 
    # If the user enters 'y' the row will be deleted.
    elif menu_choice == 'd':
        title_or_id = input("Enter 'id' or 'title' to delete a book by its id or by its title: ").lower().strip()
        if title_or_id == 'id':
            entered_id = input("Enter the id of the book you would like to delete from the database: ")
            to_delete = find_book(id=entered_id)
        elif title_or_id == 'title':
            entered_title = input("Enter the title of the book you would like to delete from the database: ")
            to_delete = find_book(title=entered_title)
        if len(to_delete) == 0:
            print("\nError. It seems we could not find a book corresponding to that id/title")
            continue
        print("\nIs this the book you would like to delete from the database?")
        print(tabulate_table_rows(to_delete))
        user_y_n = input("\nEnter 'y' if you would like to delete the book. ").lower().strip()
        if user_y_n == 'y':
            if title_or_id == 'id':
                delete_a_book(id=entered_id)
            elif title_or_id == 'title':
                delete_a_book(title=entered_title)
        else:
            print(Colour.RED + "\nThe book has not been deleted" + Colour.END)
            continue
        print("\nThe book has been deleted from the database successfully")
    
    # The user will be able to search for a book by its id, title or author. Once the book or books have been found, it will be printed to the screen. 
    # If no book is found, an appropriate message will be printed to the screen.
    elif menu_choice == 's':
        detail_choice = input("If you would like to search for the book by id enter'id', to search by 'title' enter 'title' and to search by author, enter 'author': ")
        if detail_choice.lower().strip(" ") == 'id':
            find = input("Enter the 4 digit id of the book: ")
            result = find_book(id=find)
            if len(result) == 0:
                print(f"\nThere is no book with an id of {find} in our database")
                continue
        elif detail_choice.lower().strip(" ") == 'title':
            find = input("Enter the title of the book: ")
            result = find_book(title=find)
            if len(result) == 0:
                print(f"\nWe do not have any books with a title of {find} in our database")
                continue
        elif detail_choice.lower().strip(" ") == 'author':
            find = input("Enter the author of the book: ")
            result = find_book(author=find)
            if len(result) == 0:
                print(f"\nWe do not have any book by {find} in our database")
                continue
        else:
            print(Colour.RED + "\nError. It seems you did not enter one of the options given. You will be redirected to the main menu." + Colour.END)
            continue
        print('\nThe result of the search:\n')
        print(tabulate_table_rows(result))
    
    # The book table rows will be printed to screen in an easy to read format.
    elif menu_choice == 'p':
        print_table()
    
    # This ensures that when the user leaves the programme, all the changes will be saved
    elif menu_choice == 'e':
        db.commit()
        break
    
    else:
        print("It seems you have not entered one of the choices given. Try again.")