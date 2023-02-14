import sqlite3

conn = sqlite3.connect('reviews.sqlite')

cursor = conn.cursor()
sql_query = """ CREATE TABLE reviews (
    id integer PRIMARY KEY,
    name text NOT NULL, 
    review text NOT NULL,
    rate integer NOT NULL
)"""

cursor.execute(sql_query)