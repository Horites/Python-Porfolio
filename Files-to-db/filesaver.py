import os
import sqlite3

def get_files_in_directory(directory_path):
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    return [(f, open(os.path.join(directory_path, f), 'rb').read()) for f in files]

directory_path = 'path/to/directory'  # Replace with your directory path
file_data = get_files_in_directory(directory_path)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('files.db')
c = conn.cursor()

# Create a table named 'files' with two columns: 'filename' and 'filedata'
c.execute('''
    CREATE TABLE files (
        filename TEXT,
        filedata BLOB
    )
''')

# Insert each filename and corresponding file data into the 'files' table
c.executemany('''
    INSERT INTO files (filename, filedata) VALUES (?, ?)
''', file_data)

# Commit the changes and close the connection
conn.commit()
conn.close()
