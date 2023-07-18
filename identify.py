import sys
import sqlite3
import os

__author__ = "Matthew J. Harmon"
__license__ = "MIT"
__copyright__ = "© 2023 Matthew J. Harmon" 

BUILTIN_DATABASE_FILE = 'builtin_language_signatures.db'


def create_builtin_database():
    conn = sqlite3.connect(BUILTIN_DATABASE_FILE)
    c = conn.cursor()

    # Create table to store language signatures
    c.execute('''CREATE TABLE IF NOT EXISTS signatures
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, signature BLOB, language TEXT)''')

    # Prepopulate the table with language signatures if it's empty
    c.execute('SELECT COUNT(*) FROM signatures')
    count = c.fetchone()[0]

    if count == 0:
        signatures = [
            (b'\x7fELF', 'C or C++ (ELF executable)'),
            (b'\x4d\x5a', 'Windows executable (PE format)'),
            (b'\xcf\xfa\xed\xfe', 'Mach-O executable (Mac OS X or iOS)'),
            (b'\xfe\xed\xfa\xcf', 'Mach-O executable (Mac OS X or iOS)'),
            (b'\x25\x50\x44\x46', 'PDF document'),
            (b'<?php', 'PHP script'),
            (b'#!/usr/bin/env python', 'Python script'),
            (b'#!/bin/bash', 'Bash script')
        ]

        c.executemany('INSERT INTO signatures (signature, language) VALUES (?, ?)', signatures)

    conn.commit()
    conn.close()


def create_custom_database(database_file):
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    # Create table to store language signatures
    c.execute('''CREATE TABLE IF NOT EXISTS signatures
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, signature BLOB, language TEXT)''')

    conn.commit()
    conn.close()


def identify_language(file_path, database_file=None):
    with open(file_path, 'rb') as file:
        content = file.read()

    if database_file is None:
        database_file = BUILTIN_DATABASE_FILE

    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    # Check for common language signatures
    c.execute('SELECT signature, language FROM signatures')
    rows = c.fetchall()

    matched_languages = []

    for row in rows:
        signature = row[0]
        language = row[1]

        if content.startswith(signature):
            matched_languages.append(language)

    conn.close()

    if matched_languages:
        return ', '.join(matched_languages)
    else:
        return 'Unknown'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python identify_language.py <executable_path> [database_file]')
        sys.exit(1)

    executable_path = sys.argv[1]
    database_file = sys.argv[2] if len(sys.argv) >= 3 else None

    if database_file and not os.path.isfile(database_file):
        create_custom_database(database_file)
    else:
        create_builtin_database()

    languages = identify_language(executable_path, database_file)
    print(f'The programming language(s) used in "{executable_path}" is/are: {languages}')
