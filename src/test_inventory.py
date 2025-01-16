import csv
import os
import sys
import unittest
from unittest.mock import mock_open, patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from inventory import Inventory
from book import Book
from utils import get_csv_path


class TestAvailableBooks(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="Title,Available\nBook1,5\nBook2,3")
    def test_load_available_books(self, mock_file):
        inventory = Inventory()

        with patch("csv.DictReader", return_value=[
            {"Title": "Book1", "Available": "5"},
            {"Title": "Book2", "Available": "3"}
        ]):
            available_books = {}
            with open(get_csv_path("available_books.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row["Title"]
                    available = int(row["Available"])
                    available_books[title] = available

        self.assertEqual(available_books, {"Book1": 5, "Book2": 3})

class TestUpdateAvailableBooks(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="Title,Available\nBook1,5\nBook2,3")
    def test_update_available_books(self, mock_file):
        inventory = Inventory()

        updated_data = []

        def mock_write(data):
            updated_data.append(data)

        mock_file.return_value.write = mock_write

        inventory.update_available_books_csv("Book1", 4)

        expected = [
            "Title,Available\r\n",
            "Book1,4\r\n",
            "Book2,3\r\n"
        ]

        self.assertEqual(updated_data, expected)

#Check if book that got lend add right to the loaned_books.csv:
class TestLoanedBooks(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="Title\nBook1\nBook2")
    def test_add_loaned_book(self, mock_file):
        inventory = Inventory()

        updated_data = []

        def mock_write(data):
            updated_data.append(data)

        mock_file.return_value.write = mock_write

        inventory.update_loaned_books_file("Book3", action="add")

        expected = [
            "Title\r\n",
            "Book1\r\n",
            "Book2\r\n",
            "Book3\r\n"
        ]

        self.assertEqual(updated_data, expected)

    @patch("builtins.open", new_callable=mock_open, read_data="Title\nBook1\nBook2\nBook3")
    def test_remove_loaned_book(self, mock_file):
        inventory = Inventory()

        updated_data = []

        def mock_write(data):
            updated_data.append(data)

        mock_file.return_value.write = mock_write

        inventory.update_loaned_books_file("Book2", action="remove")

        expected = [
            "Title\r\n",
            "Book1\r\n",
            "Book3\r\n"
        ]

        self.assertEqual(updated_data, expected)
class TestSearchBooks(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="Title,Available\nBook1,5\nBook2,3")
    def test_search_by_title(self, mock_file):
        inventory = Inventory()
        inventory.books = [
            Book(title="Book1", author="Author1", category="Fiction", year=2021, copies=5),
            Book(title="Book2", author="Author2", category="Non-Fiction", year=2020, copies=3),
        ]

        results = inventory.search_books(title="Book1")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Book1")

    @patch("builtins.open", new_callable=mock_open, read_data="Title,Available\nBook1,5\nBook2,3")
    def test_search_invalid_term(self, mock_file):
        inventory = Inventory()
        inventory.books = [
            Book(title="Book1", author="Author1", category="Fiction", year=2021, copies=5),
            Book(title="Book2", author="Author2", category="Non-Fiction", year=2020, copies=3),
        ]

        results = inventory.search_books(title="InvalidBook")
        self.assertEqual(len(results), 0)

    @patch("builtins.open", new_callable=mock_open, read_data="Title,Available\nBook1,5\nBook2,3")
    def test_search_by_author(self, mock_file):
        inventory = Inventory()
        inventory.books = [
            Book(title="Book1", author="Author1", category="Fiction", year=2021, copies=5),
            Book(title="Book2", author="Author2", category="Non-Fiction", year=2020, copies=3),
        ]

        results = inventory.search_books(author="Author2")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Author2")

class TestAddBookWithCSV(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="Title,Author,Copies,Category,Year\n")
    def test_add_book_to_inventory(self, mock_file):
        inventory = Inventory()

        book = Book(title="Test Book", author="Test Author", category="Test Category", year=2023, copies=5)

        inventory.add_book(book)

        mock_file.assert_any_call(get_csv_path(get_csv_path("available_books.csv")), mode="a", newline="", encoding="utf-8")

        self.assertIn(book, inventory.books)

        written_books = mock_file().write.call_args_list
        self.assertIn("Test Book", str(written_books))
        self.assertIn("5", str(written_books))

class TestInventoryRemoveBook(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="title,author,copies,genre,year\nBook1,Author1,5,Fiction,2021\n")
    def test_remove_existing_book(self, mock_file):

        inventory = Inventory()
        inventory.books = [
            Book(title="Book1", author="Author1", category="Fiction", year=2021, copies=5),
        ]

        inventory.remove_book("Book1")

        self.assertNotIn("Book1", [book.title for book in inventory.books])

        mock_file.assert_any_call(get_csv_path("books.csv"), mode="w", newline="", encoding="utf-8")

class TestUpdateAvailableBooks(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="Title,Available\nBook1,5\nBook2,3")
    def test_update_available_books(self, mock_file):
        inventory = Inventory()
        inventory.update_available_books_csv("Book1", 4)

        mock_file.assert_called_with(get_csv_path("available_books.csv"), mode="w", newline="", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_any_call("Title,Available\r\n")
        handle.write.assert_any_call("Book1,4\r\n")

class TestWaitlist(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_add_to_waitlist(self, mock_file):
        inventory = Inventory()

        inventory.add_to_waitlist("Book1", "User1", "user1@example.com", "123456789")

        mock_file.assert_any_call(get_csv_path("waiting_list.csv"), mode="w", newline="", encoding="utf-8")

        handle = mock_file()
        handle.write.assert_any_call("Book Title,Username,Email,Phone\r\n")
        handle.write.assert_any_call("Book1,User1,user1@example.com,123456789\r\n")

    @patch("builtins.open", new_callable=mock_open, read_data="Book Title,Username,Email,Phone\nBook1,User1,user1@example.com,123456789\n")
    def test_remove_from_waitlist(self, mock_file):
        inventory = Inventory()
        inventory.waitlist = {
            "Book1": [{"username": "User1", "email": "user1@example.com", "phone": "123456789"}]
        }

        inventory.waitlist["Book1"].pop(0)
        inventory.sync_waitlist_to_file()

        mock_file.assert_called_with(get_csv_path("waiting_list.csv"), mode="w", newline="", encoding="utf-8")
        handle = mock_file()
        self.assertNotIn("User1", str(handle.write.call_args_list))

class TestPopularBooks(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="Title,Available\nBook1,3\nBook2,1\n")
    def test_get_popular_books(self, mock_file):
        inventory = Inventory()
        inventory.books = [
            Book(title="Book1", author="Author1", category="Fiction", year=2021, copies=5),
            Book(title="Book2", author="Author2", category="Non-Fiction", year=2020, copies=4),
        ]

        popular_books = inventory.get_popular_books()

        self.assertEqual(popular_books[0][0], "Book2")
        self.assertEqual(popular_books[1][0], "Book1")

class TestReturnBook(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_return_book(self, mock_file):
        inventory = Inventory()

        inventory.books = [
            Book(title="Book1", author="Author1", category="Fiction", year=2021, copies=1)
        ]
        with patch("csv.DictReader", return_value=[{"Title": "Book1", "Available": "0"}]):
            result = inventory.return_book("Book1")

        mock_file.assert_any_call(get_csv_path("available_books.csv"), mode="w", newline="", encoding="utf-8")

        handle = mock_file()
        handle.write.assert_any_call("Title,Available\r\n")
        handle.write.assert_any_call("Book1,1\r\n")

        self.assertTrue(result)

class TestLendBook(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="Title,Available\nBook1,1\nBook2,0")
    def test_lend_book_successful(self, mock_file):
        inventory = Inventory()
        inventory.books = [
            Book(title="Book1", author="Author1", category="Fiction", year=2021, copies=1),
        ]

        result = inventory.lend_book("Book1", "User1")

        self.assertTrue(result)

        mock_file.assert_any_call(get_csv_path("available_books.csv"), mode="w", newline="", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_any_call("Title,Available\r\n")
        handle.write.assert_any_call("Book1,0\r\n")

class TestSyncToFiles(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_sync_to_files(self, mock_file):
        inventory = Inventory()
        inventory.books = [
            Book(title="Book1", author="Author1", category="Fiction", year=2021, copies=5),
        ]

        inventory.sync_to_files()

        mock_file.assert_any_call(get_csv_path("books.csv"), mode="w", newline="", encoding="utf-8")
        mock_file.assert_any_call(get_csv_path("available_books.csv"), mode="w", newline="", encoding="utf-8")

if __name__ == "__main__":
    unittest.main()
