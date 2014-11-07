#!/usr/bin/env python

#TODO: Write a reduction function
#TODO: Figure out best chain length and number of chains for rainbow table

import hashlib
import random
import string
import csv

def createRainbowTable():
    rainbowTable = {}
    for _ in range(3000):
        start = ""
        for _ in range(6):
            start += random.choice(string.ascii_lowercase)
        plainText = start
        for _ in range(100000):
            h = hashlib.sha256()
            h.update(plainText)
            hash = h.hexdigest()
            plainText = hash[:6]
        rainbowTable[start] = hash
    with open('RainbowTable.csv', 'w') as table:
        writer = csv.writer(table)
        for start in rainbowTable:
            writer.writerow(start + ',' + rainbowTable[start])

def expandRainbowTable():
    rainbowTable = {}
    for _ in range(500):
        start = ""
        for _ in range(6):
            start += random.choice(string.ascii_lowercase)
        plainText = start
        for _ in range(100000):
            h = hashlib.sha256()
            h.update(plainText)
            hash = h.hexdigest()
            plainText = hash[:6]
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
    for _ in range(100000):
        for start in rainbowTable:
            if rainbowTable[start] == hashedPassword:
                return traverseChain(hashedPassword, start)
        h = hashlib.sha256()
        h.update(hashedPassword[:6])
        hashedPassword = h.hexdigest()

def traverseChain(hashedPassword, start):
    while True:
        h = hashlib.sha256()
        h.update(start)
        if h.hexdigest() == hashedPassword:
            return start
        start = h.hexdigest()[:6]

def test(testPassword = None):
    if testPassword is None:
        testPassword = ""
        for _ in range(6):
            testPassword += random.choice(string.ascii_lowercase)
    h = hashlib.sha256()
    h.update(testPassword)
    hashedPassword = h.hexdigest()
    print getPassword(hashedPassword)


test("jialin")
