import sqlite3
from tabulate import tabulate


# Search an id in table books
def id_searching(id_no):
    id_list = cursor.execute('''SELECT id FROM books''').fetchall()
    id_search = [row for row in id_list if id_no == row[0]]
    return id_search


try:
    # Creates or open a database called ebookstore_db with SQLite3 DB
    db = sqlite3.connect('ebookstore_db')
    cursor = db.cursor()

    # Check if table books does not exist and create it
    cursor.execute('''CREATE TABLE IF NOT EXISTS
            books(id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER )''')
    db.commit()

    # inserting data. If data's already inserted, it'll be ignored.
    books_list = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                  (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                  (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
                  (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
                  (3005, "Alice in Wonderland", "Lewis Carroll", 12),
                  (3006, "The Adventures of Sherlock Holmes", "Arthur Conan Doyle", 35),
                  (3007, "Around the World in Eighty Days", "Jules Verne", 26)]

    cursor.executemany('''INSERT OR IGNORE INTO books (id, title, author, qty)
                      VALUES(?, ?, ?, ?)''', books_list)

    db.commit()

except Exception as e:
    raise e


db = sqlite3.connect('ebookstore_db')
cursor = db.cursor()

# it keeps asking user make a selection with while loop

while True:

    menu = input('''Please Select one of the options below: 
1. Enter book
2. Update book
3. Delete book
4. Search books
5. Display Book list
0. Exit
''')
    # Enter new book
    if menu == '1':

        try:
            id_duplicate = True
            id_no = int(input('Please enter id number of the book:'))

            # it checks if id already exists with id_searching function.It requests id till gets new id with while loop.
            while id_duplicate:
                id_searching(id_no)
                if len(id_searching(id_no)) != 0:
                    id_no = int(input('id already exists! Please enter new id:'))
                    id_duplicate = True
                else:
                    id_duplicate = False

            title = input('Please enter title of the book:')
            author = input('Please enter author of the book:').title()
            qty = int(input('Please enter quantity of the book:'))

            # Insert new book into table books
            cursor.execute('''INSERT INTO books (id, title, author, qty)
                               VALUES(?, ?, ?, ?)''', (id_no, title, author, qty))
            db.commit()

        except ValueError:
            print('You have entered an invalid number, please try again...\n')

    # Update table books
    elif menu == '2':
        update_menu = input('''Please select one of the options below to update:
        i  -  update id
        t  -  update title
        a  -  update author
        q  -  update quantity ''').lower()

        try:
            # Update id of the book
            if update_menu == 'i':

                id_no = int(input('Please enter existing id of the book'))
                id_update = int(input('Please enter new id of the book to update'))

                # Search existing id in table books
                id_searching(id_no)

                # Search new id in table books if it already exists or not
                id_searching(id_update)

                # If id is not in the table:
                if len(id_searching(id_no)) == 0:
                    print('You have entered an invalid id to update! Please try again...\n')

                # If id is in the table and new id is not in the table, it'll update id in the table.
                elif len(id_searching(id_no)) == 1 and len(id_searching(id_update)) == 0:
                    cursor.execute('''UPDATE books SET id = ?
                                    WHERE id =?''', (id_update, id_no))
                    db.commit()

                # If new id already exists
                elif len(id_searching(id_update)) == 1:
                    print('New id already exists. Please try again...\n')

                else:
                    print('You have entered invalid id! Please try again...')

            # Update title of the book
            elif update_menu == 't':

                id_no = int(input('Please enter id of the book you would like to update:'))
                id_searching(id_no)

                # If entered id already exists, it'll update title of the books with entered id.
                if len(id_searching(id_no)) != 0:
                    title_update = input('Please enter new title of the book to update')
                    cursor.execute('''UPDATE books SET title = ?
                                    WHERE id =?''', (title_update, id_no))
                    db.commit()
                else:
                    print('You have entered an invalid id to update! Please try again...\n')

            # Update author of the book
            elif update_menu == 'a':

                id_no = int(input('Please enter id of the book would you like to update:'))
                id_searching(id_no)

                # If entered id already exists, it'll update author of the books with entered id.
                if len(id_searching(id_no)) != 0:
                    author_update = input('Please enter new author of the book to update').title()
                    cursor.execute('''UPDATE books SET author = ?
                                    WHERE id =?''', (author_update, id_no))
                    db.commit()
                else:
                    print('You have entered an invalid id to update! Please try again...\n')

            # Update quantity of the book
            elif update_menu == 'q':

                id_no = int(input('Please enter id of the book would you like to update:'))
                id_searching(id_no)

                # If entered id already exists, it'll update quantity of the books with entered id.
                if len(id_searching(id_no)) != 0:
                    try:
                        qty_update = int(input('Please enter new quantity of the book to update'))
                        cursor.execute('''UPDATE books SET qty = ?
                                        WHERE id =?''', (qty_update, id_no))
                        db.commit()
                    except ValueError:
                        print('You entered an invalid quantity! Please try again...\n')
                else:
                    print('You have entered an invalid id to update! Please try again...\n')

            else:
                print('You have entered an invalid option. Please try again...\n')

        except ValueError:
            print('You have entered an invalid id! Please try again...\n')

    # Delete a book from table books
    elif menu == '3':

        try:
            id_no = int(input('Please enter id of the book would you like to delete'))
            id_searching(id_no)

            # If entered id already exists, it'll delete the books with entered id.
            if len(id_searching(id_no)) != 0:
                cursor.execute('''DELETE FROM books
                                    WHERE id =?''', (id_no,))
                db.commit()
            else:
                print('The id you have entered does not exist!\n')

        except ValueError:
            print('You have entered an invalid id! Please try again...\n')

    # Search books from database
    elif menu == '4':

        search_menu = input('''Please select one of the options below to search book:
        i  -  search with id
        t  -  search with title
        a  -  search with author''').lower()

        # Search a book with id
        if search_menu == 'i':

            try:
                id_no = int(input('Please enter id of the book to search:'))
                id_searching(id_no)

                # If entered id already exists, it'll display data about the books with entered id.
                if len(id_searching(id_no)) != 0:
                    cursor.execute('''SELECT id, title, author, qty FROM books
                                        WHERE id=?''', (id_no,))

                    headers = ['ID', 'Title', 'Author', 'Quantity']
                    print(tabulate(cursor, headers, tablefmt='grid'))
                else:
                    print('The id you have entered does not exist!\n')

            except ValueError:
                print('You have entered an invalid id! Please try again...\n')

        # Search a book with title
        elif search_menu == 't':

            title = input('Please enter title of the book to search:').lower()

            # Check if entered title already exists
            title_list = cursor.execute('''SELECT title FROM books''').fetchall()
            title_search = [row for row in title_list if title == row[0].lower()]

            # If title already exists in the database, it'll display data about title entered.
            if len(title_search) != 0:
                cursor.execute('''SELECT id, title, author, qty FROM books
                                 WHERE lower(title)=? ''', (title,))

                headers = ['ID', 'Title', 'Author', 'Quantity']
                print(tabulate(cursor, headers, tablefmt='grid'))
            else:
                print('The title you have entered does not exist!\n')

        # Search a book with author
        elif search_menu == 'a':

            author = input('Please enter author of the book to search:').lower()

            # Check if entered author already exists
            author_list = cursor.execute('''SELECT author FROM books''').fetchall()
            author_search = [row for row in author_list if author == row[0].lower()]

            # If author already exists in the database, it'll display data about author entered.
            if len(author_search) != 0:
                cursor.execute('''SELECT id, title, author, qty FROM books
                                WHERE lower(author)=?''', (author,))

                headers = ['ID', 'Title', 'Author', 'Quantity']
                print(tabulate(cursor, headers, tablefmt='grid'))
            else:
                print('The author you have entered does not exist!\n')

        else:
            print('You have entered an invalid option! Please try again...\n')

    # Display all data with a table
    elif menu == '5':
        cursor.execute('''SELECT id, title, author, qty FROM BOOKS''')
        headers = ['ID', 'Title', 'Author', 'Quantity']
        print(tabulate(cursor, headers, tablefmt='grid'))

    elif menu == '0':
        break

    else:
        print('You have entered an invalid option! Please try again...\n')
