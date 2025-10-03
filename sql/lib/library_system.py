import sqlite3
import requests
from tkinter import *
from tkinter import messagebox

# ---------- Database Initialization ----------
def init_db():
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            is_issued INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# ---------- Register Member ----------
def register_member():
    win = Toplevel()
    win.title("Register Member")
    win.geometry("700x700")

    Label(win, text="Name").pack()
    name_entry = Entry(win)
    name_entry.pack()

    Label(win, text="Email").pack()
    email_entry = Entry(win)
    email_entry.pack()

    def save_member():
        name = name_entry.get()
        email = email_entry.get()
        if not name or not email:
            messagebox.showwarning("Missing info", "All fields required.")
            return
        conn = sqlite3.connect('library.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Member Registered!")
        win.destroy()

    Button(win, text="Register", command=save_member).pack(pady=10)

# ---------- Add New Book ----------
def add_book():
    win = Toplevel()
    win.title("Add Book")
    win.geometry("300x200")

    Label(win, text="Book Title").pack()
    title_entry = Entry(win)
    title_entry.pack()

    Label(win, text="Author").pack()
    author_entry = Entry(win)
    author_entry.pack()

    def save_book():
        title = title_entry.get()
        author = author_entry.get()
        if not title or not author:
            messagebox.showwarning("Missing info", "All fields required.")
            return
        conn = sqlite3.connect('library.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book Added!")
        win.destroy()

    Button(win, text="Add Book", command=save_book).pack(pady=10)

# ---------- Local Book Search ----------
def search_books():
    win = Toplevel()
    win.title("Local Book Search")
    win.geometry("400x300")

    Label(win, text="Search Keyword").pack()
    keyword_entry = Entry(win)
    keyword_entry.pack()

    text_result = Text(win, height=10, width=45)
    text_result.pack()

    def find_books():
        keyword = keyword_entry.get()
        conn = sqlite3.connect('library.db')
        cur = conn.cursor()
        cur.execute("SELECT title, author FROM books WHERE title LIKE ? OR author LIKE ?", 
                    (f'%{keyword}%', f'%{keyword}%'))
        rows = cur.fetchall()
        text_result.delete("1.0", END)
        if rows:
            for row in rows:
                text_result.insert(END, f"Title: {row[0]} | Author: {row[1]}\n")
        else:
            text_result.insert(END, "No books found.")
        conn.close()

    Button(win, text="Search", command=find_books).pack(pady=5)

# ---------- Google Books API Search ----------
def online_search():
    win = Toplevel()
    win.title("Online Book Search (Google API)")
    win.geometry("500x400")

    Label(win, text="Enter Book Name:").pack()
    query_entry = Entry(win, width=50)
    query_entry.pack()

    result_area = Text(win, wrap=WORD)
    result_area.pack()

    def search_api():
        query = query_entry.get()
        if not query:
            messagebox.showwarning("Missing", "Enter a book name.")
            return
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
        try:
            response = requests.get(url)
            data = response.json()
            result_area.delete("1.0", END)
            if "items" in data:
                for item in data["items"][:5]:
                    title = item["volumeInfo"].get("title", "N/A")
                    authors = item["volumeInfo"].get("authors", ["Unknown"])
                    result_area.insert(END, f"Title: {title}\nAuthors: {', '.join(authors)}\n\n")
            else:
                result_area.insert(END, "No results found.")
        except:
            result_area.insert(END, "Error fetching data.")

    Button(win, text="Search", command=search_api).pack(pady=5)

# ---------- Main App ----------
def main():
    init_db()

    root = Tk()
    root.title("Library Management System")
    root.geometry("400x350")
    root.config(bg="lightyellow")

    Label(root, text="Library Management", font=("Arial", 18, "bold"), bg="lightyellow").pack(pady=20)

    Button(root, text="Register Member", command=register_member, width=25).pack(pady=5)
    Button(root, text="Add Book", command=add_book, width=25).pack(pady=5)
    Button(root, text="Search Local Books", command=search_books, width=25).pack(pady=5)
    Button(root, text="Search Books Online", command=online_search, width=25).pack(pady=5)

    Button(root, text="Exit", command=root.quit, width=25).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
