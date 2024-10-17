import os
import sqlite3
import random
import string
import hashlib

DEF_USERNAME = os.environ['DFR_USERNAME']
DEF_PASSWORD = os.environ['DFR_PASSWORD']

letters = string.ascii_letters
salt = ''.join(random.choice(letters) for i in range(10))

connection = sqlite3.connect('database.db')

with open('db_scripts.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

secret = f'{salt}{DEF_PASSWORD}'

pass_hash = hashlib.sha256(secret.encode('utf-8')).hexdigest()

cur.execute(
    'INSERT INTO users (username, pass, salt) VALUES (?, ?, ?)',
    (DEF_USERNAME, pass_hash, salt)
)

connection.commit()
connection.close()