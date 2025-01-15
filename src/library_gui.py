import csv
import tkinter as tk
from tkinter import messagebox,simpledialog
from inventory import Inventory
from PIL import Image, ImageTk
from user_manager import UserManager
from update_files import UpdateFiles
import os

class LibraryGUI:
    """
    @author Roy Meoded
    @author Noa Agassi
    The GUI file (Graphical User Interface) is a crucial component of the library management system. Its purpose is to provide users with an easy and accessible way to interact with the system without requiring direct code usage. The file includes the following functionalities:
    User Registration: The system allows new users to register by providing a username and password.
    Login: Existing users can log in, verify their credentials, and perform further actions.
    Add Books: Admins can add new books to the database.
    Remove Books: Existing books can be removed from the inventory.
    Lend Books: Users can borrow books from the inventory.
    Return Books: Books can be returned to the inventory when a user has finished using them.
    Display Books: Allows admins and users to view all the books in the system.
    Manage Waitlist: Displays users who are waiting for specific books.
    The interface uses libraries like Tkinter to create windows and graphical interactions.
    """
    def __init__(self, inventory,user_manager):
        self.inventory = inventory
        self.root = tk.Tk()  # Create the main frame
        self.user_manager=user_manager
        self.root.title("Library Management System")  # The title
        self.root.geometry("600x800")  # Define the size of the frame


        self.original_image = Image.open("../assets/books_background.jpg") #The location of the image
        self.bg_image = None
        self.bg_label = tk.Label(self.root)
        self.bg_label.place(relwidth=1, relheight=1)
        self.update_background_image()
        self.root.bind("<Configure>", self.resize_image)

        self.login_frame=None
        self.main_frame=None

        self.show_login_screen()

    def update_background_image(self):
        """
        Updating the background image according to the window siz
        """
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        resized_image = self.original_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.bg_label.config(image=self.bg_image)

    def resize_image(self, event):
        """
        Resize the image by the size of the window
        """
        self.update_background_image()

    def show_login_screen(self):
        """
        Display the login screen with a dynamic background image
        """
        self.login_frame = tk.Frame(self.root)
        self.login_frame.place(relwidth=1, relheight=1)

        try:
            login_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/books_background.jpg"))

            if not os.path.exists(login_image_path):
                raise FileNotFoundError(f"Login image not found: {login_image_path}")

            self.original_login_image = Image.open(login_image_path)

            self.lsgin_bg_label = tk.Label(self.login_frame)
            self.login_bg_label.place(relwidth=1, relheight=1)

            self.update_login_background()

            self.root.bind("<Configure>", self.update_login_background)
        except Exception as e:
            print(f"Error loading login background image: {e}")
            messagebox.showerror("Error", f"Failed to load login background image: {e}")

        title_label = tk.Label(
            self.login_frame,
            text="Library Management System\nLogin ",
            font=("Arial", 30),
            bg="#ffffff",
            fg="#333333",
            justify="center"
        )
        title_label.place(relx=0.5, rely=0.3, anchor="center")

        tk.Label(self.login_frame, text="Username:", bg="#ffffff", font=("Ariel", 16)).place(relx=0.5, rely=0.4,
                                                                                             anchor="center")
        self.username_entry = tk.Entry(self.login_frame, font=("Ariel", 16))
        self.username_entry.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(self.login_frame, text="Password:", bg="#ffffff", font=("Ariel", 16)).place(relx=0.5, rely=0.5,
                                                                                             anchor="center")
        self.password_entry = tk.Entry(self.login_frame, font=("Ariel", 16), show="*")
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")

        login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        login_button.place(relx=0.5, rely=0.65, anchor="center")

    def update_login_background(self, event=None):
        """
        Update the login screen background dynamically based on window size
        """
        try:
            width = self.root.winfo_width()
            height = self.root.winfo_height()

            resized_image = self.original_login_image.resize((width, height), Image.Resampling.LANCZOS)
            self.login_bg_image = ImageTk.PhotoImage(resized_image)

            self.login_bg_label.config(image=self.login_bg_image)
            self.login_bg_label.image = self.login_bg_image
        except Exception as e:
            print(f"Error updating login background image: {e}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.inventory.log_action("User Login", success=False, details="Missing username or password.")
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        if self.user_manager.authenticate_user(username, password):
            self.inventory.log_action("User Login", success=True, details=f"User '{username}' logged in successfully.")
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.show_main_screen()
        else:
            self.inventory.log_action("User Login", success=False,
                                      details=f"Invalid login attempt for user '{username}'.")
            messagebox.showerror("Error", "Invalid username or password.")

    def logout(self):
        """
        Logout the current user and return to the login screen.
        """
        confirmation = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirmation:
            for widget in self.root.winfo_children():
                widget.destroy()

            self.show_login_screen()

    def show_main_screen(self):
        """
        Display the main library system screen.
        """
        if self.login_frame:
            self.root.unbind("<Configure>")
            self.login_frame.destroy

        for widget in self.root.winfo_children():
            widget.destroy()

        self.main_frame = tk.Frame(self.root, bg="#ffffff")
        self.main_frame.place(relwidth=1, relheight=1)

        title_label = tk.Label(
            self.root,
            text="Library Management System \nBy: Roy Meoded & Noa Agassi",
            font=("Arial", 30),
            bg="#ffffff",
            fg="#333333",
            justify="center"
        )
        title_label.pack(pady=20)

        buttons_frame = tk.Frame(self.root, bg="#ffffff")
        buttons_frame.pack(pady=20)

        # Button for add book:
        add_book_button = tk.Button(buttons_frame, text="Add Book", width=15, command=self.add_book)
        add_book_button.grid(row=0, column=0, padx=10, pady=10)  # Location of the button on (row:0,column:0)

        # Button for remove book:
        remove_book_button = tk.Button(buttons_frame, text="Remove Book", width=15, command=self.remove_book)
        remove_book_button.grid(row=0, column=1, padx=10, pady=10)  # Location of the button on (row:0,column:1)

        # Button for display books:
        display_books_button = tk.Button(buttons_frame, text="View Books", width=15, command=self.display_books)
        display_books_button.grid(row=1, column=0, padx=10, pady=10)  # Location of the button on (row:1,column:0)

        # Button for search books:
        search_books_button = tk.Button(buttons_frame, text="Lend Book", width=15, command=self.lend_book)
        search_books_button.grid(row=1, column=1, padx=10, pady=10)  # Location of the button on (row:1,column:1)

        # Button for return book:
        return_book_button = tk.Button(buttons_frame, text="Return Book", width=15, command=self.return_book)
        return_book_button.grid(row=2, column=0, padx=10, pady=10)  # Location of the button on (row:2,column:0)

        # Button for register user:
        register_book_button = tk.Button(buttons_frame, text="Register", width=15, command=self.register)
        register_book_button.grid(row=0, column=2, padx=10, pady=10)  # Location of the button on (row:0,column:2)

        # Button for search book:
        search_book_button = tk.Button(buttons_frame, text="Search Book", width=15, command=self.search_book)
        search_book_button.grid(row=2, column=1, padx=10, pady=10)  # Location of the button on (row:2,column:1)

        # Button for Logout :
        logout_button = tk.Button(buttons_frame, text="Logout", width=15, command=self.logout)
        logout_button.grid(row=2, column=2, padx=10, pady=10)  # Location of the button on (row:2,column:2)

        # Button for Popular books :
        popular_books_button = tk.Button(buttons_frame, text="Popular Books", width=15, command=self.popular_books)
        popular_books_button.grid(row=1, column=2, padx=10, pady=10)  # Location of the button on (row:1,column:2)

        # Button for displaying the waitlist:
        waitlist_button = tk.Button(buttons_frame, text="View Waitlist", width=15, command=self.view_waitlist)
        waitlist_button.grid(row=3, column=0, padx=10, pady=10)

        # Create text area for introduce information:
        self.output_area = tk.Text(self.root, wrap=tk.WORD, width=150, height=40,font=("Ariel",20))
        self.output_area.pack(pady=20)

    def view_waitlist(self):
        """
        Display the current waitlist in the GUI.
        """
        self.output_area.delete(1.0, tk.END)  # Clear the output area

        if not self.inventory.waitlist:
            self.output_area.insert(tk.END, "No waitlist entries found.\n")
            print("DEBUG: Waitlist is empty or not loaded properly.")
        else:
            self.output_area.insert(tk.END, "Waitlist:\n")
            self.output_area.insert(tk.END, "-" * 180 + "\n")
            for book_title, users in self.inventory.waitlist.items():
                self.output_area.insert(tk.END, f"Book: {book_title}\n")
                for user in users:
                    self.output_area.insert(
                        tk.END,
                        f"  - Name: {user['username']}, Email: {user['email']}, Phone: {user['phone']}\n"
                    )
                self.output_area.insert(tk.END, "-" * 180 + "\n")

    # Method for add book:
    def add_book(self):
        """
        Use Inventory's add_book method to add a new book
        """
        #Get information from the user:
        book_title=simpledialog.askstring("Add Book","Enter the book title:")
        book_author=simpledialog.askstring("Add Book","Enter the book author:")
        book_copies=simpledialog.askstring("Add Book","Enter the book copies:")
        book_category=simpledialog.askstring("Add Book","Enter the book category:")
        book_year=simpledialog.askstring("Add Book","Enter the book year:")


        if not book_title or not book_copies or not book_year or not book_author or not book_category:
            messagebox.showerror("Error","All fields are required!")
            return

        try:
            #Creating a book object and use the Inventory to add him:
            from book import Book
            new_book=Book(title=book_title,author=book_author,copies=book_copies,category=book_category,year=book_year,is_loaned=False)
            self.inventory.add_book(new_book)
            messagebox.showinfo("Success",f"Book {book_title} added successfully!")
        except Exception as e:
            messagebox.showerror("Error",f"Failed to add book :{e}")

    # Method for remove book:
    def remove_book(self):
        """
        Use Inventory's remove_book method to remove a  book
        """
        # Get information from the user:
        book_title = simpledialog.askstring("Add Book", "Enter the book title:")

        if not book_title :
            messagebox.showerror("Error", "Book's title is required!")
            return

        if self.inventory.remove_book(book_title):
            messagebox.showinfo("Success", f"Book {book_title} removed successfully!")
        else:
            messagebox.showinfo("Error", f"Book {book_title} not found in the inventory")

    def search_book(self):
        """
        Search book by title, author, or category and display results in the output area.
        Logs the search action with success or failure details.
        """
        search_term = simpledialog.askstring("Search Books", "Enter title, author, or category:")
        if not search_term:
            self.inventory.log_action("Search Book - GUI", success=False, details="Search term not provided.")
            messagebox.showerror("Error", "Search term is required!")
            return

        try:

            available_books = {}
            with open("../csv_files/available_books.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row.get("Title", "Unknown Title")
                    available = row.get("Available", "0")
                    available_books[title] = int(available) if available.isdigit() else 0

            all_terms = set(
                book.title.lower() for book in self.inventory.books
            ) | set(
                book.author.lower() for book in self.inventory.books
            ) | set(
                book.category.lower() for book in self.inventory.books
            )

            if search_term.lower() not in all_terms:
                self.inventory.log_action(
                    "Search Book - GUI",
                    success=False,
                    details=f"Invalid search term '{search_term}' entered."
                )
                messagebox.showerror("Error", f"'{search_term}' is not recognized in the system.")
                return

            results = [
                book for book in self.inventory.books
                if search_term.lower() in book.title.lower() or
                   search_term.lower() in book.author.lower() or
                   search_term.lower() in book.category.lower()
            ]

            self.output_area.delete(1.0, tk.END)

            if not results:
                self.inventory.log_action(
                    "Search Book - GUI",
                    success=False,
                    details=f"No books found for search term '{search_term}'."
                )
                self.output_area.insert(tk.END, "No books found matching the criteria.\n")
            else:
                self.inventory.log_action(
                    "Search Book - GUI",
                    success=True,
                    details=f"Found {len(results)} books for search term '{search_term}'."
                )
                self.output_area.insert(tk.END, "Search Results:\n")
                self.output_area.insert(tk.END, "-" * 180 + "\n")
                for book in results:
                    title = f"Title: {book.title}"
                    author = f"Author: {book.author}"
                    genre = f"Genre: {book.category}"
                    year = f"Year: {book.year}"
                    total_copies = book.copies
                    available_copies = available_books.get(book.title, 0)

                    self.output_area.insert(tk.END, f"{title}\n")
                    self.output_area.insert(tk.END, f"{author}\n")
                    self.output_area.insert(tk.END, f"{genre}\n")
                    self.output_area.insert(tk.END, f"{year}\n")
                    self.output_area.insert(
                        tk.END,
                        f"Available Copies: {available_copies}/{total_copies}\n"
                    )
                    self.output_area.insert(tk.END, "-" * 180 + "\n\n")

        except FileNotFoundError:
            self.inventory.log_action(
                "Search Book - GUI",
                success=False,
                details="Error: available_books.csv file not found."
            )
            self.output_area.insert(tk.END, "Error: available_books.csv file not found.\n")
        except Exception as e:
            self.inventory.log_action(
                "Search Book - GUI",
                success=False,
                details=f"Error loading books: {e}"
            )
            self.output_area.insert(tk.END, f"Error loading books: {e}\n")

    def popular_books(self):
        """
        Display the most popular books based on the number of borrowed copies.
        """
        top_n = 10  # Number of popular books to display
        popular_books = self.inventory.get_popular_books(top_n=top_n)

        if not popular_books:
            messagebox.showinfo("Popular Books", "No popular books found.")
            return

        # Clear the output area and display the results
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, f"Top {top_n} Popular Books:\n")
        self.output_area.insert(tk.END, "-" * 50 + "\n")
        for idx, (title, borrowed_count) in enumerate(popular_books, start=1):
            self.output_area.insert(
                tk.END,
                f"{idx}. {title} - Borrowed {borrowed_count} times\n"
            )

    # Method for display books:
    def display_books(self):
        """
        Display all books in the inventory with their updated available copies out of total copies.
        """
        self.output_area.delete(1.0, tk.END)  # Clear the output area

        try:
            available_books = {}
            with open("../csv_files/available_books.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row.get("Title", "Unknown Title")
                    available = row.get("Available", "0")
                    available_books[title] = int(available) if available.isdigit() else 0

            if not self.inventory.books:
                self.output_area.insert(tk.END, "No books in the inventory.\n")
            else:
                self.output_area.insert(tk.END, "Books in the inventory:\n")
                self.output_area.insert(tk.END, "-" * 180 + "\n")
                for book in self.inventory.books:
                    title = book.title
                    author = book.author
                    genre = book.category
                    year = book.year
                    total_copies = book.copies
                    available_copies = available_books.get(title, 0)
                    self.output_area.insert(
                        tk.END,
                        f"Title: {title}\nAuthor: {author}\nGenre: {genre}\nYear: {year}\n"
                        f"Available Copies: {available_copies}/{total_copies}\n"
                    )
                    self.output_area.insert(tk.END, "-" * 180 + "\n\n")
        except FileNotFoundError:
            self.output_area.insert(tk.END, "Error: available_books.csv file not found.\n")
        except Exception as e:
            self.output_area.insert(tk.END, f"Error loading books: {e}\n")

    def register(self):
        new_username = simpledialog.askstring("Register", "Enter a new username:")
        new_password = simpledialog.askstring("Register", "Enter a new password:", show="*")

        if not new_username or not new_password:
            self.inventory.log_action("User Registration", success=False, details="Missing username or password.")
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        if self.user_manager.add_user(new_username, new_password):
            self.inventory.log_action("User Registration", success=True,
                                      details=f"User '{new_username}' registered successfully.")
            messagebox.showinfo("Success", "User registered successfully!")
        else:
            self.inventory.log_action("User Registration", success=False,
                                      details=f"Failed to register '{new_username}'. Username already exists.")
            messagebox.showerror("Error", "Username already exists.")

    # Method for lend book:
    def lend_book(self):
        """
        Lend a book to a user or add them to the waitlist if no copies are available.
        """
        book_title = simpledialog.askstring("Lend Book", "Enter the book title to lend")
        if not book_title:
            messagebox.showerror("Error", "Book title is required.")
            return

        result = self.inventory.lend_book(book_title, username="example_user")

        if result is None:
            messagebox.showerror("Error", f"Book '{book_title}' not found in the inventory.")
            return

        elif result:
            messagebox.showinfo("Success", f"Book '{book_title}' lent successfully!")
        else:
            response = messagebox.askyesno("Waitlist",
                                           f"No copies available for '{book_title}'. Do you want to join the waitlist?")
            if response:
                username = simpledialog.askstring("Waitlist", "Enter your name:")
                email = simpledialog.askstring("Waitlist", "Enter your email:")
                phone = simpledialog.askstring("Waitlist", "Enter your phone number:")

                if not username or not email or not phone:
                    messagebox.showerror("Error", "All fields are required to join the waitlist.")
                    return

                self.inventory.add_to_waitlist(book_title, username, email, phone)
                messagebox.showinfo("Waitlist", f"You have been added to the waitlist for '{book_title}'.")

    # Method for return book:
    def return_book(self):
        """
        Prompt the user for a book title, return the book, and notify if someone is on the waitlist.
        """
        book_title = simpledialog.askstring("Return Book", "Enter the book title to return:")
        if not book_title:
            messagebox.showerror("Error", "Book title is required.")
            return

        result = self.inventory.return_book(book_title)

        if result == "all_copies_available":
            messagebox.showinfo("Info", f"All copies of '{book_title}' are already available in the library.")
        elif result == True:
            messagebox.showinfo("Success", f"Book '{book_title}' returned successfully!")

            last_lent_user = self.inventory.returned_last_user
            if last_lent_user:
                messagebox.showinfo(
                    "Waitlist Notification",
                    f"The book '{book_title}' has been returned and is now lent to "
                    f"{last_lent_user['username']} (Email: {last_lent_user['email']}, Phone: {last_lent_user['phone']})."
                )
        else:
            messagebox.showerror("Error", f"Book '{book_title}' not found .")

    # Method for start the GUI:
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    inventory = Inventory()
    user_manager=UserManager()
    gui = LibraryGUI(inventory,user_manager)
    gui.run()