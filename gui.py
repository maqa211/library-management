import tkinter as tk
from tkinter import ttk, messagebox
from models import Book, Member
from library import Library

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("850x600")

        # Pəncərənin fon rəngini açıq mavi edirik
        self.root.configure(bg="#E0F2FE")

        # Yuxarıda ortada başlığın əlavə edilməsi
        title_label = tk.Label(
            self.root, 
            text="Library Management", 
            font=("Arial", 20, "bold"), 
            bg="#E0F2FE", 
            fg="#0F172A"
        )
        title_label.pack(pady=10)

        self.library = Library()

        # Style ayarları (Tabların arxa fonunun da uyğunlaşması üçün)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TFrame", background="#E0F2FE")
        style.configure("TLabelframe", background="#E0F2FE")
        style.configure("TLabelframe.Label", background="#E0F2FE", font=("Arial", 10, "bold"))
        style.configure("TLabel", background="#E0F2FE", font=("Arial", 10))

        # Tablar (Notebook)
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=5)

        self.tab_books = ttk.Frame(self.tabs)
        self.tab_members = ttk.Frame(self.tabs)
        self.tab_borrow = ttk.Frame(self.tabs)
        self.tab_search = ttk.Frame(self.tabs)
        self.tab_stats = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_books, text="Books")
        self.tabs.add(self.tab_members, text="Members")
        self.tabs.add(self.tab_borrow, text="Borrow / Return")
        self.tabs.add(self.tab_search, text="Search & Sort")
        self.tabs.add(self.tab_stats, text="Statistics")

        self.setup_books_page()
        self.setup_members_page()
        self.setup_borrow_page()
        self.setup_search_page()
        self.setup_stats_page()

    # --- 1. BOOKS PAGE ---
    def setup_books_page(self):
        frame = ttk.LabelFrame(self.tab_books, text="Book Details")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_b_id = ttk.Entry(frame)
        self.entry_b_id.grid(row=0, column=1)

        ttk.Label(frame, text="Title:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_b_title = ttk.Entry(frame)
        self.entry_b_title.grid(row=0, column=3)

        ttk.Label(frame, text="Author:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_b_author = ttk.Entry(frame)
        self.entry_b_author.grid(row=1, column=1)

        ttk.Label(frame, text="Year:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_b_year = ttk.Entry(frame)
        self.entry_b_year.grid(row=1, column=3)

        ttk.Label(frame, text="Category:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_b_cat = ttk.Entry(frame)
        self.entry_b_cat.grid(row=2, column=1)

        btn_frame = ttk.Frame(self.tab_books)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Add Book", command=self.add_book).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Book", command=self.delete_book).pack(side="left", padx=5)

        self.tree_books = ttk.Treeview(self.tab_books, columns=("ID", "Title", "Author", "Year", "Category", "Status"), show="headings")
        for col in ("ID", "Title", "Author", "Year", "Category", "Status"):
            self.tree_books.heading(col, text=col)
            self.tree_books.column(col, width=120)
        self.tree_books.pack(fill="both", expand=True, padx=10, pady=5)

        self.refresh_books_table(self.library.books)

    def refresh_books_table(self, book_list):
        for item in self.tree_books.get_children():
            self.tree_books.delete(item)
        for b in book_list:
            status = "Available" if b.is_available else "Borrowed"
            self.tree_books.insert("", "end", values=(b.id, b.title, b.author, b.year, b.category, status))

    def add_book(self):
        try:
            self.library.add_book(
                self.entry_b_id.get(),
                self.entry_b_title.get(),
                self.entry_b_author.get(),
                self.entry_b_year.get(),
                self.entry_b_cat.get()
            )
            messagebox.showinfo("Success", "Book added successfully!")
            self.refresh_books_table(self.library.books)
            self.update_borrow_combos()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_book(self):
        selected = self.tree_books.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book from table!")
            return
        book_id = self.tree_books.item(selected[0])['values'][0]
        self.library.delete_book(book_id)
        self.refresh_books_table(self.library.books)
        self.update_borrow_combos()
        messagebox.showinfo("Success", "Book deleted successfully!")

    # --- 2. MEMBERS PAGE ---
    def setup_members_page(self):
        frame = ttk.LabelFrame(self.tab_members, text="Member Details")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Member ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_m_id = ttk.Entry(frame)
        self.entry_m_id.grid(row=0, column=1)

        ttk.Label(frame, text="Name:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_m_name = ttk.Entry(frame)
        self.entry_m_name.grid(row=0, column=3)

        ttk.Label(frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_m_phone = ttk.Entry(frame)
        self.entry_m_phone.grid(row=1, column=1)

        ttk.Label(frame, text="Email:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_m_email = ttk.Entry(frame)
        self.entry_m_email.grid(row=1, column=3)

        btn_frame = ttk.Frame(self.tab_members)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Add Member", command=self.add_member).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Member", command=self.delete_member).pack(side="left", padx=5)

        self.tree_members = ttk.Treeview(self.tab_members, columns=("ID", "Name", "Phone", "Email", "Borrowed Books"), show="headings")
        for col in ("ID", "Name", "Phone", "Email", "Borrowed Books"):
            self.tree_members.heading(col, text=col)
            self.tree_members.column(col, width=140)
        self.tree_members.pack(fill="both", expand=True, padx=10, pady=5)

        self.refresh_members_table()

    def refresh_members_table(self):
        for item in self.tree_members.get_children():
            self.tree_members.delete(item)
        for m in self.library.members:
            borrowed_str = ", ".join(m.borrowed_books) if m.borrowed_books else "None"
            self.tree_members.insert("", "end", values=(m.id, m.name, m.phone, m.email, borrowed_str))

    def add_member(self):
        try:
            self.library.add_member(
                self.entry_m_id.get(),
                self.entry_m_name.get(),
                self.entry_m_phone.get(),
                self.entry_m_email.get()
            )
            messagebox.showinfo("Success", "Member added successfully!")
            self.refresh_members_table()
            self.update_borrow_combos()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_member(self):
        selected = self.tree_members.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member from table!")
            return
        member_id = self.tree_members.item(selected[0])['values'][0]
        self.library.delete_member(member_id)
        self.refresh_members_table()
        self.update_borrow_combos()
        messagebox.showinfo("Success", "Member deleted successfully!")

    # --- 3. BORROW / RETURN PAGE ---
    def setup_borrow_page(self):
        frame = ttk.LabelFrame(self.tab_borrow, text="Borrow or Return Book")
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="Select Member ID:").grid(row=0, column=0, padx=10, pady=10)
        self.combo_members = ttk.Combobox(frame, state="readonly")
        self.combo_members.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Select Book ID:").grid(row=1, column=0, padx=10, pady=10)
        self.combo_books = ttk.Combobox(frame, state="readonly")
        self.combo_books.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(frame, text="Borrow Book", command=self.borrow_book).grid(row=2, column=0, pady=15)
        ttk.Button(frame, text="Return Book", command=self.return_book).grid(row=2, column=1, pady=15)

        self.update_borrow_combos()

    def update_borrow_combos(self):
        self.combo_members["values"] = [m.id for m in self.library.members]
        self.combo_books["values"] = [b.id for b in self.library.books]

    def borrow_book(self):
        try:
            self.library.borrow_book(self.combo_members.get(), self.combo_books.get())
            messagebox.showinfo("Success", "Book borrowed successfully!")
            self.refresh_books_table(self.library.books)
            self.refresh_members_table()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def return_book(self):
        try:
            self.library.return_book(self.combo_members.get(), self.combo_books.get())
            messagebox.showinfo("Success", "Book returned successfully!")
            self.refresh_books_table(self.library.books)
            self.refresh_members_table()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # --- 4. SEARCH & SORT PAGE ---
    def setup_search_page(self):
        top_frame = ttk.Frame(self.tab_search)
        top_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(top_frame, text="Search Text:").pack(side="left", padx=5)
        self.entry_search = ttk.Entry(top_frame)
        self.entry_search.pack(side="left", padx=5)

        ttk.Button(top_frame, text="Search", command=self.search_books).pack(side="left", padx=5)

        ttk.Label(top_frame, text="Sort By:").pack(side="left", padx=(20, 5))
        self.combo_sort = ttk.Combobox(top_frame, values=["Title A-Z", "Author A-Z", "Year Asc", "Year Desc"], state="readonly")
        self.combo_sort.set("Title A-Z")
        self.combo_sort.pack(side="left", padx=5)

        ttk.Button(top_frame, text="Sort", command=self.sort_books).pack(side="left", padx=5)

        self.tree_search = ttk.Treeview(self.tab_search, columns=("ID", "Title", "Author", "Year", "Category", "Status"), show="headings")
        for col in ("ID", "Title", "Author", "Year", "Category", "Status"):
            self.tree_search.heading(col, text=col)
            self.tree_search.column(col, width=120)
        self.tree_search.pack(fill="both", expand=True, padx=10, pady=5)

    def search_books(self):
        query = self.entry_search.get()
        results = self.library.search_books(query)
        self.refresh_search_table(results)

    def sort_books(self):
        criterion = self.combo_sort.get()
        results = self.library.sort_books(criterion)
        self.refresh_search_table(results)

    def refresh_search_table(self, book_list):
        for item in self.tree_search.get_children():
            self.tree_search.delete(item)
        for b in book_list:
            status = "Available" if b.is_available else "Borrowed"
            self.tree_search.insert("", "end", values=(b.id, b.title, b.author, b.year, b.category, status))

    # --- 5. STATISTICS PAGE ---
    def setup_stats_page(self):
        ttk.Button(self.tab_stats, text="Refresh Statistics", command=self.refresh_stats).pack(pady=15)
        self.label_stats = ttk.Label(self.tab_stats, text="", font=("Arial", 14), justify="left")
        self.label_stats.pack(pady=20)
        self.refresh_stats()

    def refresh_stats(self):
        total_books = len(self.library.books)
        available_books = sum(1 for b in self.library.books if b.is_available)
        borrowed_books = total_books - available_books
        total_members = len(self.library.members)

        text = (
            f"Total Books: {total_books}\n\n"
            f"Available Books: {available_books}\n\n"
            f"Borrowed Books: {borrowed_books}\n\n"
            f"Total Members: {total_members}"
        )
        self.label_stats.config(text=text)
