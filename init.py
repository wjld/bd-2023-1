import sqlite3

db = sqlite3.connect('./ratings.db')
cursor = db.cursor()

with open('rating.ddl','r') as schema:
    last: str = ''
    for query in schema.read().split(';'):
        if 'begin' in query:
           last = query
           continue
        elif 'begin' in last:
           query = last + ';' + query
           last = ''
        cursor.execute(query.strip())