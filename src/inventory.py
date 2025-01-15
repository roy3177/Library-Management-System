import csv
import datetime
from book import Book
from book_factory import BookFactory
from update_files import UpdateFiles
from subject import Subject
from utils import get_csv_path


"""
@author Roy Meoded
@author Noa Agassi
system, responsible for managing the book inventory dynamically. Its purpose is to allow critical operations on books, such as updating, adding, deleting, and lending books, along with managing relevant files for persistent data storage.

Responsibilities of the File:
Loading Books: Reads data from books.csv to load existing books into memory.
Adding Books: Allows adding new books to the system and updates the CSV files accordingly.
Removing Books: Deletes books from the inventory and updates the files.
Lending Books: Reduces the available copies of books upon lending.
Returning Books: Adds copies back to the inventory upon return.
Managing Waitlists: Adds users to the waitlist for books that are unavailable.
Synchronizing Data: Saves book data, loaned books, and waitlists to CSV files to ensure data is preserved after system shutdown.
Displaying Books: Enables the display of all books currently in the system.
The file employs advanced techniques like loading data into Pandas DataFrames, handling CSV files, and managing Book and User objects.
"""



class BookIterator:
    def __init__(self, books):
        self._books = books
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._books):
            book = self._books[self._index]
            self._index += 1
            return book
        else:
            raise StopIteration()


