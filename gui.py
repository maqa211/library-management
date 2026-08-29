import tkinter as tk
from tkinter import ttk, messagebox
from models import Book, Member
from library import Library

library = Library()
window = tk.Tk()
window.title("Library Management")
window.geometry("1050x680")
window.configure(bg="lightblue")

dark = False

def toggle_mode():
    global dark
    dark = not dark
    bg = "#222222" if dark else "lightblue"
    fg = "white" if dark else "black"
    window.configure(bg=bg)

    for frame in [books, members, borrow, stats]:
        frame.configure(bg=bg)
        for widget in frame.children.values():
            if isinstance(widget, tk.Label):
                widget.configure(bg=bg, fg=fg)

    mode_button.config(text="Light Mode" if dark else "Dark Mode")

tk.Label(window,text="Library Management",font=("Arial", 24, "bold"), bg="lightblue").pack(pady=15)

mode_button = tk.Button(window,text="Dark Mode",command=toggle_mode)
mode_button.pack(anchor="ne",padx=10,pady=10)

tabs = ttk.Notebook(window)
tabs.pack(fill="both", expand=True, padx=15, pady=10)

books = tk.Frame(tabs, bg="lightblue")
members = tk.Frame(tabs, bg="lightblue")
borrow = tk.Frame(tabs, bg="lightblue")
stats = tk.Frame(tabs, bg="lightblue")

for frame, name in [(books, "Books"), (members, "Members"),
                    (borrow, "Borrow / Return"), (stats, "Statistics")]:
    tabs.add(frame, text=name)

def fields(frame, names, width):
    result = []
    for i, name in enumerate(names):
        tk.Label(frame, text=name, bg="lightblue",
                 font=("Arial", 10, "bold")).grid(row=0, column=i, padx=8)
        entry = tk.Entry(frame, width=width)
        entry.grid(row=1, column=i, padx=8, pady=5)
        result.append(entry)
    return result

entries = fields(books, ["ID", "Title", "Author", "Year", "Category"], 18)
member_entries = fields(members, ["ID", "Name", "Phone", "Email"], 22)

def error_action(action):
    try:
        action()
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def show_books(data=None):
    book_list.delete(*book_list.get_children())
    for b in library.get_books() if data is None else data:
        book_list.insert("", "end", values=(
            b["book_id"], b["title"], b["author"], b["year"],
            b["category"], "Available" if b["availability"] else "Borrowed"))

def add_book():
    if not all(e.get().strip() for e in entries):
        raise ValueError("All fields are required")
    library.add_book(Book(entries[0].get(), entries[1].get(),
                          entries[2].get(), int(entries[3].get()),
                          entries[4].get()))
    show_books()
    messagebox.showinfo("Success", "Book added")

def edit_book():
    library.edit_book(entries[0].get(), entries[1].get(),
                      entries[2].get(), int(entries[3].get()),
                      entries[4].get())
    show_books()
    messagebox.showinfo("Success", "Book updated")

def delete_book():
    library.delete_book(entries[0].get())
    show_books()
    messagebox.showinfo("Success", "Book deleted")

def buttons(frame, names, commands, row=2):
    for i, (name, command) in enumerate(zip(names, commands)):
        tk.Button(frame, text=name, width=12, command=command).grid(
            row=row, column=i, padx=5, pady=10)

buttons(books, ["Add", "Edit", "Delete"],
        [lambda: error_action(add_book),
         lambda: error_action(edit_book),
         lambda: error_action(delete_book)])

tk.Label(books, text="Search:", bg="lightblue",
         font=("Arial", 10, "bold")).grid(row=3, column=0)

search = tk.Entry(books, width=20)
search.grid(row=3, column=1)

def search_book():
    value = search.get().strip().lower()
    if not value:
        show_books()
        return
    found = [b for b in library.get_books()
             if value in str(b["book_id"]).lower()
             or value in b["title"].lower()]
    show_books(found)

