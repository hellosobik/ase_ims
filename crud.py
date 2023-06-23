import sqlite3
import datetime
conn=sqlite3.connect("ase.sqlite", check_same_thread=False)

cursor=conn.cursor()

def update_current_stock(item_names_qty, time):
    date=str(time).split()[0]

    data=cursor.execute("""
    SELECT * FROM current_stock
    WHERE time Like '{}%';
    """.format(date))

    if len(data.fetchall())>0:
        cursor.execute("""
        UPDATE current_stock SET
        item_names_qty = ?,
        time = ?
        WHERE time Like ?
        """, (item_names_qty, time, date+'%'))

        return "success in updation"
    else:
        cursor.execute("""
        INSERT INTO current_stock 
        (item_names_qty, time)
        VALUES (?,?);
        """, (item_names_qty, time))

        return "success in insertion"
    
def push_new_stock(item_names_qty, a_s_invest, time):
    
    cursor.execute("""
    INSERT INTO new_stock 
    (item_names_qty, a_s_invest, time)
    VALUES (?,?,?);
    """, (item_names_qty, a_s_invest, time))

    update_current_stock(item_names_qty, time)

    return "new stock push to inventory"

    

item_names_qty=str({"parle":123, "oreo":456, "gooday":90})
time=str(datetime.datetime.now())
a_s_invest=1000
# time='2023-06-23 20:38:49.970614'

# msg=update_current_stock(item_names_qty=item_names_qty, time=time)
# print(msg)

msg=push_new_stock(item_names_qty=item_names_qty, time=time, a_s_invest=a_s_invest)
print(msg)

print("")
stock_table=cursor.execute("SELECT * FROM current_stock").fetchall()
new_inven=cursor.execute("SELECT * FROM new_stock").fetchall()
print(stock_table)
print(new_inven)
conn.commit()
conn.close()


