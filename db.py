import sqlite3

conn=sqlite3.connect("ase.sqlite", check_same_thread=False)

cursor=conn.cursor()

sql_query=["""

CREATE TABLE new_stock (

sno integer PRIMARY KEY,
item_names_qty text NOT NULL,
a_s_invest text NOT NULL,
time text NOT NULL
)

""",
#current stock will be as per day
"""
CREATE TABLE current_stock (

sno integer PRIMARY KEY,
item_names_qty text NOT NULL,
time text NOT NULL
)

""",
#person updated -> Amartya or sobik
#event -> sold, consumed, lost

"""
CREATE TABLE change_in_stock (

sno integer PRIMARY KEY,
item_names_qty text NOT NULL,
person_updated text NOT NULL,
event text NOT NULL,
time text NOT NULL
)

""",

"""
CREATE TABLE current_sale (

sno integer PRIMARY KEY,
item_person_qty text NOT NULL,
time text NOT NULL
)
 """
           
           ]
for i in sql_query:

    cursor.execute(i)