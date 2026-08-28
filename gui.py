import tkinter as tk
from tkinter import ttk, messagebox
from models import Book, Member
from library import Library

library = Library()

window = tk.Tk()
window.title("Library Management")
window.geometry("1050x680")
window.configure(bg="lightblue")

tk.Label(window, text="Library Management",
         font=("Arial", 24, "bold"),
         bg="lightblue").pack(pady=15)

tabs = ttk.Notebook(window)
tabs.pack(fill="both", expand=True, padx=15, pady=10)

books = tk.Frame(tabs, bg="lightblue")
members = tk.Frame(tabs, bg="lightblue")
borrow = tk.Frame(tabs, bg="lightblue")
stats = tk.Frame(tabs, bg="lightblue")

tabs.add(books, text="Books")
tabs.add(members, text="Members")
tabs.add(borrow, text="Borrow / Return")
tabs.add(stats, text="Statistics")

entries = []

for i, x in enumerate(["ID", "Title", "Author", "Year", "Category"]):
    tk.Label(books, text=x, bg="lightblue",
             font=("Arial", 10, "bold")).grid(
             row=0, column=i, padx=8, pady=5)

    e = tk.Entry(books, width=18)
    e.grid(row=1, column=i, padx=8, pady=5)
    entries.append(e)


def show_books(data=None):
    book_tree.delete(*book_tree.get_children())

    for book in library.get_books() if data is None else data:
        book_tree.insert("", "end", values=(
            book["book_id"],
            book["title"],
            book["author"],
            book["year"],
            book["category"],
            "Available" if book["availability"] else "Borrowed"
        ))


def add_book():
    try:
        if not all(x.get().strip() for x in entries):
            raise ValueError("All fields are required")

        library.add_book(Book(
            entries[0].get(),
            entries[1].get(),
            entries[2].get(),
            int(entries[3].get()),
            entries[4].get()
        ))

        show_books()
        messagebox.showinfo("Success", "Book added")

    except ValueError as error:
        messagebox.showerror("Error", str(error))


def edit_book():
    try:
        library.edit_book(
            entries[0].get(),
            entries[1].get(),
            entries[2].get(),
            int(entries[3].get()),
            entries[4].get()
        )

        show_books()
        messagebox.showinfo("Success", "Book updated")

    except ValueError as error:
        messagebox.showerror("Error", str(error))


def delete_book():
    try:
        library.delete_book(entries[0].get())
        show_books()
        messagebox.showinfo("Success", "Book deleted")

    except ValueError as error:
        messagebox.showerror("Error", str(error))


tk.Button(books, text="Add", width=12,
          command=add_book).grid(row=2, column=0, padx=5, pady=10)

tk.Button(books, text="Edit", width=12,
          command=edit_book).grid(row=2, column=1, padx=5, pady=10)

tk.Button(books, text="Delete", width=12,
          command=delete_book).grid(row=2, column=2, padx=5, pady=10)

tk.Label(books, text="Search:", bg="lightblue",
         font=("Arial", 10, "bold")).grid(
         row=3, column=0, padx=5, pady=10)

search = tk.Entry(books, width=20)
search.grid(row=3, column=1, padx=5)


def search_book():
    try:
        show_books(library.search_books("Title", search.get()))

    except ValueError as error:
        messagebox.showerror("Error", str(error))


tk.Button(books, text="Search", width=12,
          command=search_book).grid(row=3, column=2, padx=5)

tk.Label(books, text="Sort:", bg="lightblue",
         font=("Arial", 10, "bold")).grid(
         row=3, column=3, padx=5)

sort = ttk.Combobox(
    books,
    values=[
        "Title A-Z",
        "Author A-Z",
        "Year Ascending",
        "Year Descending",
        "Category A-Z"
    ],
    state="readonly",
    width=18
)
sort.grid(row=3, column=4, padx=5)


def sort_books():
    try:
        show_books(library.sort_books(sort.get()))

    except ValueError as error:
        messagebox.showerror("Error", str(error))


tk.Button(books, text="Sort", width=12,
          command=sort_books).grid(row=3, column=5, padx=5)

