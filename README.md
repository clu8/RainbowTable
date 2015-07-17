RainbowTable
============

Initially developed for CS 55N, Autumn 2014 with Dan Boneh at Stanford University.

Contains functionality to generate a rainbow table and crack a hash for 6-digit lowercase passwords.

With a randomly generated rainbow table of 3 million rows and 1000 chain length, around 80%+ of passwords can be cracked, with an average time per password (including failures) of 3 seconds with SHA-256.