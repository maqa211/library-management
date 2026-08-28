import json


class FileManager:

    def load_books(self):
        try:
            with open("data/books.json", "r", encoding="utf-8") as file:
                return json.load(file)

        except FileNotFoundError:
            print("Books file not found.")
            return []

        except json.JSONDecodeError:
            print("Invalid JSON format.")
            return []

    def save_books(self, books):
        with open("data/books.json", "w", encoding="utf-8") as file:
            json.dump(books, file, indent=4, ensure_ascii=False)

    def load_members(self):
        try:
            with open("data/members.json", "r", encoding="utf-8") as file:
                return json.load(file)

        except FileNotFoundError:
            print("Members file not found.")
            return []

        except json.JSONDecodeError:
            print("Invalid JSON format.")
            return []

    def save_members(self, members):
        with open("data/members.json", "w", encoding="utf-8") as file:
            json.dump(members, file, indent=4, ensure_ascii=False)
