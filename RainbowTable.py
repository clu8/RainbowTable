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
            h = hashlib.sha256()
            h.update(plainText)
            hash = h.hexdigest()
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
            h = hashlib.sha256()
            h.update(plainText)
            hash = h.hexdigest()
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
        h = hashlib.sha256()
        h.update(reduction(candidate))
        candidate = h.hexdigest()

def traverseChain(hashedPassword, start):
    print "traverse"
    for _ in range(20000):
        h = hashlib.sha256()
        h.update(start)
        if h.hexdigest() == hashedPassword:
            return start
        start = reduction(h.hexdigest())
    return 0

# This is the stupidest piece of code I've ever written
def reduction(hash):
    plainText = ""
    for i in range(6):
        x = hash[i:i+2]
        x = 10*int(x[0], 16) + int(x[1], 16)
        x = x%26
        plainText += string.lowercase[x]
    return plainText

def test(testPassword = None):
    start = time.time()
    if testPassword is None:
        testPassword = ""
        for _ in range(6):
            testPassword += random.choice(string.ascii_lowercase)
    h = hashlib.sha256()
    h.update(testPassword)
    hashedPassword = h.hexdigest()
    print getPassword(hashedPassword)
    end = time.time()
    duration = end - start
    print "duration of search: " + str(int(duration/60)) + " min, " + str(duration%60) + " sec"

test()