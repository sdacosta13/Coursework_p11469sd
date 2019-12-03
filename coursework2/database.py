import sqlite3

print(dir(sqlite3))
conn, cur = sqlite3.connect("data.db")
