#!/usr/bin/env python

#TODO: Avoid collisions -- possible reason for code not working
#TODO: Figure out best chain length and number of chains for rainbow table

import hashlib
import random
import string
import csv
import time

def createRainbowTable():
    rainbowTable = {}
    for i in range(25000):
        if i%5 == 0:
            print i
        start = ""
        for _ in range(6):
            start += random.choice(string.ascii_lowercase)
        plainText = start
        hash = ""
        for _ in range(20000):
            hash = hashlib.sha256(plainText).hexdigest()
            plainText = reduction(hash)
        rainbowTable[start] = hash
    with open('RainbowTable.csv', 'w') as table:
        writer = csv.writer(table)
        for start in rainbowTable:
            writer.writerow(start + ',' + rainbowTable[start])

def expandRainbowTable():
    rainbowTable = {}
    for i in range(25000):
        if i%5 == 0:
            print i
        start = ""
        for _ in range(6):
            start += random.choice(string.ascii_lowercase)
        plainText = start
        hash = ""
        for _ in range(20000):
            hash = hashlib.sha256(plainText).hexdigest()
            plainText = reduction(hash)
        rainbowTable[start] = hash
    with open('RainbowTable.csv', 'a') as table:
        writer = csv.writer(table)
        for start in rainbowTable:
            writer.writerow(start + ',' + rainbowTable[start])

def getPassword(hashedPassword):
    rainbowTable = {}
    with open('RainbowTable.csv', 'r') as table:
        reader = csv.reader(table)
        for row in reader:
            start = "".join(row[:6])
            hash = "".join(row[7:])
            rainbowTable[start] = hash
    candidate = hashedPassword
    for i in range(20000):
        if i%50 == 0:
            print i
        for start in rainbowTable:
            if rainbowTable[start] == candidate:
                traversalResult = traverseChain(hashedPassword, start)
                if traversalResult != 0:
                    return traversalResult
        candidate = hashlib.sha256(reduction(candidate)).hexdigest()

def traverseChain(hashedPassword, start):
    print("traverse")
    for _ in range(20000):
        hash = hashlib.sha256(start).hexdigest()
        if hash == hashedPassword:
            return start
        start = reduction(hash)
    return 0

def reduction(hash):
    plainText = ""
    for i in range(6):
        x = (10*int(hash[i], 16) + int(hash[i+1], 16)) % 26
        plainText += string.lowercase[x] #abcdef...z
    return plainText

def test(testPassword = None):
    start = time.time()

    if testPassword is None:
        testPassword = ""
        for _ in range(6):
            testPassword += random.choice(string.ascii_lowercase)

    hashedPassword = hashlib.sha256(testPassword).hexdigest()

    print("Cracked password: %s") % getPassword(hashedPassword)
    elapsed = time.time() - start
    print("Elapsed: %s mins, %s secs.") % (str(int(duration/60)), str(duration%60))

test('tester')