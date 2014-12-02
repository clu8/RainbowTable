#!/usr/bin/env python

import hashlib
import random
import string
import csv
import time

CHAIN_LENGTH = 4000

def createRainbowTable():
    rainbowTable = {}
    for i in range(100000):
        if i%5 == 0:
            print(i)
        start = ""
        for _ in range(6):
            start += random.choice(string.ascii_lowercase)
        plainText = start
        hash = ""
        for col in range(CHAIN_LENGTH):
            hash = hashlib.sha256(bytes(plainText, 'utf-8')).hexdigest()
            plainText = reduction(hash, col)
        rainbowTable[start] = hash
    with open('RainbowTable.csv', 'w') as table:
        writer = csv.writer(table)
        for start in rainbowTable:
            writer.writerow(start + ',' + rainbowTable[start])

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
            hash = hashlib.sha256(bytes(plainText, 'utf-8')).hexdigest()
            plainText = reduction(hash, col)
        rainbowTable[start] = hash
    with open('RainbowTable.csv', 'a') as table:
        writer = csv.writer(table)
        for start in rainbowTable:
            writer.writerow(start + ',' + rainbowTable[start])

def crack(hashedPassword):
    rainbowTable = {}
    with open('RainbowTable.csv', 'r') as table:
        reader = csv.reader(table)
        for row in reader:
            start = "".join(row[:6])
            hash = "".join(row[7:])
            rainbowTable[start] = hash
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
            candidate = hashlib.sha256(bytes(reduction(candidate, column), 'utf-8')).hexdigest()

def traverseChain(hashedPassword, start):
    print("traverse")
    for col in range(CHAIN_LENGTH):
        hash = hashlib.sha256(start).hexdigest()
        if hash == hashedPassword:
            return start
        start = reduction(hash, col)
    return 0

def reduction(hash, col):
    plainText = ""
    for i in range(6):
        x = ((10*int(hash[i], 16) + int(hash[i+1], 16)) + col) % 26
        plainText += string.ascii_lowercase[x] #abcdef...z
    return plainText

def test(password = ""):
    start = time.time()

    if password == "":
        for _ in range(6):
            password += random.choice(string.ascii_lowercase)

    hashedPassword = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()

    print("Cracked password: {0}".format(crack(hashedPassword)))
    elapsed = time.time() - start
    print("Elapsed: {0} mins, {1} secs.".format(int(elapsed / 60), elapsed % 60))

test('tester')