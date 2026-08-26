import json
import os

from models import Book, Member


class FileManager:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder

        self.books_file = os.path.join(
            self.data_folder,
            "books.json"
        )

        self.members_file = os.path.join(
            self.data_folder,
            "members.json"
        )

        self.create_data_folder()

    def create_data_folder(self):
        os.makedirs(self.data_folder, exist_ok=True)

    def save_books(self, books):
        data = [book.to_dict() for book in books]

        with open(self.books_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_books(self):
        if not os.path.exists(self.books_file):
            return []

        try:
            with open(self.books_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            return [Book.from_dict(book) for book in data]

        except (json.JSONDecodeError, KeyError):
            return []

    def save_members(self, members):
        data = [member.to_dict() for member in members]

        with open(self.members_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_members(self):
        if not os.path.exists(self.members_file):
            return []

        try:
            with open(self.members_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            return [Member.from_dict(member) for member in data]

        except (json.JSONDecodeError, KeyError):
            return []
