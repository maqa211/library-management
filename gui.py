```python
import tkinter as tk
from tkinter import ttk, messagebox
from models import Book, Member
from library import Library
from file_manager import FileManager
from validators import validate_book, validate_member

BG = "#D9F0FF"
BTN = "#B8DFFF"


class LibraryGUI:
    def __init__(self, root):
        self.root = root
        root.title("Library Management")
        root.geometry("900x600")
        root.configure(bg=BG)

        self.library = Library()
        self.files = FileManager()
        self.library.books = self.files.load_books()
        self.library.members = self.files.load_members()

        style = ttk.Style()
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10))

        self.build()
        self.refresh()

    def build(self):
        ttk.Label(
            self.root, text="Library Management",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True)

        self.books = ttk.Frame(self.tabs)
        self.members = ttk.Frame(self.tabs)
        self.borrow = ttk.Frame(self.tabs)
        self.search = ttk.Frame(self.tabs)
        self.stats = ttk.Frame(self.tabs)

        for frame, name in [
            (self.books, "Books"), (self.members, "Members"),
            (self.borrow, "Borrow / Return"),
            (self.search, "Search"), (self.stats, "Statistics")
        ]:
            self.tabs.add(frame, text=name)

        self.book_page()
        self.member_page()
        self.borrow_page()
        self.search_page()
        self.stats_page()

    def entries(self, parent, names):
        result = []
        for i, name in enumerate(names):
            ttk.Label(parent, text=name).grid(row=0, column=i, padx=3)
            e = ttk.Entry(parent, width=16)
            e.grid(row=1, column=i, padx=3, pady=3)
            result.append(e)
        return result

    def book_page(self):
        self.be = self.entries(
            self.books, ["ID", "Title", "Author", "Year", "Category"]
        )
        for i, (text, cmd) in enumerate([
            ("Add", self.add_book),
            ("Edit", self.edit_book),
            ("Delete", self.delete_book)
        ]):
            ttk.Button(
                self.books, text=text, command=cmd
            ).grid(row=2, column=i, pady=8)

        self.bt = self.table(
            self.books,
            ("ID", "Title", "Author", "Year", "Category", "Status")
        )
        self.bt.grid(row=3, column=0, columnspan=5, sticky="nsew")

    def member_page(self):
        self.me = self.entries(
            self.members, ["ID", "Name", "Phone", "Email"]
        )
        for i, (text, cmd) in enumerate([
            ("Add", self.add_member),
            ("Edit", self.edit_member),
            ("Delete", self.delete_member)
        ]):
            ttk.Button(
                self.members, text=text, command=cmd
            ).grid(row=2, column=i, pady=8)

        self.mt = self.table(
            self.members,
            ("ID", "Name", "Phone", "Email", "Borrowed")
        )
        self.mt.grid(row=3, column=0, columnspan=4, sticky="nsew")

    def borrow_page(self):
        ttk.Label(self.borrow, text="Member ID").pack(pady=5)
        self.mc = ttk.Combobox(self.borrow, state="readonly")
        self.mc.pack()

        ttk.Label(self.borrow, text="Book ID").pack(pady=5)
        self.bc = ttk.Combobox(self.borrow, state="readonly")
        self.bc.pack()

        ttk.Button(
            self.borrow, text="Borrow", command=self.borrow_book
        ).pack(pady=5)
        ttk.Button(
            self.borrow, text="Return", command=self.return_book
        ).pack()

    def search_page(self):
        self.sc = ttk.Combobox(
            self.search,
            values=["id", "title", "author", "category"],
            state="readonly"
        )
        self.sc.current(0)
        self.sc.pack(side="left", padx=5, pady=8)

        self.se = ttk.Entry(self.search)
        self.se.pack(side="left")

        ttk.Button(
            self.search, text="Search", command=self.search_book
        ).pack(side="left", padx=5)

        self.sort = ttk.Combobox(
            self.search,
            values=["title", "author", "year_asc", "year_desc", "category"],
            state="readonly"
        )
        self.sort.current(0)
        self.sort.pack(side="left")

        ttk.Button(
            self.search, text="Sort", command=self.sort_books
        ).pack(side="left", padx=5)

        self.st = self.table(
            self.search, ("ID", "Title", "Author", "Year", "Category")
        )
        self.st.pack(fill="both", expand=True)

    def stats_page(self):
        self.stat = ttk.Label(
            self.stats, font=("Arial", 16), justify="center"
        )
        self.stat.pack(pady=60)

    def table(self, parent, columns):
        t = ttk.Treeview(parent, columns=columns, show="headings")
        for c in columns:
            t.heading(c, text=c)
            t.column(c, width=120)
        return t

    def run(self, action, success):
        try:
            action()
            self.save()
            self.refresh()
            messagebox.showinfo("Success", success)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def add_book(self):
        v = [e.get().strip() for e in self.be]
        year = validate_book(*v)
        self.library.add_book(Book(v[0], v[1], v[2], year, v[4]))

    def edit_book(self):
        v = [e.get().strip() for e in self.be]
        year = validate_book(*v)
        self.library.edit_book(v[0], v[1], v[2], year, v[4])

    def delete_book(self):
        self.library.delete_book(self.be[0].get())

    def add_member(self):
        v = [e.get().strip() for e in self.me]
        validate_member(*v)
        self.library.add_member(Member(*v))

    def edit_member(self):
        v = [e.get().strip() for e in self.me]
        validate_member(*v)
        self.library.edit_member(*v)

    def delete_member(self):
        self.library.delete_member(self.me[0].get())

    def borrow_book(self):
        self.run(
            lambda: self.library.borrow_book(
                self.mc.get(), self.bc.get()
            ),
            "Book borrowed."
        )

    def return_book(self):
        self.run(
            lambda: self.library.return_book(
                self.mc.get(), self.bc.get()
            ),
            "Book returned."
        )

    def search_book(self):
        self.show(self.library.search_book(
            self.se.get(), self.sc.get()
        ))

    def sort_books(self):
        self.show(self.library.sort_books(self.sort.get()))

    def show(self, books):
        self.st.delete(*self.st.get_children())
        for b in books:
            self.st.insert("", "end", values=(
                b.book_id, b.title, b.author, b.year, b.category
            ))

    def refresh(self):
        self.bt.delete(*self.bt.get_children())
        for b in self.library.books:
            self.bt.insert("", "end", values=(
                b.book_id, b.title, b.author, b.year,
                b.category,
                "Available" if b.availability else "Borrowed"
            ))

        self.mt.delete(*self.mt.get_children())
        for m in self.library.members:
            self.mt.insert("", "end", values=(
                m.member_id, m.name, m.phone, m.email,
                ", ".join(m.borrowed_books)
            ))

        self.mc["values"] = [m.member_id for m in self.library.members]
        self.bc["values"] = [b.book_id for b in self.library.books]

        s = self.library.get_statistics()
        self.stat.config(text=
            f"Total Books: {s['total_books']}\n"
            f"Available: {s['available_books']}\n"
            f"Borrowed: {s['borrowed_books']}\n"
            f"Members: {s['total_members']}\n"
            f"Top Category: {s['most_common_category']}"
        )

    def save(self):
        self.files.save_books(self.library.books)
        self.files.save_members(self.library.members)


if __name__ == "__main__":
    root = tk.Tk()
    LibraryGUI(root)
    root.mainloop()
```
