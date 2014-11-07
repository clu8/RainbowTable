#!/usr/bin/env python

import hashlib
import random
import string

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
    return rainbowTable

def expandRainbowTable(rainbowTable):
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
    return rainbowTable

def getPassword(hashedPassword, rainbowTable):
    while True:
        for start in rainbowTable:
            if rainbowTable[start] == hashedPassword:
                return traverseChain(hashedPassword, rainbowTable, start)
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
