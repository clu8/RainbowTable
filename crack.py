#!/usr/bin/env python3

import rainbow

import hashlib
import string
import time
import random

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
def test(table, password=""):
    if password == "":
        for _ in range(6):
            password += random.choice(string.ascii_lowercase)

    print("Cracking password: {0}\nH(password): {1}".format(password, H(password)))

    cracked = table.crack(H(password))
    if cracked:
        print("Success! Password: {0}".format(cracked))
        return True
    else:
        print("Unsuccessful :(")
        return False

# Tests random passwords multiple times and prints success rate and average crack time. 
def bulk_test(table, numTests):
    start = time.time()
    numSuccess = 0

    for i in range(numTests):
        print("\nTest {0} of {1}".format(i + 1, numTests))
        numSuccess += test(table)

    print("""\n{0} out of {1} random hashes were successful!\n
Average time per hash (including failures): {2} secs.""" \
        .format(numSuccess, numTests, (time.time() - start) / numTests))

table = rainbow.RainbowTable(H, R)