import sqlite3
import json

connector = sqlite3.connect("test.db")
cursor    = connector.cursor()

cursor.execute("select * from menu")
d = { "itemList": [ { 'name':  row[0], 'price': row[1], 'value': row[2] } for row in cursor.fetchall()] }

print(d)
print(json.dumps(d))

cursor.close()
connector.close()
