#!/usr/bin/env python

"""
Rainbow table attack
Jialin Ding (jding09@stanford.edu) and Charles Lu (charleslu@stanford.edu)
CS 55N Autumn 2014 with Dan Boneh
----------------------------------------------------------------------------
Contains functionality to create a rainbow table and crack a hash for 6-digit passwords.
"""

# Use Python 3

import hashlib
import random
import string
import csv
import time

CHAIN_LENGTH = 1000
ROWS = 3 * 10**6
TABLE_FILE = "RainbowTable.csv"
TABLE_FIELDNAMES = ['start_point', 'endpoint_hash']
rainbowTable = {}

"""Creates rainbow table using H() and R() with ROWS of CHAIN_LENGTH in TABLE_FILE
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
    with open(TABLE_FILE, mode) as table:
        writer = csv.DictWriter(table, fieldnames=TABLE_FIELDNAMES)
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
            writer.writerow({TABLE_FIELDNAMES[0]: start, TABLE_FIELDNAMES[1]: hash})

    elapsed = time.time() - startTime
    print("Done in {0} mins, {1} secs.".format(int(elapsed / 60), elapsed % 60))

def load_rainbow_table():
    print("Loading rainbow table...")
    startTime = time.time()
    with open(TABLE_FILE, 'r') as table:
        reader = csv.DictReader(table)
        for row in reader:
            rainbowTable[row[TABLE_FIELDNAMES[1]]] = row[TABLE_FIELDNAMES[0]]
            # rainbowTable: keys are endpoint hashes, values are start plaintexts
    print("Done loading in {0} secs.".format(time.time() - startTime))

def crack(hashedPassword):
    if len(rainbowTable) == 0:
        load_rainbow_table()

    for col in range(CHAIN_LENGTH):
        candidate = hashedPassword
        for column in range(col, CHAIN_LENGTH):
            if column % 1000 == 0:
                print(column)

            if candidate in rainbowTable:
                traversalResult = traverse_chain(hashedPassword, rainbowTable[candidate])
                if traversalResult:
                    return traversalResult

            candidate = H(R(candidate, column))

"""Traverses a chain in the table to find the plaintext password once we've found a possible one
Postcondition: Returns plaintext password if successful; otherwise returns None
"""
def traverse_chain(hashedPassword, start):
    print("Traversing...")
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

    print("Cracked password: {0}".format(crack(H(password))))
    elapsed = time.time() - start
    print("Done in {0} mins, {1} secs.".format(int(elapsed / 60), elapsed % 60))
