import sqlite3

conn = sqlite3.connect("bible_kjv.db")

cursor = conn.cursor()

cursor.execute('''SELECT * FROM t_kjv
                WHERE b = 1 AND c = 1''')

temp = cursor.fetchall()
print("\nGenesis 1\n")
for x in temp:
    print(f"Verse {x[3]}: {x[4]}")

conn.commit()
conn.close()
