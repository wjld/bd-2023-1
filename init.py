import sqlite3

db = sqlite3.connect('./ratings.db')
cursor = db.cursor()

with open('schema.ddl','r') as schema:
    for query in schema.read().split(';'):
        cursor.execute(query.strip())