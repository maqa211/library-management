class Book:
    def __init__(self, book_id, title, author, year, category, availability=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.category = category
        self.availability = availability

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "category": self.category,
            "availability": self.availability
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["book_id"],
            data["title"],
            data["author"],
            data["year"],
            data["category"],
            data["availability"]
        )


class Member:
    def __init__(self, member_id, name, phone, email, borrowed_books=None):
        self.member_id = member_id
        self.name = name
        self.phone = phone
        self.email = email
        self.borrowed_books = borrowed_books if borrowed_books is not None else []

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "borrowed_books": self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["member_id"],
            data["name"],
            data["phone"],
            data["email"],
            data.get("borrowed_books", [])
        )
