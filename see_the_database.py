import sqlite3

import cursor as cursor

# Connect to the SQLite database
conn = sqlite3.connect("sqlitepassenger.db")

# Create a cursor object
cursor = conn.cursor()

# Execute a SELECT query to fetch data from the table
cursor.execute("SELECT * FROM passenger")

# Fetch all rows from the result set
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
