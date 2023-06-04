import sqlite3

conn=sqlite3.connect("ase.sqlite", check_same_thread=False)

cursor=conn.cursor()

sql_query_list={

#create
"insert_new_stock":
"""
INSERT INTO create_stock
(item_names, item_qtys, a_s_invest, time)
VALUES (?, ?, ?, ?);
"""
,
"change_in_stock":
"""
INSERT INTO change_in_stock
(item_names, item_qtys, person_updated, event, time)
VALUES (?, ?, ?, ?, ?);
"""
,
"current_stock":[
"""
INSERT INTO current_stock 
(item_names, item_qtys, time)
VALUES (?, ?, ?);
""" 
    ,
"""
UPDATE current_stock SET 
item_names = {item_names},
item_qtys = {item_qtys},
time = {time}
WHERE time Like '{date}%';
"""
]
,

#read

"read_create_stock":"SELECT * FROM create_stock",
"read_current_stock":"SELECT * FROM current_stock",
"read_change_in_stock":"SELECT * FROM change_in_stock",

#update


#delete

}

def current_stock(date):
    data=cursor.execute("""
    SELECT * FROM current_stock
    WHERE time Like '{date}%';
    """)
    if len(data.fetchall())>0:
        return sql_query_list["current_stock"][1]
    else:
        return sql_query_list["current_stock"][0]



