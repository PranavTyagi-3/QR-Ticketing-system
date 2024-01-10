import sqlite3

conn= sqlite3.connect('QRBuddy.db')
cursor = conn.cursor()

cursor.execute("""create table event (id INTEGER PRIMARY KEY AUTOINCREMENT,
               ClubName varchar(100),
                EventName varchar(100),
               Email varchar(50),
               EventDate varchar(50),
               FacultyCoordinator varchar(100),
               Semester varchar(50),
               StartTime varchar(50),
               EndTime varchar(50)
               ) ;""")
'''
# Fetch all the table names using fetchall()
table_names = cursor.fetchall()

# Close the cursor and the database connection
cursor.close()
conn.close()

# Extract the table names from the result and print them
for table in table_names:
    print(table[0])
cursor.execute("insert into users values('Edgetronix','p@sswo3d','G9JD87')")
'''
conn.commit()
conn.close()
print("Table Succesfully Created")