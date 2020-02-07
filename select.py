import sqlite3

conn = sqlite3.connect('projecthostpython/TAGS.db')
print("Opened database successfully")

cursor = conn.execute("SELECT Filename,Auto_tag,Manual_tag,Summary,status from Tag")
for row in cursor:
   print("Filename = ", row[0],"Auto_tag = ", row[1],"Manual_tag = ", row[2],"Summary = ", row[3],"status = ", row[4])

conn.close()