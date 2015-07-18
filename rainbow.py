import csv
import pickle
import os
import string
import time

CSV_FIELDNAMES = ['start_point', 'endpoint_hash']

class RainbowTable:
	def __init__(self, hash_function, reduction_function, gen_password_function, chain_length=1000):
		self.table = {}
		self.H = hash_function
		self.R = reduction_function
		self.G = gen_password_function
		self.chain_length = chain_length

	"""Generates rainbow table using H() and R() with rows of chain_length hashes, 
	and also dumps it to pickle_file. Keys are endpoint hashes and values are start plaintexts.
	"""
	def generate(self, pickle_file="RainbowTable.pickle", rows=3*10**6, extend=False):
		startTime = time.time()
		if not extend:
			self.table = {}

		for i in range(rows):
			if i % 1000 == 0:
				print(i)

			start = self.G()

			plainText = start
			for col in range(self.chain_length):
				hashcode = self.H(plainText)
				plainText = self.R(hashcode, col)
			self.table[hashcode] = start

		pickle.dump(self.table, open(pickle_file, "wb"))

		elapsed = time.time() - startTime
		print("Done in {0} mins, {1} secs.".format(int(elapsed / 60), elapsed % 60))

	"""Clears self.table and reloads it from a pickle or CSV file.
	"""
	def load(self, filename="RainbowTable.pickle"):
		startTime = time.time()
		self.table = {}

		if filename.endswith('.csv'):
			print("Loading rainbow table from CSV...")
			with open(filename, 'r') as table:
				reader = csv.DictReader(table)
				for row in reader:
					self.table[row[CSV_FIELDNAMES[1]]] = row[CSV_FIELDNAMES[0]]
		else:
			print("Loading rainbow table from pickle...")
			self.table = pickle.load(open(filename, "rb"))

		print("Done loading in {0} secs.".format(time.time() - startTime))

	def export_csv(self, filename="RainbowTable.csv"):
		with open(filename, 'w') as table:
			writer = csv.DictWriter(table, fieldnames=CSV_FIELDNAMES)
			writer.writeheader()
			for k, v in self.table.items():
				writer.writerow({CSV_FIELDNAMES[0]: v, CSV_FIELDNAMES[1]: k})

	def crack(self, hashedPassword):
		for startCol in range(self.chain_length-1, -1, -1):
			candidate = hashedPassword
			for col in range(startCol, self.chain_length):
				candidate = self.H(self.R(candidate, col-1))
			if candidate in self.table:
				traversalResult = self.traverse_chain(hashedPassword, self.table[candidate])
				if traversalResult:
					return traversalResult

	"""Traverses a chain in the table to find the plaintext password once we've found a possible one
	Postcondition: Returns plaintext password if successful; otherwise returns None
	"""
	def traverse_chain(self, hashedPassword, start):
		for col in range(self.chain_length):
			hash = self.H(start)
			if hash == hashedPassword:
				return start
			start = self.R(hash, col)

		return None