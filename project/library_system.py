import datetime
import xlsxwriter

class Library:
    def __init__(self, get_book_Title, get_book_Author, get_book_Isbn):
        self.get_book_Title = get_book_Title
        self.get_book_Author = get_book_Author
        self.get_book_Isbn = get_book_Isbn
        self.set_Transactions = []  # List to store each addition as a transaction
        self.get_Removed = False  # Flag to indicate if the book has been removed

    def set_Transaction(self, get_bookQuantity):
        # Record each addition as a transaction with a timestamp
        Transaction = {
            'quantity': get_bookQuantity,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.set_Transactions.append(Transaction)

    def mark_as_Removed(self):
        self.get_Removed = True

    def get_total_quantity(self):
        return sum(t['quantity'] for t in self.set_Transactions)

    def get_book_details(self):
        return {
            'title': self.get_book_Title,
            'author': self.get_book_Author,
            'isbn': self.get_book_Isbn,
            'quantity': self.get_total_quantity(),
            'status': "Book Removed" if self.get_Removed else "Books Available" if self.get_total_quantity() > 0 else "Books Unavailable"
        }


addBooks = []

# Helper function to get valid input
def get_input(prompt, cast_type=str, choices=None):
    while True:
        user_input = input(prompt).strip()
        if not user_input:  # If input is empty, silently re-prompt
            continue
        try:
            value = cast_type(user_input)  # Try to cast the input to the desired type
            if choices is not None and value not in choices:  # Check if value is in valid choices
                print(f"---> Invalid input, please try again.\n")
                continue
            return value
        except ValueError:  # If casting fails, print an error message and re-prompt
            print("---> Invalid input, please enter a valid value.\n")
            continue


# Helper function for Yes/No prompts
def get_yes_no_input(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ["yes", "no"]:
            return user_input
        print("---> Invalid input, please enter 'Yes' or 'No'.\n")


# Helper function to find a book by ISBN
def find_book_by_isbn(get_book_Isbn):
    return next((book for book in addBooks if book.get_book_Isbn == get_book_Isbn), None)


# Function to display book information
def display_bookInfo(book):
    book_details = book.get_book_details()
    print(f"{'[BOOK TITLE\t\t\t\t]':<15}\t\t\t{f'[{book_details['title']:<20}]'}\n"
          f"{'[BOOK AUTHOR\t\t\t]':<15}\t\t\t{f'[{book_details['author']:<20}]'}\n"
          f"{'[BOOK ISBN\t\t\t\t]':<15}\t\t\t{f'[{book_details['isbn']:<20}]'}\n"
          f"{'[BOOK QUANTITY\t\t\t]':<15}\t\t\t{f'[{book_details['quantity']:<20}]'}\n"
          f"{'[BOOK STATUS\t\t\t]':<15}\t\t\t{f'[{book_details['status']:<20}]'}\n")


# Function to add a book
def addBook():
    get_book_Isbn = get_input("- Enter book ISBN\t.\t.\t.\t.\t.\t: ")
    existing_book = find_book_by_isbn(get_book_Isbn)
    if existing_book:
        print(f"- Book author\t.\t.\t.\t.\t.\t: {existing_book.get_book_Author}")
        print(f"- Book title\t.\t.\t.\t.\t.\t: {existing_book.get_book_Title}")
        get_book_newQuantity = get_input("- Enter additional quantity\t.\t.\t.\t.\t.\t: ", int)
        existing_book.set_Transaction(get_book_newQuantity)  # Add a new transaction
        print("---> Book added to library successfully!\n")
    else:
        get_book_Title = get_input("- Enter book title\t.\t.\t.\t.\t.\t: ")
        get_book_Author = get_input("- Enter book author\t.\t.\t.\t.\t.\t: ")
        get_book_oldQuantity = get_input("- Enter book quantity\t.\t.\t.\t.\t.\t: ", int)
        get_new_addBook = Library(get_book_Title, get_book_Author, get_book_Isbn)
        get_new_addBook.set_Transaction(get_book_oldQuantity)  # Add the initial transaction
        addBooks.append(get_new_addBook)
        print("---> Book added to library successfully!\n")


# Function to check all books in the library
def checkLibrary():
    if not addBooks:
        print("\t\t\t   -------> NO BOOKS IN LIBRARY <-------\n")
        return

    print("- Books in the library: \n")
    for i, book in enumerate(addBooks, start=1):
        print(f"{i}. BOOK ISBN   ---------> {book.get_book_Isbn} <---------")
        display_bookInfo(book)


# Function to search for a book by ISBN
def searchBook():
    while True:
        get_book_Isbn = get_input("- Enter book ISBN to search\t.\t.\t.\t.\t.\t: ")
        if not get_book_Isbn:
            print("---> Invalid input, please try again.\n")
            continue
        book = find_book_by_isbn(get_book_Isbn)
        if book:
            print('')
            print(f"--->  BOOK ISBN --------> {book.get_book_Isbn} <--------")
            display_bookInfo(book)
            while True:
                user_input = get_input("---> Enter 1 to continue searching or 0 to exit: ")
                print(' ')
                if user_input in ["0", "1"]:
                    break
                print("---> Invalid input, please try again.\n")
            if user_input == "0":
                print('---> Exiting search.\n')
                break
        else:
            print("---> Book not found, please try again.\n")


# Function to update book information
def updateBook():
    while True:
        book_Isbn = get_input("- Enter book ISBN to update\t.\t.\t.\t.\t.\t: ")
        book = find_book_by_isbn(book_Isbn)
        if book:
            print("\n\t\t\t   ------> Input New Information <------")
            book.get_book_Isbn = get_input("- Enter new book ISBN\t.\t.\t.\t.\t.\t: ")
            book.get_book_Title = get_input("- Enter new book title\t.\t.\t.\t.\t.\t: ")
            book.get_book_Author = get_input("- Enter new book author\t.\t.\t.\t.\t.\t: ")
            print("---> Book updated successfully!\n")
            while True:
                user_input = get_input("---> Enter 1 to continue updating or 0 to exit: ")
                print(' ')
                if user_input in ["0", "1"]:
                    break
                print("---> Invalid input, please try again.\n")
            if user_input == "0":
                print('---> Exiting update.\n')
                break
        else:
            print("---> Book not found, please try again.\n")


# Function to remove a book
def removeBook():
    while True:
        book_Isbn = get_input("- Enter book ISBN to remove\t.\t.\t.\t.\t.\t: ")
        if not book_Isbn:
            print("---> Invalid input, please try again.\n")
            continue
        book = find_book_by_isbn(book_Isbn)
        if book:
            print(' ')
            remove_type = get_input("---> Type 'All' to remove all books or enter quantity\t\t: ").strip().lower()
            print(' ')
            if remove_type == 'all':
                confirm = get_yes_no_input("---> Are you sure you want to remove all books? (Yes/No)\t: ")
                if confirm == 'yes':
                    total_quantity = book.get_total_quantity()
                    book.set_Transaction(-total_quantity)  # Record the removal of all copies as a negative transaction
                    book.mark_as_Removed()
                    print("---> All copies of the book marked as removed successfully!\n")
                else:
                    print("---> Book removal canceled.\n")
            else:
                try:
                    remove_quantity = int(remove_type)
                    if remove_quantity > 0:
                        confirm = get_yes_no_input(
                            f"---> Are you sure you want to remove {remove_quantity} book('s)? (Yes/No)\t: ")
                        if confirm == 'yes':
                            book.set_Transaction(-remove_quantity)  # Record the removal as a negative transaction
                            print(f"---> {remove_quantity} copies of the book removed successfully!\n")
                        else:
                            print("---> Book removal canceled.\n")
                    else:
                        print("---> Invalid quantity, please try again.\n")
                except ValueError:
                    print("---> Invalid input, please enter a valid quantity or 'All'.\n")
            while True:
                user_input = get_input("---> Enter 1 to continue removing or 0 to exit\t.\t.\t.\t: ")
                print(' ')
                if user_input in ["0", "1"]:
                    break
                print("---> Invalid input, please try again.\n")
            if user_input == "0":
                print('---> Exiting removal.\n')
                break
        else:
            print("---> Book not found, please try again.\n")


# Function to export books to Excel
def export_to_excel():
    # Create a new Excel workbook and add a worksheet
    workbook = xlsxwriter.Workbook('LibraryBooks.xlsx')
    worksheet = workbook.add_worksheet('DATA ENTRY')

    # Write the headers
    headers = ['No', 'Purchase Date', 'ISBN', 'Title', 'Author', 'Book Quantity', 'Transaction']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Write the book details
    row_num = 1  # Start from row 1 (row 0 is headers)
    for book in addBooks:
        for transaction in book.set_Transactions:
            worksheet.write(row_num, 0, row_num)
            worksheet.write(row_num, 1, transaction['date'])
            worksheet.write(row_num, 2, book.get_book_Isbn)
            worksheet.write(row_num, 3, book.get_book_Title)
            worksheet.write(row_num, 4, book.get_book_Author)
            worksheet.write(row_num, 5, transaction['quantity'])
            worksheet.write(row_num, 6, 'Purchase In' if transaction['quantity'] > 0 else 'Removed')
            row_num += 1

    # Save and close the workbook
    workbook.close()
    print("---> Books exported to LibraryBooks.xlsx successfully!\n")


# Function to manage the library
def manageLibrary():
    while True:
        print(
            "===================================================== LIBRARY MANAGEMENT ====================================================")
        print(
            "\t1. ADD BOOK\t2. CHECK LIBRARY\t3. SEARCH BOOK\t4. UPDATE BOOK\t5. REMOVE BOOK\t6. EXPORT BOOKS\t7. EXIT")
        print(
            "======================================================== INSTRUCTION ========================================================")

        option = get_input("---> Choose Your Option\t.\t.\t.\t.\t.\t: ", int, choices=range(1, 8))
        print(" ")

        if option == 1:
            print("\t\t\t   ------------> ADD BOOKS <------------")
            num_books = get_input("- Enter number of books to add\t.\t.\t.\t.\t.\t: ", int)
            for i in range(num_books):
                print(f"\n\t\t\t   --------> Enter Book {i + 1} Data <--------")
                addBook()
        elif option == 2:
            print("\t\t\t   ------------ CHECK BOOKS <-----------")
            checkLibrary()
        elif option == 3:
            print("\t\t\t   ------------ SEARCH BOOK <-----------")
            searchBook()
        elif option == 4:
            print("\t\t\t   -----------> UPDATE BOOK <-----------")
            updateBook()
        elif option == 5:
            print("\t\t\t   -----------> REMOVE BOOK <-----------")
            removeBook()
        elif option == 6:
            print("\t\t\t   -----------> EXPORT BOOKS <----------")
            export_to_excel()
        else:
            print("Exiting Library Management...\n")
            break

        input("Press any key to continue...\n")