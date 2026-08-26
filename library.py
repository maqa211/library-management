from models import Book, Member


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        for existing_book in self.books:
            if existing_book.book_id == book.book_id:
                raise ValueError("This Book ID already exists.")

        self.books.append(book)

    def delete_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                self.books.remove(book)
                return

        raise ValueError("Book not found.")

    def edit_book(self, book_id, title, author, year, category):
        for book in self.books:
            if book.book_id == book_id:
                book.title = title
                book.author = author
                book.year = year
                book.category = category
                return

        raise ValueError("Book not found.")

    def add_member(self, member):
        for existing_member in self.members:
            if existing_member.member_id == member.member_id:
                raise ValueError("This Member ID already exists.")

        self.members.append(member)

    def delete_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                if member.borrowed_books:
                    raise ValueError(
                        "This member has borrowed books and cannot be deleted."
                    )

                self.members.remove(member)
                return

        raise ValueError("Member not found.")

    def edit_member(self, member_id, name, phone, email):
        for member in self.members:
            if member.member_id == member_id:
                member.name = name
                member.phone = phone
                member.email = email
                return

        raise ValueError("Member not found.")

    def search_book(self, keyword, search_by):
        keyword = keyword.lower()

        results = []

        for book in self.books:
            if search_by == "id" and keyword in book.book_id.lower():
                results.append(book)

            elif search_by == "title" and keyword in book.title.lower():
                results.append(book)

            elif search_by == "author" and keyword in book.author.lower():
                results.append(book)

            elif search_by == "category" and keyword in book.category.lower():
                results.append(book)

        return results

    def sort_books(self, sort_by):
        if sort_by == "title":
            return sorted(self.books, key=lambda book: book.title.lower())

        elif sort_by == "author":
            return sorted(self.books, key=lambda book: book.author.lower())

        elif sort_by == "year_asc":
            return sorted(self.books, key=lambda book: book.year)

        elif sort_by == "year_desc":
            return sorted(self.books, key=lambda book: book.year, reverse=True)

        elif sort_by == "category":
            return sorted(self.books, key=lambda book: book.category.lower())

        raise ValueError("Invalid sorting option.")

    def borrow_book(self, member_id, book_id):
        member = None
        book = None

        for m in self.members:
            if m.member_id == member_id:
                member = m
                break

        for b in self.books:
            if b.book_id == book_id:
                book = b
                break

        if member is None:
            raise ValueError("Member not found.")

        if book is None:
            raise ValueError("Book not found.")

        if not book.availability:
            raise ValueError("This book is already borrowed.")

        book.availability = False
        member.borrowed_books.append(book.book_id)

    def return_book(self, member_id, book_id):
        member = None
        book = None

        for m in self.members:
            if m.member_id == member_id:
                member = m
                break

        for b in self.books:
            if b.book_id == book_id:
                book = b
                break

        if member is None:
            raise ValueError("Member not found.")

        if book is None:
            raise ValueError("Book not found.")

        if book.book_id not in member.borrowed_books:
            raise ValueError("This book was not borrowed by this member.")

        book.availability = True
        member.borrowed_books.remove(book.book_id)

    def get_statistics(self):
        total_books = len(self.books)
        available_books = sum(1 for book in self.books if book.availability)
        borrowed_books = total_books - available_books
        total_members = len(self.members)

        category_counts = {}

        for book in self.books:
            category_counts[book.category] = (
                category_counts.get(book.category, 0) + 1
            )

        most_common_category = "N/A"

        if category_counts:
            most_common_category = max(
                category_counts,
                key=category_counts.get
            )

        return {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": borrowed_books,
            "total_members": total_members,
            "most_common_category": most_common_category
        }
