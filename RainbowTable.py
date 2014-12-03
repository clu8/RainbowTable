#!/usr/bin/env python

# Use Python 3

import hashlib
import random
import string
import csv
import time

CHAIN_LENGTH = 1000
ROWS = 1000 # 3 * 10**6
TABLE_FILE = "table.csv" # "RainbowTable.csv" for final, "table.csv" for testing
TABLE_FIELDNAMES = ['start_point', 'endpoint_hash']

# Creates rainbow table using H() and R(), given ROWS, CHAIN_LENGTH, and TABLE_FILE
# Precondition: To expand, input number of rows as param expand; otherwise previous table will be erased
def createRainbowTable(expandRows = None):
    startTime = time.time()

    if expandRows:
        rows = expandRows
        flag = 'a'
    else:
        rows = ROWS
        flag = 'w'

    with open(TABLE_FILE, flag) as table:
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

def crack(hashedPassword):
    rainbowTable = {}
    with open(TABLE_FILE, 'r') as table:
        reader = csv.DictReader(table)
        for row in reader:
            rainbowTable[row[TABLE_FIELDNAMES[1]]] = row[TABLE_FIELDNAMES[0]]
            # rainbowTable: keys are endpoint hashes, values are start plaintexts

    candidate = hashedPassword
    for col in range(CHAIN_LENGTH):
        for column in range(col, CHAIN_LENGTH):
            if column % 50 == 0:
                print(column)

            if candidate in rainbowTable:
                traversalResult = traverseChain(hashedPassword, rainbowTable[candidate])
                if traversalResult != 0:
                    return traversalResult

            candidate = H(R(candidate, column))

def traverseChain(hashedPassword, start):
    print("traverse")
    for col in range(CHAIN_LENGTH):
        hash = H(start)
        if hash == hashedPassword:
            return start
        start = R(hash, col)
    return 0

# Hash function
# Precondition: Input plaintext as string
# Postcondition: Returns hash as string
def H(plaintext):
    return hashlib.sha256(bytes(plaintext, 'utf-8')).hexdigest()

# Reduction function
# Precondition: hash is H(previousPlaintext)
# Postcondition: returns randomly distributed 6-digit lowercase plaintext password
def R(hash, col):
    plaintextKey = (int(hash[:9], 16) ^ col) % 308915776 # 26**6
    plaintext = ""
    for _ in range(6):
        plaintext += string.ascii_lowercase[plaintextKey % 26]
        plaintextKey //= 26
    return plaintext

# Precondition: Input a 6 digit lowercase password to test, or input no arguments to generate a random password
# Postcondition: Cracks H(password) and prints elapsed time
def test(password = ""):
    start = time.time()

    if password == "":
        for _ in range(6):
            password += random.choice(string.ascii_lowercase)

    print("Cracking password: {0}\nH(password): {1}".format(password, H(password)))

    print("Cracked password: {0}".format(crack(H(password))))
    elapsed = time.time() - start
    print("Done in {0} mins, {1} secs.".format(int(elapsed / 60), elapsed % 60))
