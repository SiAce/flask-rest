import sqlite3

connnection = sqlite3.connect('data.db')

cursor = connnection.cursor()

# create_table = "CREATE TABLE users (id int, username text, password text)"
# cursor.execute(create_table)
#
# user = (1, 'jose', 'asdf')
# insert_query = "INSERT INTO users VALUES (?, ?, ?)"
# cursor.execute(insert_query, user)
#
# users = [
#     (2, 'rolf', 'asdf'),
#     (3, 'rose', 'qwer'),
#     (4, 'jazzy', 'efg')
# ]
# cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
result = cursor.execute(select_query)

print(result)
print(type(result))

print(next(result))
print(cursor.fetchone())

connnection.commit()

connnection.close()
