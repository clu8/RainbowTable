#!/usr/bin/env python

# Use Python 3

import hashlib
import random
import string
import csv
import time

CHAIN_LENGTH = 4000 # 4000
ROWS = 10 # 100000
TABLE_FILE = "table.csv" # "RainbowTable.csv" for final, "table.csv" for testing
TABLE_FIELDNAMES = ['start_point', 'endpoint_hash']

def createRainbowTable():
    rainbowTable = {}
    for i in range(ROWS):
        if i % 5 == 0:
            print(i)

        start = ""
        for _ in range(6):
            start += random.choice(string.ascii_lowercase)

        plainText = start
        for col in range(CHAIN_LENGTH):
            hash = H(plainText)
            plainText = R(hash, col)
        rainbowTable[start] = hash

    with open(TABLE_FILE, 'w') as table:
        writer = csv.DictWriter(table, fieldnames=TABLE_FIELDNAMES)
        writer.writeheader()
        for start in rainbowTable:
            writer.writerow({TABLE_FIELDNAMES[0]: start, TABLE_FIELDNAMES[1]: rainbowTable[start]})

def expandRainbowTable():
    rainbowTable = {}
    for i in range(25000):
        if i%5 == 0:
            print(i)
        start = ""
        for _ in range(6):
            start += random.choice(string.ascii_lowercase)
        plainText = start
        hash = ""
        for col in range(CHAIN_LENGTH):
            plainText = R(H(plainText), col)
        rainbowTable[start] = hash
    with open(TABLE_FILE, 'a') as table:
        writer = csv.DictWriter(table, fieldnames=TABLE_FIELDNAMES)
        writer.writeheader()
        for start in rainbowTable:
            writer.writerow({TABLE_FIELDNAMES[0]: start, TABLE_FIELDNAMES[1]: rainbowTable[start]})

def crack(hashedPassword):
    rainbowTable = {}
    with open(TABLE_FILE, 'r') as table:
        reader = csv.DictReader(table)
        for row in reader:
            rainbowTable[row[TABLE_FIELDNAMES[0]]] = row[TABLE_FIELDNAMES[1]]

    candidate = hashedPassword
    for col in range(CHAIN_LENGTH):
        for column in range(col, CHAIN_LENGTH+1):
            if column%50 == 0:
                print(column)
            for start in rainbowTable:
                if rainbowTable[start] == candidate:
                    traversalResult = traverseChain(hashedPassword, start)
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
    plainText = ""
    for i in range(6):
        x = ((10*int(hash[i], 16) + int(hash[i+1], 16)) + col) % 26
        plainText += string.ascii_lowercase[x] #abcdef...z
    return plainText

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
    print("Elapsed: {0} mins, {1} secs.".format(int(elapsed / 60), elapsed % 60))