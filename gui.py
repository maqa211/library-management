import tkinter as tk
from tkinter import ttk, messagebox
from models import Book, Member
from library import Library

library = Library()

root = tk.Tk()
root.title("Library Management")
root.geometry("1050x680")
root.configure(bg="lightblue")

tk.Label(root, text="Library Management", font=("Arial", 24, "bold"),
         bg="lightblue").pack(pady=15)

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True, padx=15, pady=10)

books = tk.Frame(tabs, bg="lightblue")
members = tk.Frame(tabs, bg="lightblue")
borrow = tk.Frame(tabs, bg="lightblue")
stats = tk.Frame(tabs, bg="lightblue")

tabs.add(books, text="Books")
tabs.add(members, text="Members")
tabs.add(borrow, text="Borrow / Return")
tabs.add(stats, text="Statistics")

be = []

for i, x in enumerate(["ID", "Title", "Author", "Year", "Category"]):
    tk.Label(books, text=x, bg="lightblue",
             font=("Arial", 10, "bold")).grid(
             row=0, column=i, padx=8, pady=5)

    e = tk.Entry(books, width=18)
    e.grid(row=1, column=i, padx=8, pady=5)
    be.append(e)

bt = ttk.Treeview(
    books,
    columns=["ID", "Title", "Author", "Year", "Category", "Status"],
    show="headings",
    height=15
)

for x in ["ID", "Title", "Author", "Year", "Category", "Status"]:
    bt.heading(x, text=x)
    bt.column(x, width=150)

bt.grid(row=4, column=0, columnspan=5, padx=15, pady=15)


def show_books(data=None):
    bt.delete(*bt.get_children())

    for b in library.get_books() if data is None else data:
        bt.insert("", "end", values=(
            b["book_id"], b["title"], b["author"], b["year"],
            b["category"],
            "Available" if b["availability"] else "Borrowed"
        ))


def add_book():
    try:
        if not all(x.get().strip() for x in be):
            raise ValueError("All fields are required")

        library.add_book(Book(
            be[0].get(), be[1].get(), be[2].get(),
            int(be[3].get()), be[4].get()
        ))

        show_books()
        messagebox.showinfo("Success", "Book added")

    except ValueError as e:
        messagebox.showerror("Error", str(e))


def edit_book():
    try:
        library.edit_book(
            be[0].get(), be[1].get(), be[2].get(),
            int(be[3].get()), be[4].get()
        )

        show_books()
        messagebox.showinfo("Success", "Book updated")

    except ValueError as e:
        messagebox.showerror("Error", str(e))


def delete_book():
    try:
        library.delete_book(be[0].get())
        show_books()
        messagebox.showinfo("Success", "Book deleted")

    except ValueError as e:
        messagebox.showerror("Error", str(e))


tk.Button(books, text="Add", width=12, command=add_book).grid(
    row=2, column=0, padx=5, pady=10)

tk.Button(books, text="Edit", width=12, command=edit_book).grid(
    row=2, column=1, padx=5, pady=10)

tk.Button(books, text="Delete", width=12, command=delete_book).grid(
    row=2, column=2, padx=5, pady=10)

search = tk.Entry(books, width=20)
search.grid(row=2, column=3, padx=5)


def search_book():
    try:
        show_books(library.search_books("Title", search.get()))

    except ValueError as e:
        messagebox.showerror("Error", str(e))


tk.Button(books, text="Search", width=12, command=search_book).grid(
    row=2, column=4, padx=5)

sort = ttk.Combobox(
    books,
    values=["Title A-Z", "Author A-Z", "Year Ascending",
            "Year Descending", "Category A-Z"],
    state="readonly",
    width=18
)

sort.grid(row=3, column=3, pady=5)

tk.Button(
    books,
    text="Sort",
    width=12,
    command=lambda: show_books(library.sort_books(sort.get()))
).grid(row=3, column=4, padx=5)

me = []

