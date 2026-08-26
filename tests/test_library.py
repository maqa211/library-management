import unittest

from models import Book, Member
from library import Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.library = Library()

    def test_add_book(self):
        book = Book(
            "B1",
            "Python",
            "John",
            2024,
            "Programming"
        )

        self.library.add_book(book)

        self.assertEqual(len(self.library.books), 1)

    def test_delete_book(self):
        book = Book(
            "B1",
            "Python",
            "John",
            2024,
            "Programming"
        )

        self.library.add_book(book)
        self.library.delete_book("B1")

        self.assertEqual(len(self.library.books), 0)

    def test_search_book(self):
        book = Book(
            "B1",
            "Python",
            "John",
            2024,
            "Programming"
        )

        self.library.add_book(book)

        result = self.library.search_book(
            "Python",
            "title"
        )

        self.assertEqual(len(result), 1)

    def test_add_member(self):
        member = Member(
            "M1",
            "Ali",
            "0500000000",
            "ali@gmail.com"
        )

        self.library.add_member(member)

        self.assertEqual(len(self.library.members), 1)

    def test_borrow_and_return(self):
        book = Book(
            "B1",
            "Python",
            "John",
            2024,
            "Programming"
        )

        member = Member(
            "M1",
            "Ali",
            "0500000000",
            "ali@gmail.com"
        )

        self.library.add_book(book)
        self.library.add_member(member)

        self.library.borrow_book("M1", "B1")

        self.assertFalse(book.availability)
        self.assertIn("B1", member.borrowed_books)

        self.library.return_book("M1", "B1")

        self.assertTrue(book.availability)
        self.assertNotIn("B1", member.borrowed_books)


if __name__ == "__main__":
    unittest.main()
