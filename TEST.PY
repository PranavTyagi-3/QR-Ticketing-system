import sqlite3

conn= sqlite3.connect('AutoQR.db')
cursor = conn.cursor()
"""
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all the table names using fetchall()
table_names = cursor.fetchall()

# Close the cursor and the database connection
cursor.close()
conn.close()

# Extract the table names from the result and print them
for table in table_names:
    print(table[0])
"""
cursor.execute("insert into users values('Edgetronix','p@sswo3d','G9JD87')")
conn.commit()
conn.close()