for i, x in enumerate(["ID", "Name", "Phone", "Email"]):
    tk.Label(members, text=x, bg="lightblue",
             font=("Arial", 10, "bold")).grid(
             row=0, column=i, padx=10, pady=5)

    e = tk.Entry(members, width=22)
    e.grid(row=1, column=i, padx=10, pady=5)
    me.append(e)

mt = ttk.Treeview(
    members,
    columns=["ID", "Name", "Phone", "Email", "Borrowed Books"],
    show="headings",
    height=15
)

for x in ["ID", "Name", "Phone", "Email", "Borrowed Books"]:
    mt.heading(x, text=x)
    mt.column(x, width=170)

mt.grid(row=4, column=0, columnspan=5, padx=15, pady=15)


def show_members():
    mt.delete(*mt.get_children())

    for m in library.get_members():
        borrowed = ", ".join(m["borrowed_books"]) if m["borrowed_books"] else "-"

        mt.insert("", "end", values=(
            m["member_id"], m["name"], m["phone"],
            m["email"], borrowed
        ))


def add_member():
    try:
        if not all(x.get().strip() for x in me):
            raise ValueError("All fields are required")

        library.add_member(Member(
            me[0].get(), me[1].get(), me[2].get(), me[3].get()
        ))

        show_members()
        messagebox.showinfo("Success", "Member added")

    except ValueError as e:
        messagebox.showerror("Error", str(e))


def edit_member():
    try:
        library.edit_member(
            me[0].get(), me[1].get(), me[2].get(), me[3].get()
        )

        show_members()
        messagebox.showinfo("Success", "Member updated")

    except ValueError as e:
        messagebox.showerror("Error", str(e))


def delete_member():
    try:
        library.delete_member(me[0].get())
        show_members()
        messagebox.showinfo("Success", "Member deleted")

    except ValueError as e:
        messagebox.showerror("Error", str(e))


tk.Button(members, text="Add", width=12, command=add_member).grid(
    row=2, column=0, padx=5, pady=10)

tk.Button(members, text="Edit", width=12, command=edit_member).grid(
    row=2, column=1, padx=5, pady=10)

tk.Button(members, text="Delete", width=12, command=delete_member).grid(
    row=2, column=2, padx=5, pady=10)

tk.Label(borrow, text="Member ID", bg="lightblue",
         font=("Arial", 10, "bold")).grid(
         row=0, column=0, padx=15, pady=15)

mid = tk.Entry(borrow, width=25)
mid.grid(row=0, column=1)

tk.Label(borrow, text="Book ID", bg="lightblue",
         font=("Arial", 10, "bold")).grid(
         row=1, column=0, padx=15, pady=15)

bid = tk.Entry(borrow, width=25)
bid.grid(row=1, column=1)


def borrow_book():
    try:
        library.borrow_book(mid.get(), bid.get())
        show_books()
        show_members()
        messagebox.showinfo("Success", "Book borrowed")

    except ValueError as e:
        messagebox.showerror("Error", str(e))


def return_book():
    try:
        library.return_book(mid.get(), bid.get())
        show_books()
        show_members()
        messagebox.showinfo("Success", "Book returned")

    except ValueError as e:
        messagebox.showerror("Error", str(e))


tk.Button(borrow, text="Borrow Book", width=15,
          command=borrow_book).grid(
          row=2, column=0, padx=10, pady=15)

tk.Button(borrow, text="Return Book", width=15,
          command=return_book).grid(
          row=2, column=1, padx=10, pady=15)


def statistics():
    s = library.get_statistics()

    messagebox.showinfo(
        "Statistics",
        f"Total books: {s['total_books']}\n"
        f"Available: {s['available_books']}\n"
        f"Borrowed: {s['borrowed_books']}\n"
        f"Members: {s['total_members']}\n"
        f"Top category: {s['most_common_category']}"
    )


tk.Button(stats, text="Show Statistics", width=18,
          command=statistics).pack(pady=50)

show_books()
show_members()

root.mainloop()