tk.Button(books, text="Search", width=12,
          command=search_book).grid(row=3, column=2)

tk.Label(books, text="Sort:", bg="lightblue",
         font=("Arial", 10, "bold")).grid(row=3, column=3)

sort = ttk.Combobox(
    books,
    values=["Title A-Z", "Author A-Z", "Year Ascending",
            "Year Descending", "Category A-Z"],
    state="readonly", width=18)
sort.grid(row=3, column=4)

tk.Button(
    books, text="Sort", width=12,
    command=lambda: error_action(
        lambda: show_books(library.sort_books(sort.get()))
    )
).grid(row=3, column=5)

book_list = ttk.Treeview(
    books,
    columns=["ID", "Title", "Author", "Year", "Category", "Status"],
    show="headings", height=15)

for x in ["ID", "Title", "Author", "Year", "Category", "Status"]:
    book_list.heading(x, text=x)
    book_list.column(x, width=150)

book_list.grid(row=4, column=0, columnspan=6, padx=15, pady=15)

def show_members():
    member_list.delete(*member_list.get_children())
    for m in library.get_members():
        borrowed = ", ".join(m["borrowed_books"]) if m["borrowed_books"] else "-"
        member_list.insert("", "end", values=(
            m["member_id"], m["name"], m["phone"], m["email"], borrowed))

def add_member():
    if not all(e.get().strip() for e in member_entries):
        raise ValueError("All fields are required")
    library.add_member(Member(
        member_entries[0].get(), member_entries[1].get(),
        member_entries[2].get(), member_entries[3].get()))
    show_members()
    messagebox.showinfo("Success", "Member added")

def edit_member():
    library.edit_member(
        member_entries[0].get(), member_entries[1].get(),
        member_entries[2].get(), member_entries[3].get())
    show_members()
    messagebox.showinfo("Success", "Member updated")

def delete_member():
    library.delete_member(member_entries[0].get())
    show_members()
    messagebox.showinfo("Success", "Member deleted")

buttons(members, ["Add", "Edit", "Delete"],
        [lambda: error_action(add_member),
         lambda: error_action(edit_member),
         lambda: error_action(delete_member)])

member_list = ttk.Treeview(
    members,
    columns=["ID", "Name", "Phone", "Email", "Borrowed Books"],
    show="headings", height=15)

for x in ["ID", "Name", "Phone", "Email", "Borrowed Books"]:
    member_list.heading(x, text=x)
    member_list.column(x, width=170)

member_list.grid(row=4, column=0, columnspan=5, padx=15, pady=15)

def entry_label(frame, text, row):
    tk.Label(frame, text=text, bg="lightblue",
             font=("Arial", 10, "bold")).grid(
                 row=row, column=0, padx=15, pady=15)

entry_label(borrow, "Member ID", 0)
member_id = tk.Entry(borrow, width=25)
member_id.grid(row=0, column=1)

entry_label(borrow, "Book ID", 1)
book_id = tk.Entry(borrow, width=25)
book_id.grid(row=1, column=1)

def borrow_book():
    library.borrow_book(member_id.get(), book_id.get())
    show_books()
    show_members()
    messagebox.showinfo("Success", "Book borrowed")

def return_book():
    library.return_book(member_id.get(), book_id.get())
    show_books()
    show_members()
    messagebox.showinfo("Success", "Book returned")

buttons(borrow, ["Borrow Book", "Return Book"],
        [lambda: error_action(borrow_book),
         lambda: error_action(return_book)])

def statistics():
    s = library.get_statistics()
    messagebox.showinfo(
        "Statistics",
        f"Total books: {s['total_books']}\n"
        f"Available: {s['available_books']}\n"
        f"Borrowed: {s['borrowed_books']}\n"
        f"Members: {s['total_members']}\n"
        f"Top category: {s['most_common_category']}")

tk.Button(stats, text="Show Statistics", width=18,
          command=statistics).pack(pady=50)

show_books()
show_members()
window.mainloop()
