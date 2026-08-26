import tkinter as tk
from tkinter import ttk, messagebox

from models import Book, Member
from library import Library
from file_manager import FileManager
from validators import validate_book, validate_member


class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1000x650")

        self.library = Library()
        self.file_manager = FileManager()

        self.load_data()

        self.create_widgets()

    def load_data(self):
        self.library.books = self.file_manager.load_books()
        self.library.members = self.file_manager.load_members()

    def save_data(self):
        self.file_manager.save_books(self.library.books)
        self.file_manager.save_members(self.library.members)

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Library Management System",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=15)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.books_tab = ttk.Frame(self.notebook)
        self.members_tab = ttk.Frame(self.notebook)
        self.borrow_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)
        self.statistics_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.books_tab, text="Books")
        self.notebook.add(self.members_tab, text="Members")
        self.notebook.add(self.borrow_tab, text="Borrow / Return")
        self.notebook.add(self.search_tab, text="Search / Sort")
        self.notebook.add(self.statistics_tab, text="Statistics")

        self.create_books_tab()
        self.create_members_tab()
        self.create_borrow_tab()
        self.create_search_tab()
        self.create_statistics_tab()

    def create_books_tab(self):
        pass

    def create_members_tab(self):
        pass

    def create_borrow_tab(self):
        pass

    def create_search_tab(self):
        pass

    def create_statistics_tab(self):
        pass

    def refresh_all(self):
        pass

    def update_statistics(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
