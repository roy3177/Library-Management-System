import pandas as pd
from book import Book


class BookFactory:
    """
    @author Roy Meoded
    @author Noa Agassi
    Factory class for creating and updating books in the inventory.
    Handles the creation of new books, merging with existing ones,
    and updating the inventory file when book copies are modified.
    """

    @staticmethod
    def create_book(title, author, is_loaned, copies, genre, year, books, waiting_list=None):
        """
        Create a new book or update an existing book's copies.

        :param title: Title of the book.
        :param author: Author of the book.
        :param is_loaned: Boolean indicating if the book is currently loaned.
        :param copies: Number of copies to add.
        :param genre: Genre or category of the book.
        :param year: Year of publication.
        :param books: List of existing books in the inventory.
        :param waiting_list: Optional waiting list for the book.
        :return: The created or updated Book object.
        """
        # Convert copies to integer if passed as a string
        copies = int(copies) if isinstance(copies, str) else copies

        # Check if the book already exists in the inventory
        for book in books:
            if book.title == title:
                book.copies += copies
                return book

        # Create a new book and add it to the inventory
        book = Book(title, author, copies, genre, year, is_loaned)

        # Handle waiting list if provided
        if waiting_list:
            if isinstance(waiting_list, str):
                book.waiting_list = waiting_list.split(",")
            elif isinstance(waiting_list, list):
                book.waiting_list = waiting_list

        books.append(book)
        return book

    @staticmethod
    def update_book_copies(book):
        """
        Update the number of copies for a book in the inventory file.

        :param book: The Book object to update.
        :raises FileNotFoundError: If the inventory file does not exist.
        :raises Exception: For any other error during the update.
        """
        try:
            # Load the inventory file into a DataFrame
            df = pd.read_csv("../csv_files/books.csv")

            # Find the index of the book in the DataFrame
            book_index = df[(df["title"] == book.title) & (df["author"] == book.author)].index

            if not book_index.empty:
                # Update the copies column for the book
                df.loc[book_index, "copies"] = book.num_of_copies
                # Save the updated DataFrame back to the file
                df.to_csv("../csv_files/books.csv", index=False)
            else:
                raise ValueError(f"Book '{book.title}' by '{book.author}' not found in inventory.")
        except FileNotFoundError:
            raise FileNotFoundError("The file 'books.csv' was not found.")
        except Exception as e:
            raise Exception(f"Failed to update copies: {e}")