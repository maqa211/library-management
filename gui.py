import tkinter as tk
from tkinter import ttk, messagebox
from models import Book, Member
from library import Library

library = Library()

root = tk.Tk()
root.title("Library Management")
root.geometry("1000x650")
root.configure(bg="lightblue")

tk.Label(root, text="Library Management", font=("Arial", 22, "bold"),
         bg="lightblue").pack(pady=10)

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True, padx=10, pady=5)

books_tab = tk.Frame(tabs, bg="lightblue")
members_tab = tk.Frame(tabs, bg="lightblue")
borrow_tab = tk.Frame(tabs, bg="lightblue")
stats_tab = tk.Frame(tabs, bg="lightblue")

tabs.add(books_tab, text="Books")
tabs.add(members_tab, text="Members")
tabs.add(borrow_tab, text="Borrow / Return")
tabs.add(stats_tab, text="Statistics")

book_fields = ["ID", "Title", "Author", "Year", "Category"]
book_entries = []

for i, field in enumerate(book_fields):
    tk.Label(books_tab, text=field, bg="lightblue").grid(row=0, column=i)
    e = tk.Entry(books_tab, width=18)
    e.grid(row=1, column=i, padx=3)
    book_entries.append(e)

book_tree = ttk.Treeview(books_tab, columns=book_fields, show="headings", height=15)
for field in book_fields:
    book_tree.heading(field, text=field)
    book_tree.column(field, width=150)
book_tree.grid(row=3, column=0, columnspan=5, pady=10)

def show_books(books=None):
    book_tree.delete(*book_tree.get_children())
    for b in books or library.get_books():
        book_tree.insert("", "end", values=(
            b["book_id"], b["title"], b["author"], b["year"],
            b["category"], "Available" if b["availability"] else "Borrowed"
        ))

def add_book():
    try:
        e = book_entries
        if not all(x.get().strip() for x in e):
            raise ValueError("All fields are required.")
        year = int(e[3].get())
        library.add_book(Book(e[0].get(), e[1].get(), e[2].get(),
                              year, e[4].get()))
        show_books()
        messagebox.showinfo("Success", "Book added.")
    except ValueError as error:
        messagebox.showerror("Error", str(error))

tk.Button(books_tab, text="Add Book", command=add_book).grid(row=2, column=0)

search = tk.Entry(books_tab, width=20)
search.grid(row=2, column=1)

def search_books():
    try:
        result = library.search_books("Title", search.get())
        show_books(result)
    except ValueError as error:
        messagebox.showerror("Error", str(error))

tk.Button(books_tab, text="Search", command=search_books).grid(row=2, column=2)

sort_box = ttk.Combobox(books_tab, values=["Title A-Z", "Author A-Z",
    "Year Ascending", "Year Descending", "Category A-Z"], state="readonly")
sort_box.grid(row=2, column=3)

def sort_books():
    show_books(library.sort_books(sort_box.get()))

tk.Button(books_tab, text="Sort", command=sort_books).grid(row=2, column=4)

member_fields = ["ID", "Name", "Phone", "Email"]
member_entries = []

for i, field in enumerate(member_fields):
    tk.Label(members_tab, text=field, bg="lightblue").grid(row=0, column=i)
    e = tk.Entry(members_tab, width=22)
    e.grid(row=1, column=i)
    member_entries.append(e)

member_tree = ttk.Treeview(members_tab, columns=member_fields, show="headings")
for field in member_fields:
    member_tree.heading(field, text=field)
    member_tree.column(field, width=180)
member_tree.grid(row=3, column=0, columnspan=4, pady=10)

def show_members():
    member_tree.delete(*member_tree.get_children())
    for m in library.get_members():
        member_tree.insert("", "end", values=(
            m["member_id"], m["name"], m["phone"], m["email"]))

def add_member():
    try:
        e = member_entries
        if not all(x.get().strip() for x in e):
            raise ValueError("All fields are required.")
        library.add_member(Member(e[0].get(), e[1].get(), e[2].get(), e[3].get()))
        show_members()
        messagebox.showinfo("Success", "Member added.")
    except ValueError as error:
        messagebox.showerror("Error", str(error))

tk.Button(members_tab, text="Add Member", command=add_member).grid(row=2, column=0)

tk.Label(borrow_tab, text="Member ID", bg="lightblue").grid(row=0, column=0)
member_id = tk.Entry(borrow_tab)
member_id.grid(row=0, column=1)

tk.Label(borrow_tab, text="Book ID", bg="lightblue").grid(row=1, column=0)
book_id = tk.Entry(borrow_tab)
book_id.grid(row=1, column=1)

def borrow():
    try:
        library.borrow_book(member_id.get(), book_id.get())
        show_books()
        messagebox.showinfo("Success", "Book borrowed.")
    except ValueError as error:
        messagebox.showerror("Error", str(error))

def return_book():
    try:
        library.return_book(member_id.get(), book_id.get())
        show_books()
        messagebox.showinfo("Success", "Book returned.")
    except ValueError as error:
        messagebox.showerror("Error", str(error))

tk.Button(borrow_tab, text="Borrow Book", command=borrow).grid(row=2, column=0)
tk.Button(borrow_tab, text="Return Book", command=return_book).grid(row=2, column=1)

def statistics():
    s = library.get_statistics()
    text = f"Total books: {s['total_books']}\nAvailable books: {s['available_books']}\n"
    text += f"Borrowed books: {s['borrowed_books']}\nTotal members: {s['total_members']}\n"
    text += f"Most common category: {s['most_common_category']}"
    messagebox.showinfo("Statistics", text)

tk.Button(stats_tab, text="Show Statistics", command=statistics).pack(pady=40)

show_books()
show_members()
root.mainloop()
