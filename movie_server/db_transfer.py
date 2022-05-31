import sqlite3

connection1 = sqlite3.connect('cinema.db')
cursor1 = connection1.cursor()

# rows = cursor1.execute("SELECT id, title, image, runtime_hrs, runtime_mins, rating FROM movies").fetchall()
# print(rows)

connection2 = sqlite3.connect('db.sqlite3')
cursor2 = connection2.cursor()

# for record in rows:
#     print(record)
#     cursor2.execute("INSERT INTO ticket_handler_movie VALUES (?, ?, ?, ?, ?, ?)", record)
#
# connection2.commit()

rows = cursor1.execute("SELECT id, date, time, ticket_price, seats_available, seats_total, movie FROM showings").fetchall()
print(rows)

for record in rows:
    print(record)
    cursor2.execute("INSERT INTO ticket_handler_showing VALUES (?, ?, ?, ?, ?, ?, ?)", record)

connection2.commit()

rows = cursor1.execute("SELECT id, ticket_code, ticket_type, ticket_used, buyer, showing FROM tickets").fetchall()
print(rows)

for record in rows:
    print(record)
    cursor2.execute("INSERT INTO ticket_handler_ticket VALUES (?, ?, ?, ?, ?, ?)", record)

connection2.commit()

