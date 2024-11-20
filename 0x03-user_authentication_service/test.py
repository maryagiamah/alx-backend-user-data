#!/usr/bin/env python3

import sqlite3

# Connect to the SQLite file
connection = sqlite3.connect("a.db")

# Create a cursor
cursor = connection.cursor()

# Execute a query
cursor.execute("SELECT * FROM users;")

# Fetch results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
connection.close()