book_tree = ttk.Treeview(
    books,
    columns=["ID", "Title", "Author", "Year", "Category", "Status"],
    show="headings",
    height=15
)

for x in ["ID", "Title", "Author", "Year", "Category", "Status"]:
    book_tree.heading(x, text=x)
    book_tree.column(x, width=150)

book_tree.grid(row=4, column=0, columnspan=6, padx=15, pady=15)

member_entries = []

for i, x in enumerate(["ID", "Name", "Phone", "Email"]):
    tk.Label(members, text=x, bg="lightblue",
             font=("Arial", 10, "bold")).grid(
             row=0, column=i, padx=10, pady=5)

    e = tk.Entry(members, width=22)
    e.grid(row=1, column=i, padx=10, pady=5)
    member_entries.append(e)


def show_members():
    member_tree.delete(*member_tree.get_children())

    for member in library.get_members():
        borrowed = ", ".join(
            member["borrowed_books"]
        ) if member["borrowed_books"] else "-"

        member_tree.insert("", "end", values=(
            member["member_id"],
            member["name"],
            member["phone"],
            member["email"],
            borrowed
        ))


def add_member():
    try:
        if not all(x.get().strip() for x in member_entries):
            raise ValueError("All fields are required")

        library.add_member(Member(
            member_entries[0].get(),
            member_entries[1].get(),
            member_entries[2].get(),
            member_entries[3].get()
        ))

        show_members()
        messagebox.showinfo("Success", "Member added")

    except ValueError as error:
        messagebox.showerror("Error", str(error))


def edit_member():
    try:
        library.edit_member(
            member_entries[0].get(),
            member_entries[1].get(),
            member_entries[2].get(),
            member_entries[3].get()
        )

        show_members()
        messagebox.showinfo("Success", "Member updated")

    except ValueError as error:
        messagebox.showerror("Error", str(error))


def delete_member():
    try:
        library.delete_member(member_entries[0].get())
        show_members()
        messagebox.showinfo("Success", "Member deleted")

    except ValueError as error:
        messagebox.showerror("Error", str(error))


tk.Button(members, text="Add", width=12,
          command=add_member).grid(row=2, column=0, padx=5, pady=10)

tk.Button(members, text="Edit", width=12,
          command=edit_member).grid(row=2, column=1, padx=5, pady=10)

tk.Button(members, text="Delete", width=12,
          command=delete_member).grid(row=2, column=2, padx=5, pady=10)

tk.Label(borrow, text="Member ID", bg="lightblue",
         font=("Arial", 10, "bold")).grid(
         row=0, column=0, padx=15, pady=15)

member_id = tk.Entry(borrow, width=25)
member_id.grid(row=0, column=1)

tk.Label(borrow, text="Book ID", bg="lightblue",
         font=("Arial", 10, "bold")).grid(
         row=1, column=0, padx=15, pady=15)

book_id = tk.Entry(borrow, width=25)
book_id.grid(row=1, column=1)


def borrow_book():
    try:
        library.borrow_book(member_id.get(), book_id.get())
        show_books()
        show_members()
        messagebox.showinfo("Success", "Book borrowed")

    except ValueError as error:
        messagebox.showerror("Error", str(error))


def return_book():
    try:
        library.return_book(member_id.get(), book_id.get())
        show_books()
        show_members()
        messagebox.showinfo("Success", "Book returned")

    except ValueError as error:
        messagebox.showerror("Error", str(error))


tk.Button(borrow, text="Borrow Book", width=15,
          command=borrow_book).grid(
          row=2, column=0, padx=10, pady=15)

tk.Button(borrow, text="Return Book", width=15,
          command=return_book).grid(
          row=2, column=1, padx=10, pady=15)


def statistics():
    stats_data = library.get_statistics()

    messagebox.showinfo(
        "Statistics",
        f"Total books: {stats_data['total_books']}\n"
        f"Available: {stats_data['available_books']}\n"
        f"Borrowed: {stats_data['borrowed_books']}\n"
        f"Members: {stats_data['total_members']}\n"
        f"Top category: {stats_data['most_common_category']}"
    )


tk.Button(stats, text="Show Statistics", width=18,
          command=statistics).pack(pady=50)

show_books()
show_members()

window.mainloop()
