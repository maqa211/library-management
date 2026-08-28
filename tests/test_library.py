import unittest

from models import Book, Member
from library import Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.library.books = []
        self.library.members = []

    def test_add_book(self):
        book = Book("B100", "Python Basics", "John Smith", 2024, "Programming")
        self.library.add_book(book)

        self.assertEqual(len(self.library.books), 1)

    def test_delete_book(self):
        book = Book("B100", "Python Basics", "John Smith", 2024, "Programming")
        self.library.add_book(book)
        self.library.delete_book("B100")

        self.assertEqual(len(self.library.books), 0)

    def test_search_book(self):
        book = Book("B100", "Python Basics", "John Smith", 2024, "Programming")
        self.library.add_book(book)

        result = self.library.search_books("Title", "Python")

        self.assertEqual(len(result), 1)

    def test_add_member(self):
        member = Member("M100", "Ali Aliyev", "0501234567", "ali@gmail.com")
        self.library.add_member(member)

        self.assertEqual(len(self.library.members), 1)

    def test_borrow_book(self):
        book = Book("B100", "Python Basics", "John Smith", 2024, "Programming")
        member = Member("M100", "Ali Aliyev", "0501234567", "ali@gmail.com")

        self.library.add_book(book)
        self.library.add_member(member)

        self.library.borrow_book("M100", "B100")

        self.assertFalse(self.library.books[0]["availability"])

    def test_return_book(self):
        book = Book("B100", "Python Basics", "John Smith", 2024, "Programming")
        member = Member("M100", "Ali Aliyev", "0501234567", "ali@gmail.com")

        self.library.add_book(book)
        self.library.add_member(member)

        self.library.borrow_book("M100", "B100")
        self.library.return_book("M100", "B100")

        self.assertTrue(self.library.books[0]["availability"])


if __name__ == "__main__":
    unittest.main()
