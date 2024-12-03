# import sqlite3

# conn = sqlite3.connect('pz.db')
# cursor = conn.cursor()

# admin = [('admin', 'admin')]

# conn.execute('''create table if not exists ADMIN
#                   (name_id INTEGER PRIMARY KEY,
#                    USER varchar(20) NOT NULL,
#                    PASSWORD varchar(20) NOT NULL)''')
# # conn.executemany('INSERT INTO ADMIN_TABLE(USER, PASSWORD) VALUES (?,?)', admin)

# for i in conn.execute('SELECT * FROM ADMIN_TABLE'):
#     user = i[1]
#     pas = i[2]


# a = input('username :')
# b = input('password :')

# if a == user and b == pas:
#     print('admin')

# conn.commit()
# conn.close()

# User's password without echoing
# # Echoing password and masked with hashtag(#)
import maskpass # importing maskpass library

# prompt msg = Password and
# masking password with hashtag(#)
pwd = maskpass.askpass(prompt="Password:", mask="#")
print(pwd)


