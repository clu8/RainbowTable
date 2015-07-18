RainbowTable
============

Initially developed for CS 55N with Dan Boneh at Stanford University in Autumn 2014.

Contains functionality to generate a rainbow table and crack password hashes given a hash function and reduction function. A reduction function for lowercase passwords of a given length is implemented. 

With a randomly generated rainbow table of 3 million rows and 1000 chain length, around 80%+ of 6-digit lowercase passwords hashed with SHA-256 can be cracked, with an average time per password (including failures) of 3 seconds. 