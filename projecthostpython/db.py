import sqlite3
conn = sqlite3.connect('TAGS.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE Tag
             (Filename TEXT NOT NULL, 
             Auto_tag TEXT, 
             Manual_tag TEXT, 
             status INT);''')

# # Insert a row of data
# c.execute("INSERT INTO COMPANY (ID,Filename,Auto_tag,Manual_tag,status) VALUES (1, 'file', 'Auto_tag','Manual_tag',0 )")
# # Save (commit) the changes
#c.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()


