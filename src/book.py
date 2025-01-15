"""
@author Roy Meoded
@author Noa Agassi
The Book class represents a single book in the library management system.
It contains attributes like title, author, total copies, category, year of publication,
and whether the book is currently loaned.
The class also provides methods to lend and return copies of the book,
track the number of times the book has been borrowed,
and calculate the number of available copies at any given time.
"""
class Book:
    def __init__(self, title, author, copies, category, year, is_loaned=False):
        """
        Initialize a Book object.
        :param title: Title of the book.
        :param author: Author of the book.
        :param copies: Total number of copies available for the book.
        :param category: Category or genre of the book.
        :param year: Year of publication.
        :param is_loaned: Boolean indicating if the book is currently loaned.
        """
        self.title = title  # Book title
        self.author = author  # Book author
        self.copies = int(copies)  # Total number of copies
        self.category = category  # Book category
        self.year = year  # Year of publication
        self.is_loaned = is_loaned  # Is the book currently loaned?
        self.borrow_count = 0  # The number of lends for the book

    @property
    def available_copies(self):
        return self.copies - self.borrow_count

    def lend(self):
        """
        Lend a copy of the book if available.
        :return: True if the book was successfully lent, False otherwise.
        """
        if self.available_copies > 0:
            self.borrow_count += 1
        else:
            raise ValueError("No copies available to lend")

    def return_copy(self):
        """
        Return a copy of the book.
        :return: True if the book was successfully returned, False otherwise.
        """
        if self.borrow_count > 0:
            self.borrow_count -= 1
            if self.available_copies > 0:
                self.is_loaned = False
            return True
        else:
            return False

    def __str__(self):
        """
        Return a string representation of the book.
        """
        loan_status = "Loaned" if self.is_loaned else "Available"
        return f"The book : {self.title},  author:{self.author} ,category:{self.category},year: ({self.year}) , available copies:{self.available_copies}/copies:{self.copies}\n"