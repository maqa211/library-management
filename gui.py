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
        self.root.geometry("900x600")

        self.library = Library()
        self.files = FileManager()
        self.library.books = self.files.load_books()
        self.library.members = self.files.load_members()

        self.create_gui()
        self.refresh()

    def create_gui(self):
        ttk.Label(
            self.root,
            text="Library Management System",
            font=("Arial", 20)
        ).pack(pady=10)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True)

        self.books = ttk.Frame(self.tabs)
        self.members = ttk.Frame(self.tabs)
        self.borrow = ttk.Frame(self.tabs)
        self.search = ttk.Frame(self.tabs)
        self.stats = ttk.Frame(self.tabs)

        for tab, name in [
            (self.books, "Books"),
            (self.members, "Members"),
            (self.borrow, "Borrow / Return"),
            (self.search, "Search / Sort"),
            (self.stats, "Statistics")
        ]:
            self.tabs.add(tab, text=name)

        self.book_gui()
        self.member_gui()
        self.borrow_gui()
        self.search_gui()
        self.stats_gui()

    def book_gui(self):
        self.be = []
        for i, text in enumerate(
            ["ID", "Title", "Author", "Year", "Category"]
        ):
            ttk.Label(self.books, text=text).grid(row=0, column=i)
            e = ttk.Entry(self.books, width=15)
            e.grid(row=1, column=i, padx=3)
            self.be.append(e)

        for i, (text, command) in enumerate([
            ("Add", self.add_book),
            ("Edit", self.edit_book),
            ("Delete", self.delete_book)
        ]):
            ttk.Button(
                self.books,
                text=text,
                command=command
            ).grid(row=2, column=i, pady=8)

        self.bt = ttk.Treeview(
            self.books,
            columns=("ID", "Title", "Author", "Year", "Category", "Status"),
            show="headings"
        )

        for c in self.bt["columns"]:
            self.bt.heading(c, text=c)

        self.bt.grid(
            row=3, column=0,
            columnspan=5,
            sticky="nsew"
        )

    def add_book(self):
        try:
            v = [e.get().strip() for e in self.be]
            year = validate_book(*v)
            self.library.add_book(
                Book(v[0], v[1], v[2], year, v[4])
            )
            self.save()
            self.refresh()
            messagebox.showinfo("Success", "Book added.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def edit_book(self):
        try:
            v = [e.get().strip() for e in self.be]
            year = validate_book(*v)
            self.library.edit_book(
                v[0], v[1], v[2], year, v[4]
            )
            self.save()
            self.refresh()
            messagebox.showinfo("Success", "Book updated.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_book(self):
        try:
            self.library.delete_book(self.be[0].get())
            self.save()
            self.refresh()
            messagebox.showinfo("Success", "Book deleted.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def member_gui(self):
        self.me = []

        for i, text in enumerate(
            ["ID", "Name", "Phone", "Email"]
        ):
            ttk.Label(self.members, text=text).grid(row=0, column=i)
            e = ttk.Entry(self.members, width=20)
            e.grid(row=1, column=i, padx=3)
            self.me.append(e)

        ttk.Button(
            self.members,
            text="Add Member",
            command=self.add_member
        ).grid(row=2, column=0, pady=8)

        ttk.Button(
            self.members,
            text="Edit",
            command=self.edit_member
        ).grid(row=2, column=1)

        ttk.Button(
            self.members,
            text="Delete",
            command=self.delete_member
        ).grid(row=2, column=2)

        self.mt = ttk.Treeview(
            self.members,
            columns=("ID", "Name", "Phone", "Email", "Borrowed"),
            show="headings"
        )

        for c in self.mt["columns"]:
            self.mt.heading(c, text=c)

        self.mt.grid(
            row=3, column=0,
            columnspan=4,
            sticky="nsew"
        )

    def add_member(self):
        try:
            v = [e.get().strip() for e in self.me]
            validate_member(*v)
            self.library.add_member(Member(*v))
            self.save()
            self.refresh()
            messagebox.showinfo("Success", "Member added.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def edit_member(self):
        try:
            v = [e.get().strip() for e in self.me]
            validate_member(*v)
            self.library.edit_member(*v)
            self.save()
            self.refresh()
            messagebox.showinfo("Success", "Member updated.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_member(self):
        try:
            self.library.delete_member(self.me[0].get())
            self.save()
            self.refresh()
            messagebox.showinfo("Success", "Member deleted.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def borrow_gui(self):
        ttk.Label(
            self.borrow,
            text="Member ID"
        ).pack(pady=5)

        self.mc = ttk.Combobox(
            self.borrow,
            state="readonly"
        )
        self.mc.pack()

        ttk.Label(
            self.borrow,
            text="Book ID"
        ).pack(pady=5)

        self.bc = ttk.Combobox(
            self.borrow,
            state="readonly"
        )
        self.bc.pack()

        ttk.Button(
            self.borrow,
            text="Borrow",
            command=self.borrow_book
        ).pack(pady=5)

        ttk.Button(
            self.borrow,
            text="Return",
            command=self.return_book
        ).pack()

    def borrow_book(self):
        try:
            self.library.borrow_book(
                self.mc.get(),
                self.bc.get()
            )
            self.save()
            self.refresh()
            messagebox.showinfo("Success", "Book borrowed.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def return_book(self):
        try:
            self.library.return_book(
                self.mc.get(),
                self.bc.get()
            )
            self.save()
            self.refresh()
            messagebox.showinfo("Success", "Book returned.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def search_gui(self):
        self.sc = ttk.Combobox(
            self.search,
            values=["id", "title", "author", "category"],
            state="readonly"
        )
        self.sc.current(0)
        self.sc.pack(side="left", padx=5, pady=10)

        self.se = ttk.Entry(self.search)
        self.se.pack(side="left")

        ttk.Button(
            self.search,
            text="Search",
            command=self.search_book
        ).pack(side="left", padx=5)

        self.sort = ttk.Combobox(
            self.search,
            values=[
                "title",
                "author",
                "year_asc",
                "year_desc",
                "category"
            ],
            state="readonly"
        )
        self.sort.current(0)
        self.sort.pack(side="left")

        ttk.Button(
            self.search,
            text="Sort",
            command=self.sort_books
        ).pack(side="left", padx=5)

        self.st = ttk.Treeview(
            self.search,
            columns=("ID", "Title", "Author", "Year", "Category"),
            show="headings"
        )

        for c in self.st["columns"]:
            self.st.heading(c, text=c)

        self.st.pack(fill="both", expand=True)

    def show(self, books):
        self.st.delete(*self.st.get_children())

        for b in books:
            self.st.insert(
                "",
                "end",
                values=(
                    b.book_id,
                    b.title,
                    b.author,
                    b.year,
                    b.category
                )
            )

    def search_book(self):
        self.show(
            self.library.search_book(
                self.se.get(),
                self.sc.get()
            )
        )

    def sort_books(self):
        self.show(
            self.library.sort_books(
                self.sort.get()
            )
        )

    def stats_gui(self):
        self.stat = ttk.Label(
            self.stats,
            font=("Arial", 16)
        )
        self.stat.pack(pady=50)

    def refresh(self):
        self.bt.delete(*self.bt.get_children())
        for b in self.library.books:
            self.bt.insert(
                "",
                "end",
                values=(
                    b.book_id,
                    b.title,
                    b.author,
                    b.year,
                    b.category,
                    "Available" if b.availability else "Borrowed"
                )
            )

        self.mt.delete(*self.mt.get_children())
        for m in self.library.members:
            self.mt.insert(
                "",
                "end",
                values=(
                    m.member_id,
                    m.name,
                    m.phone,
                    m.email,
                    ", ".join(m.borrowed_books)
                )
            )

        self.mc["values"] = [
            m.member_id for m in self.library.members
        ]

        self.bc["values"] = [
            b.book_id for b in self.library.books
        ]

        s = self.library.get_statistics()

        self.stat.config(
            text=(
                f"Total Books: {s['total_books']}\n"
                f"Available Books: {s['available_books']}\n"
                f"Borrowed Books: {s['borrowed_books']}\n"
                f"Total Members: {s['total_members']}\n"
                f"Most Common Category: "
                f"{s['most_common_category']}"
            )
        )

    def save(self):
        self.files.save_books(self.library.books)
        self.files.save_members(self.library.members)


if __name__ == "__main__":
    root = tk.Tk()
    LibraryGUI(root)
    root.mainloop()
