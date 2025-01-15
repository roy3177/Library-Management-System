


import pandas as pd
from book_factory import BookFactory
class UpdateFiles(object):


    @staticmethod
    def update_books_file(book):
        try:
            # Convert the book object to a dictionary
            row = {
                "title": book.title,
                "author": book.author,
                "is_loaned": "Yes" if book.is_loaned else "No",
                "copies": book.copies,
                "genre": book.category,
                "year": book.year
            }

            # Create a DataFrame from the dictionary
            df = pd.DataFrame([row])

            # Append the DataFrame to the CSV file with a proper line terminator
            with open("../csv_files/books.csv",mode="a",newline='',encoding="utf-8") as file:
                df.to_csv(file,index=False,header=False)

            print("SUCCESS: Book added to books.csv")
            print(df.to_string(index=False))
        except Exception as e:
            print(f"ERROR: Failed to update books file: {e}")
    @staticmethod
    def load_books():
        books = []
        try:
            books_df = pd.read_csv("../csv_files/books.csv", encoding="utf-8")
            print("Loaded books.csv columns:", books_df.columns)
            print("Loaded books.csv data:")
            print(books_df)

            for index, row in books_df.iterrows():
                book = BookFactory.create_book(
                    title=row["title"],
                    author=row["author"],
                    is_loaned=row["is_loaned"]=="Yes",
                    copies=int(row["copies"]),
                    genre=row["genre"],
                    year=int(row["year"]),
                    books=books,
                    waiting_list=row.get("waiting_list")
                )

            print("Books created from file:", [book.title for book in books])
        except FileNotFoundError:
            print("ERROR: File books.csv not found.")
        except Exception as e:
            print(f"ERROR: Error loading books: {e}")

        return books

    @staticmethod
    def load_available_books():
        available_books = {}
        try:
            available_books_df = pd.read_csv("../csv_files/available_books.csv", encoding="utf-8")
            for index, row in available_books_df.iterrows():
                count = row["count"]
                available_books[row["title"]] = int(count) if isinstance(count, str) and count.isdigit() else 0
            print("SUCCESS: Loaded books from available_books.csv")

        except FileNotFoundError:
            print("ERROR: File available_books.csv not found.")
        except Exception as e:
            print(f"ERROR: Error loading available books: {e}")
        print(f"len available = {len(available_books)}")
        return available_books

    @staticmethod
    def load_loaned_books():
        loaned_books = []
        try:
            loaned_books_df = pd.read_csv("../csv_files/loaned_books.csv", encoding="utf-8")
            loaned_books = loaned_books_df['title'].tolist()
            print("SUCCESS: Loaded loaned books from loaned_books.csv")
        except FileNotFoundError:
            print("ERROR: File loaned_books.csv not found.")
        except Exception as e:
            print(f"ERROR: Error loading loaned books: {e}")
        print(f"len available = {len(loaned_books)}")
        return loaned_books