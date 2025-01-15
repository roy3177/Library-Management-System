import os


def get_csv_path(filename):
    """
    Get the full path to a CSV file located in the 'csv_files' directory.

    :param filename: Name of the CSV file (e.g., 'books.csv').
    :return: Full path to the file as a string.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory of the running script
    csv_dir = os.path.join(base_dir, "../csv_files")  # Path to the 'csv_files' folder
    return os.path.join(csv_dir, filename)