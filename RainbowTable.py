#!/usr/bin/env python

import hashlib
import random
import string

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
