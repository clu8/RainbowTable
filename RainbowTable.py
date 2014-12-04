#!/usr/bin/env python

"""
Rainbow table attack
Jialin Ding (jding09@stanford.edu) and Charles Lu (charleslu@stanford.edu)
CS 55N Autumn 2014 with Dan Boneh
----------------------------------------------------------------------------
Contains functionality to create a rainbow table and crack a hash for 6-digit lowercase passwords.
"""

# Use Python 3

import hashlib
import random
import string
import csv
import pickle
import os
import time

CHAIN_LENGTH = 1000
ROWS = 3 * 10**6
CSV_FILE = "RainbowTable.csv"
CSV_FIELDNAMES = ['start_point', 'endpoint_hash']
PICKLE_FILE = "RainbowTable.pickle"
RAINBOW_TABLE = {}

"""Creates rainbow table using H() and R() with ROWS of CHAIN_LENGTH hashes in CSV_FILE
Precondition: To expand, input number of rows as param expand
"""
def create_rainbow_table(expandRows=None):
    if expandRows:
        rows = expandRows
        mode = 'a'
        print("Expanding rainbow table...")
    else:
        if input("Are you sure? This will overwrite any existing table. (y/n) ") != "y":
            print("Cancelling.")
            return
        rows = ROWS
        mode = 'w'
        print("Creating rainbow table...")

    startTime = time.time()
    with open(CSV_FILE, mode) as table:
        writer = csv.DictWriter(table, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for i in range(rows):
            if i % 1000 == 0:
                 print(i)

            start = ""
            for _ in range(6):
                start += random.choice(string.ascii_lowercase)

            plainText = start
            for col in range(CHAIN_LENGTH):
                hash = H(plainText)
                plainText = R(hash, col)
            writer.writerow({CSV_FIELDNAMES[0]: start, CSV_FIELDNAMES[1]: hash})

    elapsed = time.time() - startTime
    print("Done in {0} mins, {1} secs.".format(int(elapsed / 60), elapsed % 60))

'''Clears any existing rainbow table loaded into memory and reloads it from CSV_FILE.
Also stores the dictionary in PICKLE_FILE for fast access.
Keys are endpoint hashes, values are start plaintexts.
'''
def load_rainbow_table():
    global RAINBOW_TABLE
    RAINBOW_TABLE = {}
    print("Loading rainbow table from CSV and saving as pickle file...")
    startTime = time.time()
    with open(CSV_FILE, 'r') as table:
        reader = csv.DictReader(table)
        for row in reader:
            RAINBOW_TABLE[row[CSV_FIELDNAMES[1]]] = row[CSV_FIELDNAMES[0]]

    pickle.dump(RAINBOW_TABLE, open(PICKLE_FILE, "wb"))

    print("Done loading in {0} secs.".format(time.time() - startTime))

def crack(hashedPassword, reloadTable=False):
    global RAINBOW_TABLE
    if reloadTable or not os.path.isfile(PICKLE_FILE):
        load_rainbow_table()
    if reloadTable or not RAINBOW_TABLE:
        print("Loading rainbow table from pickle file...")
        RAINBOW_TABLE = pickle.load(open(PICKLE_FILE, "rb"))

    print("Cracking hash...")
    startTime = time.time()

    for startCol in range(CHAIN_LENGTH-1, -1, -1):
        candidate = hashedPassword
        for col in range(startCol, CHAIN_LENGTH):
            candidate = H(R(candidate, col-1))
        if candidate in RAINBOW_TABLE:
            traversalResult = traverse_chain(hashedPassword, RAINBOW_TABLE[candidate])
            if traversalResult:
                print("Done cracking in {0} secs.".format(time.time() - startTime))
                return traversalResult

"""Traverses a chain in the table to find the plaintext password once we've found a possible one
Postcondition: Returns plaintext password if successful; otherwise returns None
"""
def traverse_chain(hashedPassword, start):
    for col in range(CHAIN_LENGTH):
        hash = H(start)
        if hash == hashedPassword:
            return start
        start = R(hash, col)

    return None

"""Hash function
Precondition: Input plaintext as string
Postcondition: Returns hash as string
"""
def H(plaintext):
    return hashlib.sha256(bytes(plaintext, 'utf-8')).hexdigest()

"""Reduction function
Precondition: hash is H(previousPlaintext)
Postcondition: returns randomly distributed 6-digit lowercase plaintext password
"""
def R(hash, col):
    plaintextKey = (int(hash[:9], 16) ^ col) % 308915776 # 26**6
    plaintext = ""
    for _ in range(6):
        plaintext += string.ascii_lowercase[plaintextKey % 26]
        plaintextKey //= 26
    return plaintext

"""Precondition: Input a 6 digit lowercase password to test, or input no arguments to generate a random password
Postcondition: Cracks H(password) and prints elapsed time
"""
def test(password=""):
    start = time.time()

    if password == "":
        for _ in range(6):
            password += random.choice(string.ascii_lowercase)

    print("Cracking password: {0}\nH(password): {1}".format(password, H(password)))

    cracked = crack(H(password))
    if cracked:
        print("Success! Password: {0}".format(cracked))
    else:
        print("Unsuccessful :(")