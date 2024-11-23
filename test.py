# from persiantools.jdatetime import JalaliDate
# import datetime

# print(JalaliDate.today())

# miladi = JalaliDate(1396,7,1).to_gregorian()

# print(miladi)

import sqlite3
data_person_name = [('amirrr','attary')]

con = sqlite3.connect("pz.db")



c = con.cursor()

# c.execute('''create table if not exists q1_person_name
#                  (name_id INTEGER PRIMARY KEY,
#                   first_name varchar(20) NOT NULL,
#                   last_name varchar(20) NOT NULL)''')
# c.executemany('INSERT INTO q1_person_name(first_name, last_name) VALUES (?,?)', data_person_name)
# c.execute('DELETE FROM paziresh WHERE tel = ""')
list_person_name = []
for row in c.execute('SELECT tel FROM paziresh '):
    a = list(row)
    list_person_name.append(a)
# print(list_person_name)
for i in list_person_name:
    a= int(i[0])
    print(a)
# b = a[0]
# b=int(b)
# print(b)
con.commit()
con.close()

# import sqlite3

# conn = sqlite3.connect('memo.db')
# cursor = conn.cursor()

# a=cursor.execute("SELECT name_id FROM q1_person_name ORDER BY name_id DESC LIMIT 1")
# last_id = cursor.lastrowid
# print(a)

# conn.commit()
# cursor.close()
# conn.close()

# import sqlite3 
# import io 
# conn = sqlite3.connect('pz.db') 

# # Open() function 
# with io.open('backupdatabase_dumpp.sql', 'w' ,encoding='utf-8') as p: 
		
# 	# iterdump() function 
# 	for line in conn.iterdump(): 
		
# 		p.write('%s\n' % line) 
	
# print(' Backup performed successfully!') 
# print(' Data Saved as backupdatabase_dump.sql') 

# conn.close() 


