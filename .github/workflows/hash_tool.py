#!/usr/bin/env python3
"""
hash_tool.py

A simple command-line tool that:
  1. Generates a hash table (JSON file) for every file in a chosen directory.
  2. Verifies files in a directory against a previously generated hash table,
     detecting modified, added, and deleted files.

Uses only the Python standard library (hashlib, os, json).
"""

import os
import json
import hashlib

# Name of the JSON file used to store the hash table.
HASH_TABLE_FILE = "hash_table.json"

# Chunk size (in bytes) used when reading files for hashing.
# Reading in chunks avoids loading very large files entirely into memory.
CHUNK_SIZE = 8192

# Hash algorithm to use. SHA-256 is a strong, widely-used cryptographic hash.
HASH_ALGORITHM = "sha256"


def hash_file(filepath):
    """
    Calculates the cryptographic hash of a file's contents.

    Args:
        filepath (str): Path to the file to hash.

    Returns:
        str: The hex digest of the file's hash, or None if the file
             could not be read (e.g. permission error, broken symlink).
    """
    hasher = hashlib.new(HASH_ALGORITHM)
    try:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                hasher.update(chunk)
    except (OSError, IOError) as e:
        print(f"  [!] Could not read '{filepath}': {e}")
        return None

    return hasher.hexdigest()


def traverse_directory(directory):
    """
    Navigates to the directory entered by the user and collects the full
    path of every file found (recursively, including subdirectories).

    Args:
        directory (str): The root directory to search.

    Returns:
        list[str]: A list of file paths found within the directory.
    """
    file_paths = []

    for root, _dirs, files in os.walk(directory):
        for filename in files:
            full_path = os.path.join(root, filename)
            file_paths.append(full_path)

    return file_paths


def generate_table(directory):
    """
    Traverses the given directory, hashes every file within it, and writes
    the results (filepath -> hash) to a JSON hash table file.

    Args:
        directory (str): The directory to hash.
    """
    file_paths = traverse_directory(directory)

    if not file_paths:
        print(f"No files found in '{directory}'. Nothing to hash.")
        return

    hash_table = {}
    for filepath in file_paths:
        file_hash = hash_file(filepath)
        if file_hash is not None:
            hash_table[filepath] = file_hash

    with open(HASH_TABLE_FILE, "w") as f:
        json.dump(hash_table, f, indent=4)

    print("Hash table generated")


def validate_hash(directory):
    """
    Reads the previously generated hash table, re-traverses the directory,
    recomputes the hash of each file currently present, and compares those
    hashes to the stored values.

    Also reports files that have been added (present in the directory but
    not in the stored table) or deleted (present in the stored table but
    no longer in the directory).

    Args:
        directory (str): The directory to verify.
    """
    if not os.path.exists(HASH_TABLE_FILE):
        print(f"No hash table found ('{HASH_TABLE_FILE}'). "
              f"Generate one first using option 1.")
        return

    with open(HASH_TABLE_FILE, "r") as f:
        stored_table = json.load(f)

    current_files = traverse_directory(directory)
    current_file_set = set(current_files)
    stored_file_set = set(stored_table.keys())

    # Files present now AND in the stored table -> check hash validity.
    for filepath in sorted(current_file_set & stored_file_set):
        current_hash = hash_file(filepath)
        stored_hash = stored_table[filepath]

        if current_hash is None:
            print(f"{filepath} hash is invalid (unreadable)")
        elif current_hash == stored_hash:
            print(f"{filepath} hash is valid")
        else:
            print(f"{filepath} hash is invalid")

    # Files present now but NOT in the stored table -> newly added.
    for filepath in sorted(current_file_set - stored_file_set):
        print(f"New file detected (not in hash table): {filepath}")

    # Files in the stored table but NOT present now -> deleted.
    for filepath in sorted(stored_file_set - current_file_set):
        print(f"File has been deleted: {filepath}")


def get_directory_from_user():
    """
    Prompts the user for a directory path and validates that it exists.

    Returns:
        str: A valid, existing directory path.
    """
    while True:
        directory = input("Enter the directory path: ").strip()
        if os.path.isdir(directory):
            return directory
        print(f"'{directory}' is not a valid directory. Please try again.")


def main():
    """
    Handles user input, calls the appropriate functions, and drives the
    overall program flow.
    """
    print("Hashing Program")
    print("1. Generate a new hash table")
    print("2. Verify hashes")

    choice = input("Select an option (1 or 2): ").strip()

    if choice == "1":
        directory = get_directory_from_user()
        generate_table(directory)
    elif choice == "2":
        directory = get_directory_from_user()
        validate_hash(directory)
    else:
        print("Invalid option. Please run the program again and enter 1 or 2.")


if __name__ == "__main__":
    main()
