import sqlite3

conn=sqlite3.connect("ase.sqlite")

cursor=conn.cursor()

sql_query="""

CREATE TABLE create_stock (

sno integer PRIMARY KEY,
item_names text NOT NULL,
item_qtys text NOT NULL,
time text NOT NULL
)

"""

cursor.execute(sql_query)