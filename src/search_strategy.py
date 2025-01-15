
from abc import ABC ,abstractmethod

#Basic class for search strategy:
class SearchStrategy(ABC):
    """""
    Abstract base class for search strategies
    """""
    @abstractmethod
    def search(self,books,value):
        """""
        Abstract method for searching books
        Return list of matching books
        """""
        pass

#Search by title:
class SearchByTitle(SearchStrategy):
    """""
    Search strategy to find books by title
    """""
    def search(self,books,value):
        return [book for book in books if value.lower() in book.title.lower()]

#Search by author:
class SearchByAuthor(SearchStrategy):
    """""
    Search strategy to find books by author
    """""
    def search(self,books,value):
        return [book for book in books if value.lower() in book.author.lower()]

#Search by title:
class SearchByCategory(SearchStrategy):
    """""
    Search strategy to find books by category
    """""
    def search(self,books,value):
        return [book for book in books if value.lower() in book.category.lower()]

#Manges the strategies:
class SearchManager:
    """""
    Manager to handle search strategies
    """""
    def __init__(self,strategy):
        self.strategy=strategy

    def set_strategy(self,strategy):
        """""
        Set a new search strategy
        """""
        self.strategy=strategy

    def search(self,books,value):
        """""
        Perform a search using the current strategy
        """""
        return self.strategy.search(books,value)