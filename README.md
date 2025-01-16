# Library Management System
# By: Roy Meoded & Noa Agassi


## Introduction
The *Library Management System* is a Python-based project designed to manage book inventories
,users,loans,and returns efficiently.
This system provides a user-friendly interface for administrators and readers, making library management streamlined and intuitive.

---
## Features
- *User Management:*
  - Add and authenticate users.
  - Save and load user data from CSV files.
- *Book Inventory Management:*
  - Add, remove, lend, and return books.
  - Search books by title, author, or category.
  - Sync inventory to CSV files.
- *Waiting List Management:*
  - Add and remove users from waiting lists.
  - Sync waiting lists to CSV files.
- *GUI:*
  - User-friendly interface for performing library operations.

## Requirements
The project requires the following Python libraries:
- pandas
- unittest
- werkzeug
---

## File Structure
- *src/*
  - Contains the core modules of the system, including inventory.py, user_manager.py, and book.py. ,
  ,library_gui.py,design patterns files and more..
  - Contains unit tests for the application.
- *csv_files/*
  - Directory for storing CSV files such as books.csv, available_books.csv,waiting_list.csv, loaned_books.csv, and users.csv.

## Design Patterns Utilized

This project employs several key design patterns to ensure scalability,
maintainability, and modularity in the Library Management System:

1. *Observer Pattern*:
   The Observer Pattern is used to keep the system components synchronized. 
   For instance, when the inventory is updated, observers such as the GUI are notified automatically, ensuring that the user interface always reflects the current state of the system.

2. *Decorator Pattern*:
   The Decorator Pattern allows additional features, such as waiting lists or borrow counts, 
   to be dynamically added to book objects without altering the core Book class. This ensures that the system remains flexible for future enhancements.

3. *Iterator Pattern*:
   The Iterator Pattern simplifies the traversal of collections such as the inventory.
   It allows for clean and efficient looping through the list of books without exposing the internal structure of the collection.

4. *Strategy Pattern*:
   The Strategy Pattern enables flexible and dynamic searching capabilities. 
   The Inventory.search_books() method leverages this pattern to allow searches by various criteria like title, author, or category, without the need to hardcode the logic.

5. *Factory Pattern*:
   The Factory Pattern is implemented in the BookFactory to encapsulate the creation logic of Book objects.
   This ensures consistency and simplifies the addition of new books to the inventory.

### Advantages of These Patterns
By using these design patterns, the system achieves:
- *Modularity*: Each component can function independently, making the system easier to manage and debug.
- *Flexibility*: New features can be added with minimal changes to the existing codebase.
- *Scalability*: The system is designed to handle larger libraries and more complex operations as needed.


These patterns collectively ensure that the Library Management System remains robust and easy to maintain as it evolves.

## Testing
To run unit tests, navigate to the src/ directory and execute:
bash
python -m unittest discover

## Prerequisites
Ensure you have the following installed:
- Python 3.10 or above
- pip (Python package manager)

---
## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/roy3177/library-management-system.git
   cd library-management-system  

---

## Running the Project

To run the *Library Management System* on your Linux machine, follow these steps:

1. *Navigate to the Project Directory*  
   Ensure you are in the project directory where all the files are located:
   bash
   cd Library-Management-System
   

2. *Install Dependencies*
   Add to csv.files to the src files by cp csv_files/*.csv src/
   Use the final.txt file to install the necessary Python libraries:
   bash
   pip install -r final.txt
   

4. *Run the GUI*  
   The main entry point for interacting with the program is the graphical user interface (library_gui.py). Launch the GUI using the following command:
   bash
   python src/library_gui.py
   

5. *Interact with the GUI*  
   - *Log in or Register*: Use the user management options to log in or register new users.
   - *Manage Books*: Add, remove, search, lend, or return books directly through the GUI.
   - *Manage Waiting Lists*: Add or remove users from waiting lists.

6. *Run Unit Tests (Optional)*  
   To validate the functionality of the program, you can run the included unit tests:
   bash
   python -m unittest discover src/
   

7. *Exit the Program*  
   Close the GUI window when you are finished with your tasks.

---

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Authors
- *Roy Maoded*
- *Noa Agassi*
