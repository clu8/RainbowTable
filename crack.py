#!/usr/bin/env python3

import rainbow

import hashlib
import string
import time
import random

"""SHA-256 hash function
Precondition: Input plaintext as string
Postcondition: Returns hash as string
"""
def sha256(plaintext):
	return hashlib.sha256(bytes(plaintext, 'utf-8')).hexdigest()

"""Returns a reduction function which generates an n-digit lowercase password from a hash
"""
def reduce_lower(n):
	"""Reduction function
	Precondition: hash is H(previousPlaintext)
	Postcondition: returns randomly distributed n-digit lowercase plaintext password
	"""
	def result(hash, col):
		plaintextKey = (int(hash[:9], 16) ^ col) % (26 ** n)
		plaintext = ""
		for _ in range(n):
			plaintext += string.ascii_lowercase[plaintextKey % 26]
			plaintextKey //= 26
		return plaintext
	return result

"""Returns a function which generates a random n-digit lowercase password
"""
def gen_lower(n):
	def result():
		password = ""
		for _ in range(n):
			password += random.choice(string.ascii_lowercase)
		return password
	return result

"""Precondition: Input a function which generates a random password, or input no arguments to generate a random password
Postcondition: Cracks H(password) and prints elapsed time
"""
def test(table, hash_function, gen_password_function, password=""):
	if password == "":
		password = gen_password_function()

	print("Cracking password: {0}\nH(password): {1}".format(password, hash_function(password)))

	cracked = table.crack(hash_function(password))
	if cracked:
		print("Success! Password: {0}".format(cracked))
		return True
	else:
		print("Unsuccessful :(")
		return False

# Tests random passwords multiple times and prints success rate and average crack time. 
def bulk_test(table, hash_function, gen_password_function, numTests):
	start = time.time()
	numSuccess = 0

	for i in range(numTests):
		print("\nTest {0} of {1}".format(i + 1, numTests))
		numSuccess += test(table, hash_function, gen_password_function)

	print("""\n{0} out of {1} random hashes were successful!\n
Average time per hash (including failures): {2} secs.""" \
		.format(numSuccess, numTests, (time.time() - start) / numTests))

table = rainbow.RainbowTable(sha256, reduce_lower(4), gen_lower(4))