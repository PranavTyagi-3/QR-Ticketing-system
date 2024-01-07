import sqlite3

conn = sqlite3.connect("AutoQR.db")
cur=conn.cursor()

cur.execute("""insert into users values (
            "Innoxify",
            "securepass",
            "BF298P"
 )
            """)


conn.commit()
conn.close()