from models import Book, Member
from file_manager import FileManager


class Library:

    def __init__(self):
        self.file_manager = FileManager()

        self.books = self.file_manager.load_books()
        self.members = self.file_manager.load_members()

    def add_book(self, book):
        for existing_book in self.books:
            if existing_book["book_id"] == book.book_id:
                raise ValueError("Book ID already exists.")

        self.books.append(book.to_dict())
        self.file_manager.save_books(self.books)

    def delete_book(self, book_id):
        for book in self.books:
            if book["book_id"] == book_id:

                if book["availability"] == False:
                    raise ValueError("Borrowed book cannot be deleted.")

                self.books.remove(book)
                self.file_manager.save_books(self.books)
                return

        raise ValueError("Book not found.")

    def edit_book(self, book_id, title, author, year, category):
        for book in self.books:
            if book["book_id"] == book_id:
                book["title"] = title
                book["author"] = author
                book["year"] = year
                book["category"] = category

                self.file_manager.save_books(self.books)
                return

        raise ValueError("Book not found.")

    def get_books(self):
        return self.books

    def add_member(self, member):
        for existing_member in self.members:
            if existing_member["member_id"] == member.member_id:
                raise ValueError("Member ID already exists.")

        self.members.append(member.to_dict())
        self.file_manager.save_members(self.members)

    def delete_member(self, member_id):
        for member in self.members:
            if member["member_id"] == member_id:

                if member["borrowed_books"]:
                    raise ValueError("Member has borrowed books.")

                self.members.remove(member)
                self.file_manager.save_members(self.members)
                return

        raise ValueError("Member not found.")

    def edit_member(self, member_id, name, phone, email):
        for member in self.members:
            if member["member_id"] == member_id:
                member["name"] = name
                member["phone"] = phone
                member["email"] = email

                self.file_manager.save_members(self.members)
                return

        raise ValueError("Member not found.")

    def get_members(self):
        return self.members

    def search_books(self, search_type, keyword):
        keyword = keyword.lower()
        results = []

        for book in self.books:

            if search_type == "ID":
                value = book["book_id"].lower()

            elif search_type == "Title":
                value = book["title"].lower()

            elif search_type == "Author":
                value = book["author"].lower()

            elif search_type == "Category":
                value = book["category"].lower()

            else:
                raise ValueError("Invalid search type.")

            if keyword in value:
                results.append(book)

        return results

    def sort_books(self, sort_type):

        if sort_type == "Title A-Z":
            return sorted(
                self.books,
                key=lambda book: book["title"].lower()
            )

        elif sort_type == "Author A-Z":
            return sorted(
                self.books,
                key=lambda book: book["author"].lower()
            )

        elif sort_type == "Year Ascending":
            return sorted(
                self.books,
                key=lambda book: book["year"]
            )

        elif sort_type == "Year Descending":
            return sorted(
                self.books,
                key=lambda book: book["year"],
                reverse=True
            )

        elif sort_type == "Category A-Z":
            return sorted(
                self.books,
                key=lambda book: book["category"].lower()
            )

        else:
            raise ValueError("Invalid sorting option.")

    def borrow_book(self, member_id, book_id):

        member = None
        book = None

        for item in self.members:
            if item["member_id"] == member_id:
                member = item
                break

        if member is None:
            raise ValueError("Member not found.")

        for item in self.books:
            if item["book_id"] == book_id:
                book = item
                break

        if book is None:
            raise ValueError("Book not found.")

        if book["availability"] == False:
            raise ValueError("Book is already borrowed.")

        if book_id in member["borrowed_books"]:
            raise ValueError("Member already borrowed this book.")

        book["availability"] = False
        member["borrowed_books"].append(book_id)

        self.file_manager.save_books(self.books)
        self.file_manager.save_members(self.members)

    def return_book(self, member_id, book_id):

        member = None
        book = None

        for item in self.members:
            if item["member_id"] == member_id:
                member = item
                break

        if member is None:
            raise ValueError("Member not found.")

        for item in self.books:
            if item["book_id"] == book_id:
                book = item
                break

        if book is None:
            raise ValueError("Book not found.")

        if book_id not in member["borrowed_books"]:
            raise ValueError("This member did not borrow this book.")

        member["borrowed_books"].remove(book_id)
        book["availability"] = True

        self.file_manager.save_books(self.books)
        self.file_manager.save_members(self.members)

    def get_statistics(self):

        total_books = len(self.books)

        available_books = 0

        for book in self.books:
            if book["availability"]:
                available_books += 1

        borrowed_books = total_books - available_books

        total_members = len(self.members)

        category_count = {}

        for book in self.books:
            category = book["category"]

            if category not in category_count:
                category_count[category] = 1
            else:
                category_count[category] += 1

        most_common_category = "N/A"

        if category_count:
            most_common_category = max(
                category_count,
                key=category_count.get
            )

        return {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": borrowed_books,
            "total_members": total_members,
            "most_common_category": most_common_category
        }
