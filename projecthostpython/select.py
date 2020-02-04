import sqlite3

conn = sqlite3.connect('TAGS.db')
print("Opened database successfully")

cursor = conn.execute("SELECT Filename,Auto_tag,Manual_tag,status from Tag")
for row in cursor:
   print("Filename = ", row[0],"Auto_tag = ", row[1],"Manual_tag = ", row[2],"status = ", row[3])

conn.close()