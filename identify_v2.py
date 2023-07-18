import sys
import sqlite3
import os

__author__ = "Matthew J. Harmon"
__license__ = "MIT"
__copyright__ = "© 2023 Matthew J. Harmon"

DATABASE_FILE = 'file_signatures.db'
SEGMENT_SIZE = 1024


def create_database():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Create table to store file type signatures
    c.execute('''CREATE TABLE IF NOT EXISTS signatures
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, signature BLOB, filetype TEXT, offset INTEGER DEFAULT 0)''')

    # Prepopulate the table with file type signatures if it's empty
    c.execute('SELECT COUNT(*) FROM signatures')
    count = c.fetchone()[0]

    if count == 0:
        signatures = [
            (b'\x25\x50\x44\x46', 'PDF', 0),
            (b'\x4d\x5a', 'Windows executable (PE format)', 0),
            (b'\xcf\xfa\xed\xfe', 'Mach-O executable (Mac OS X or iOS)', 0),
            (b'\xfe\xed\xfa\xcf', 'Mach-O executable (Mac OS X or iOS)', 0),
            (b'\x1f\x8b\x08', 'GZIP', 0),
            (b'\x50\x4b\x03\x04', 'ZIP', 0),
            # Add more file type signatures here
        ]

        c.executemany('INSERT INTO signatures (signature, filetype, offset) VALUES (?, ?, ?)', signatures)

    conn.commit()
    conn.close()


def identify_file_type(file_path):
    with open(file_path, 'rb') as file:
        while True:
            content = file.read(SEGMENT_SIZE)
            if not content:
                break

            conn = sqlite3.connect(DATABASE_FILE)
            c = conn.cursor()

            # Check for file type signatures
            c.execute('SELECT signature, filetype, offset FROM signatures')
            rows = c.fetchall()

            for row in rows:
                signature = row[0]
                filetype = row[1]
                offset = row[2]

                if len(content) >= offset + len(signature) and content[offset:].startswith(signature):
                    conn.close()
                    return filetype

            conn.close()

    return 'Unknown'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python file_type_identifier.py <file_path>')
        sys.exit(1)

    if not os.path.isfile(DATABASE_FILE):
        create_database()

    file_path = sys.argv[1]
    file_type = identify_file_type(file_path)
    print(f'The file type of "{file_path}" is: {file_type}')