class Inventory(Subject):
    def __init__(self):
        """
        Initialize the Inventory class to manage a collection of books.
        """
        super().__init__()  #Initialize subject's observers list.
        self.books=UpdateFiles.load_books()  # A list to store Book objects
        self.waitlist={} #Dictionary to manage waitlist
        self.notifications=[] #Notifications list
        self.load_waitlist_from_file()
        self.returned_last_user=None

    def check_book_exists(func):
        """
        Decorator to check if a book exists in the inventory before performing an action.
        """

        def wrapper(self, title, *args, **kwargs):
            # Check if the book exists in the inventory
            book = next((b for b in self.books if b.title.lower() == title.lower()), None)
            if not book:
                # Log and raise an exception if the book is not found
                self.log_action(func.__name__, success=False, details=f"Book '{title}' not found in inventory.")
                raise ValueError(f"Book '{title}' not found in inventory.")
            return func(self, title, *args, **kwargs)

        return wrapper

    def handle_exceptions(func):
        """
        Decorator to handle exceptions in a method.
        """

        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                # Log the exception and print an error message
                self.log_action(func.__name__, success=False, details=f"Error: {e}")
                print(f"An error occurred in {func.__name__}: {e}")

        return wrapper


    def __iter__(self):
        return BookIterator(self.books)

    def add_book(self, book):
        """
        Add a new book to the inventory.
        """
        try:
            if not isinstance(book, Book):
                raise ValueError("Invalid book object. Must be an instance of 'Book'.")

            # Add the book to the inventory
            self.books.append(book)
            UpdateFiles.update_books_file(book)

            # Update available_books.csv
            with open(get_csv_path("available_books.csv"), mode="a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Title", "Available"])
                writer.writerow({"Title": book.title, "Available": book.copies})
    
            # Log the action
            self.log_action("Add Book", success=True, details=f"Book '{book.title}' added successfully.")
            print(f"Book '{book.title}' added successfully.")

            # Notify observers
            self.notify()

        except Exception as e:
            self.log_action("Add Book", success=False, details=f"Error: {e}")
            print(f"Error adding book: {e}")

    @handle_exceptions
    @check_book_exists
    def remove_book(self, title):
        """
        Remove a book from the inventory by title and update all relevant files.
        Logs the action and raises a ValueError if the book is not found.
        """
        try:
            book_to_remove = next((book for book in self.books if book.title.lower() == title.lower()), None)

            if not book_to_remove:
                self.log_action("Remove Book", success=False, details=f"Book '{title}' not found in inventory.")
                raise RuntimeError(f"Book '{title}' not found in inventory.")

            self.books.remove(book_to_remove)

            self.sync_to_files()

            self.log_action("Remove Book", success=True, details=f"Book '{title}' removed successfully.")
            print(f"Book '{title}' removed successfully.")
            return True

        except Exception as e:
            self.log_action("Remove Book", success=False, details=f"Error removing book '{title}': {e}")
            print(f"Error removing book '{title}': {e}")

    def remove_book(self, title):
        """
        Remove a book from the inventory by title and update all relevant files.
        Logs the action and raises a ValueError if the book is not found.
        """
        try:
            book_to_remove = next((book for book in self.books if book.title.lower() == title.lower()), None)

            if not book_to_remove:
                self.log_action("Remove Book", success=False, details=f"Book '{title}' not found in inventory.")
                raise ValueError(f"Book '{title}' not found in inventory.")
                return False

            self.books.remove(book_to_remove)

            with open(get_csv_path("books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                books_rows = [row for row in reader if row["title"].lower() != title.lower()]

            with open(get_csv_path("books.csv"), mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["title", "author", "is_loaned", "copies", "genre", "year"])
                writer.writeheader()
                writer.writerows(books_rows)
            with open(get_csv_path("available_books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                available_rows = [row for row in reader if row["Title"].lower() != title.lower()]

            with open(get_csv_path("available_books.csv"), mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Title", "Available"])
                writer.writeheader()
                writer.writerows(available_rows)

            with open(get_csv_path("loaned_books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                loaned_rows = [row for row in reader if row["Title"].lower() != title.lower()]

            with open(get_csv_path("loaned_books.csv"), mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Title"])
                writer.writeheader()
                writer.writerows(loaned_rows)

            self.log_action("Remove Book", success=True, details=f"Book '{title}' removed successfully.")
            print(f"Book '{title}' removed successfully.")
            return True

        except Exception as e:
            self.log_action("Remove Book", success=False, details=f"Error removing book '{title}': {e}")
            print(f"Error removing book '{title}': {e}")

    def remove_from_csv(self, file_path, title):
        """
        Remove rows related to a specific book title from a CSV file.
        """
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                rows = [row for row in reader if row["Title"].lower() != title.lower()]

            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Title", "Available"] if "available_books" in file_path else [
                    "Title"])
                writer.writeheader()
                writer.writerows(rows)

        except Exception as e:
            print(f"ERROR: Failed to remove '{title}' from {file_path}: {e}")

    def update_book(self, title, **kwargs):
        """
        Update details of an existing book with enhanced logging.
        """
        try:
            book_to_update = next((book for book in self.books if book.title.lower() == title.lower()), None)
            if book_to_update:
                for key, value in kwargs.items():
                    if hasattr(book_to_update, key):
                        setattr(book_to_update, key, value)

                self.sync_to_files()

                self.log_action(
                    "Update Book",
                    success=True,
                    details=f"Book '{title}' updated successfully with changes: {kwargs}."
                )
                print(f"Book '{title}' updated successfully.")
            else:
                self.log_action(
                    "Update Book",
                    success=False,
                    details=f"Book '{title}' not found in inventory."
                )
                print(f"Book '{title}' not found in the inventory.")
        except Exception as e:
            self.log_action(
                "Update Book",
                success=False,
                details=f"Error updating book '{title}': {e}"
            )
            print(f"Error updating book '{title}': {e}")

    def update_available_books_csv(self, title, available_copies, found_in_available=False):
        """
        Update available_books.csv with the new availability.
        """
        try:
            with open(get_csv_path("available_books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            with open(get_csv_path("available_books.csv"), mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Title", "Available"])
                writer.writeheader()
                updated = False
                for row in rows:
                    if row["Title"].lower() == title.lower():
                        row["Available"] = str(available_copies)
                        updated = True
                    writer.writerow(row)

                if not updated and available_copies > 0:
                    writer.writerow({"Title": title, "Available": available_copies})

        except Exception as e:
            print(f"ERROR: Failed to update available_books.csv for '{title}': {e}")

    def display_books(self):
        """
        Display all books in the inventory and log the action.
        """
        try:
            if not self.books:
                self.log_action("Display Books", success=False, details="No books found in the inventory.")
                print("No books in the inventory.")
            else:
                self.log_action("Display Books", success=True, details=f"Displaying {len(self.books)} books.")
                print("Books in the inventory:")
                for book in self:
                    print(book)
        except Exception as e:
            self.log_action("Display Books", success=False, details=f"Error displaying books: {e}")
            print(f"Error displaying books: {e}")

    def search_books(self, **kwargs):
        """
        Search for books based on criteria provided in kwargs.
        Supports searching by title, author, or category.
        Logs the search action with success or failure details.
        Returns a list of matching books or an empty list if no matches are found.
        """
        try:
            available_books = {}
            with open(get_csv_path("available_books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row.get("Title", "Unknown Title")
                    available = row.get("Available", "0")
                    available_books[title] = int(available) if available.isdigit() else 0


            results = [
                book for book in self.books
                if all(str(getattr(book, key, "")).lower() == str(value).lower() for key, value in kwargs.items())
            ]

            if not results:
                self.log_action(
                    "Search Books",
                    success=False,
                    details=f"No books found matching criteria: {kwargs}"
                )
                return []

            for book in results:
                print(f"The book: {book.title}, author: {book.author}, category: {book.category}, "
                      f"year: ({book.year}), available copies: {available_books.get(book.title, 0)}/{book.copies}")

            self.log_action(
                "Search Books",
                success=True,
                details=f"Found {len(results)} books matching criteria: {kwargs}"
            )
            return results

        except FileNotFoundError:
            self.log_action(
                "Search Books",
                success=False,
                details="Error: available_books.csv file not found."
            )
            print("Error: available_books.csv file not found.")
            return []
        except Exception as e:
            self.log_action(
                "Search Books",
                success=False,
                details=f"Error during search: {e}"
            )
            print(f"Error during search: {e}")
            return []

    @handle_exceptions
    @check_book_exists
    def lend_book(self, title, username, email=None, phone=None):
        """
        Lend a book from the inventory. If unavailable, add the user to the waitlist.
        """

        book_to_lend = next((book for book in self.books if book.title.lower() == title.lower()), None)
        if not book_to_lend:
            print(f"ERROR: Book '{title}' not found in inventory.")
            self.log_action("Lend Book", success=False, details=f"Book '{title}' not found.")
            return False

        available_copies = 0
        try:
            with open(get_csv_path("available_books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Title"].lower() == title.lower():
                        available_copies = int(row["Available"])
                        break
        except FileNotFoundError:
            print("WARNING: available_books.csv not found. Assuming 0 available copies.")
        except Exception as e:
            print(f"ERROR: Failed to read available_books.csv: {e}")
            return False

        if available_copies > 0:
            book_to_lend.lend()
            available_copies -= 1

            self.update_available_books_csv(title, available_copies)
            if available_copies == 0:
                self.update_loaned_books_file(title, action="add")

            self.log_action("Lend Book", success=True, details=f"Book '{title}' lent to {username}.")
            print(f"Book '{title}' lent to {username}.")
            return True

        else:
            return False

    def update_loaned_books_file(self, title, action="add"):
        try:

            with open(get_csv_path("loaned_books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            with open(get_csv_path("loaned_books.csv"), mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Title"])
                writer.writeheader()
                for row in rows:
                    if row["Title"].lower() == title.lower() and action == "remove":
                        continue
                    writer.writerow(row)
                if action == "add":
                    writer.writerow({"Title": title})

        except FileNotFoundError as e:
            print(f"ERROR: File loaned_books.csv not found. {e}")
            raise FileNotFoundError("The file loaned_books.csv is missing.")
        except Exception as e:
            print(f"ERROR: Failed to update loaned_books.csv for '{title}': {e}")

    def add_to_waitlist(self, title, username, email, phone):
        """
        Add a user to the waitlist for a specific book and log the action.
        Prevents adding entries with missing details or duplicates.
        """
        try:
            # Validate input fields
            if not username or not email or not phone:
                print(f"ERROR: Missing required fields for user '{username}'.")
                self.log_action(
                    "Add to Waitlist",
                    success=False,
                    details=f"Failed to add to waitlist for '{title}': Missing fields."
                )
                return

            # Check if the book exists in the waitlist
            if title not in self.waitlist:
                self.waitlist[title] = []

            # Prevent duplicate entries
            for user in self.waitlist[title]:
                if user["username"] == username and user["email"] == email and user["phone"] == phone:
                    print(f"User '{username}' is already in the waitlist for '{title}'.")
                    return

            # Add the user to the waitlist
            self.waitlist[title].append({"username": username, "email": email, "phone": phone})
            self.sync_waitlist_to_file()

            # Log the success
            self.log_action(
                "Add to Waitlist",
                success=True,
                details=f"User '{username}' added to waitlist for book '{title}'."
            )
            print(f"User '{username}' added to the waitlist for '{title}'.")

        except Exception as e:
            print(f"ERROR: Failed to add to waitlist: {e}")
            self.log_action(
                "Add to Waitlist",
                success=False,
                details=f"Error occurred while adding '{username}' to waitlist for '{title}': {e}"
            )

    def get_popular_books(self, top_n=10):
        """
        Get the top N most popular books based on the number of borrowed copies.
        """
        popular_books = []

        try:
            # Load available copies from available_books.csv
            available_books = {}
            with open(get_csv_path("available_books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row.get("Title", "").strip()
                    available_copies = int(row.get("Available", 0))
                    if title:
                        available_books[title] = available_copies

            # Calculate borrowed copies for each book
            for book in self.books:
                total_copies = book.copies
                available_copies = available_books.get(book.title, 0)
                borrowed_copies = total_copies - available_copies

                # Include only books that have borrowed copies
                if borrowed_copies > 0:
                    popular_books.append((book.title, borrowed_copies))

            # Sort by borrowed copies in descending order
            popular_books = sorted(popular_books, key=lambda x: x[1], reverse=True)

            # Return the top N books
            return popular_books[:top_n]

        except FileNotFoundError:
            print("ERROR: available_books.csv not found.")
            return []
        except Exception as e:
            print(f"ERROR: Failed to calculate popular books: {e}")
            return []

    def remove_from_loaned_books(self, title):
        """
        Remove a book from loaned_books.csv if it is returned and has available copies.
        """
        try:
            with open( get_csv_path("loaned_books.csv"), mode="r", encoding="utf-8") as file:
                lines = file.readlines()

            with open(get_csv_path("loaned_books.csv"), mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Title"])
                for line in lines[1:]:
                    if line.strip() != title:
                        writer.writerow([line.strip()])
        except Exception as e:
            print(f"ERROR: Failed to update loaned_books.csv: {e}")

    def return_book(self, title):
        """
        Return a specific book to the inventory.
        If a user is in the waitlist, lend the book to them immediately.
        If no users are in the waitlist, update CSV files accordingly.
        """

        book_to_return = next((book for book in self.books if book.title.lower() == title.lower()), None)
        if not book_to_return:
            print(f"ERROR: Book '{title}' not found in inventory.")
            self.log_action("Return Book", success=False, details=f"Book '{title}' not found.")
            return False

        waitlist_users = self.waitlist.get(title, [])
        if waitlist_users:
            next_user = waitlist_users.pop(0)
            self.sync_waitlist_to_file()
            self.lend_book(title, next_user["username"], next_user["email"], next_user["phone"])
            print(f"INFO: The book '{title}' was lent to '{next_user['username']}' from the waitlist.")
            self.sync_waitlist_to_file()
            return True

        try:
            book_found = False

            with open(get_csv_path("available_books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                available_books_data = list(reader)

            for row in available_books_data:
                if row["Title"].lower() == title.lower():
                    current_available = int(row["Available"])
                    if current_available >= book_to_return.copies:
                        print(f"INFO: All copies of '{title}' are already available.")
                        self.log_action("Return Book", success=False,
                                        details=f"All copies of '{title}' are already available.")
                        return "all_copies_available"
                    row["Available"] = str(current_available + 1)
                    book_found = True
                    break

            if not book_found:
                available_books_data.append({"Title": title, "Available": "1"})

            with open(get_csv_path("available_books.csv"), mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Title", "Available"])
                writer.writeheader()
                writer.writerows(available_books_data)


            self.update_loaned_books_file(title, action="remove")

            self.log_action("Return Book", success=True, details=f"Book '{title}' returned successfully.")
            print(f"Book '{title}' returned successfully.")
            return True

        except Exception as e:
            print(f"ERROR: Failed to return book '{title}': {e}")
            self.log_action("Return Book", success=False, details=f"Error: {e}")
            return False

    def update_available_books_csv(self, title, available_copies):
        """
        Update the available_books.csv file for a specific book after lending it.
        """
        try:
            rows = []
            found = False

            with open(get_csv_path("available_books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Title"].lower() == title.lower():
                        row["Available"] = str(available_copies)
                        found = True
                    rows.append(row)

            if not found:
                rows.append({"Title": title, "Available": str(available_copies)})

            with open(get_csv_path("available_books.csv"), mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Title", "Available"])
                writer.writeheader()
                writer.writerows(rows)

        except Exception as e:
            print(f"ERROR: Failed to update available_books.csv: {e}")

    def sync_to_files(self):
        """
        Sync all data to the corresponding CSV files: books.csv, available_books.csv, loaned_books.csv.
        """
        try:
            # Update books.csv
            with open(get_csv_path("books.csv"), mode="w", newline="", encoding="utf-8") as books_file:
                writer = csv.writer(books_file)
                writer.writerow(["title", "author", "is_loaned", "copies", "genre", "year"])
                for book in self.books:
                    writer.writerow([
                        book.title,
                        book.author,
                        "Yes" if book.available_copies < book.copies else "No",
                        book.copies,
                        book.category,
                        book.year
                    ])

            # Update available_books.csv
            with open(get_csv_path("available_books.csv"), mode="w", newline="", encoding="utf-8") as available_file:
                writer = csv.writer(available_file)
                writer.writerow(["Title", "Available"])
                for book in self.books:
                    if book.available_copies > 0:
                        writer.writerow([book.title, book.available_copies])

            # Update loaned_books.csv
            with open(get_csv_path("loaned_books.csv"), mode="w", newline="", encoding="utf-8") as loaned_file:
                writer = csv.writer(loaned_file)
                writer.writerow(["Title"])
                for book in self.books:
                    if book.available_copies == 0:
                        writer.writerow([book.title])

            print("SUCCESS: Files synced successfully (books.csv, available_books.csv, loaned_books.csv).")
        except Exception as e:
            print(f"ERROR: Failed to sync files: {e}")

    def load_waitlist_from_file(self):
        """
        Load the waitlist from a CSV file into the system.
        """
        try:
            with open(get_csv_path("waiting_list.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book_title = row["Book Title"]
                    if book_title not in self.waitlist:
                        self.waitlist[book_title] = []
                    self.waitlist[book_title].append({
                        "username": row["Username"],
                        "email": row["Email"],
                        "phone": row["Phone"]
                    })
        except FileNotFoundError:
            print("WARNING: waiting_list.csv not found. Starting with an empty waitlist.")
        except Exception as e:
            print(f"ERROR: Failed to load waitlist: {e}")

    def sync_waitlist_to_file(self):
        """
        Sync the waitlist to a CSV file, removing duplicates and ensuring consistency.
        """
        try:
            with open(get_csv_path("waiting_list.csv"), mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Book Title", "Username", "Email", "Phone"])  # כותרת

                for title, users in self.waitlist.items():
                    for user in users:
                        writer.writerow([title, user["username"], user["email"], user["phone"]])

        except Exception as e:
            print(f"ERROR: Failed to sync waitlist to file: {e}")

    def update_loaned_books_file(self, title, action="add"):
        """
        Add or remove a book from loaned_books.csv.

        :param title: The title of the book.
        :param action: Action type ('add' or 'remove').
        """
        try:

            with open(get_csv_path("loaned_books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            with open(get_csv_path("loaned_books.csv"), mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Title"])
                writer.writeheader()
                for row in rows:
                    if row["Title"].lower() == title.lower() and action == "remove":
                        continue
                    writer.writerow(row)

                if action == "add":
                    writer.writerow({"Title": title})

        except Exception as e:
            print(f"ERROR: Failed to update loaned_books.csv for '{title}': {e}")

    def load_books(self):
        """
        Load books from a CSV file into the inventory and log the action.
        """
        try:
            with open(get_csv_path("books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_book = next((b for b in self.books if b.title == row["title"]), None)
                    if existing_book:
                        continue

                    book = BookFactory.create_book(
                        title=row["title"],
                        author=row["author"],
                        is_loaned=row["is_loaned"] == "Yes",
                        copies=int(row["copies"]),
                        genre=row["genre"],
                        year=int(row["year"]),
                        books=self.books
                    )
                    self.books.append(book)

            self.log_action("Load Books", success=True, details="Books loaded successfully from CSV file.")
            print("Books loaded successfully from file.")
        except FileNotFoundError:
            self.log_action("Load Books", success=False, details="File 'books.csv' not found.")
            print("Error: File 'books.csv' not found.")
        except Exception as e:
            self.log_action("Load Books", success=False, details=f"Error loading books: {e}")
            print(f"Error loading books from file: {e}")

    def log_action(self, action, success=True, details=""):
        """
        Log an action to a log file with timestamp and clear formatting.
        :param action: The action performed (e.g., "Add Book", "Lend Book").
        :param success: Whether the action was successful (True/False).
        :param details: Additional details about the action.
        """
        try:
            with open("log.txt", mode="a", encoding="utf-8") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                status = "SUCCESS" if success else "FAILURE"
                log_file.write(f"[{timestamp}] ACTION: {action} | STATUS: {status} | DETAILS: {details}\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")

    def search_books_with_strategy(self, strategy, value):
        """
        Search books using a given strategy.
        :param strategy: An instance of SearchStrategy.
        :param value: The value to search for.
        :return: List of matching books.
        """
        from search_strategy import SearchManager  #Import the manager
        manager = SearchManager(strategy)
        results = manager.search(self.books, value)
        if results:
            print("Search results:")
            for book in results:
                print(book)
        else:
            print("No books found matching the criteria.")
        return results

    def add_notification(self,message):
        """
        Add a notification message to the system
        """
        self.notifications.append(message)
        print(f"Notification added :{message}")

    def display_notification(self):
        """
        Display all notification and clear the list after it
        """
        if not self.notifications:
            print("No notifications")
        else:
            print("Notifications:")
            for notification in self.notifications:
                print(f"- {notification}")
            self.notifications.clear()

    def check_book_exists(func):
        """
        Decorator to check if a book exists in the inventory before performing an action.
        """

        def wrapper(self, title, *args, **kwargs):
            # Check if the book exists in the inventory
            book = next((b for b in self.books if b.title.lower() == title.lower()), None)
            if not book:
                # Log and raise an exception if the book is not found
                self.log_action(func.__name__, success=False, details=f"Book '{title}' not found in inventory.")
                raise ValueError(f"Book '{title}' not found in inventory.")
            return func(self, title, *args, **kwargs)

        return wrapper

    def handle_exceptions(func):
        """
        Decorator to handle exceptions in a method.
        """

        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                # Log the exception and print an error message
                self.log_action(func.__name__, success=False, details=f"Error: {e}")
                print(f"An error occurred in {func._name_}: {e}")

        return wrapper

