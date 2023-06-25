import sqlite3
import datetime
conn=sqlite3.connect("ase.sqlite", check_same_thread=False)
from pprint import pprint
cursor=conn.cursor()

"""
functions to perform
create and update operations
"""

def get_current_stock(time):
    date=str(time).split()[0]

    data=cursor.execute("""
    SELECT * FROM current_stock
    WHERE time Like '{}%';
    """.format(date))
    data=data.fetchall()
    # print(data)
    return data

def add_sub(task, item_names_qty, time):
    item_names_qty=dict(eval(item_names_qty))
    if len(cursor.execute("SELECT * FROM current_stock").fetchall())==0:
        item_names_qty_past=dict()
        item_names_qty_past=item_names_qty
        # print(item_names_qty_past)
        # print("current stock is 0")
        return str(item_names_qty_past)
    elif len(get_current_stock(time))==0 and task=="sub":
        item_names_qty_past=dict(eval(cursor.execute("SELECT * FROM current_stock").fetchall()[-1][-2]))
        for i in item_names_qty.keys():
            if i in item_names_qty_past:
                item_names_qty_past[i]-=item_names_qty[i]
            # item_names_qty_past.update(item_names_qty)
            # print(item_names_qty_past)
        return str(item_names_qty_past)
    elif len(get_current_stock(time))==0 and task=="add":
        item_names_qty_past=dict(eval(cursor.execute("SELECT * FROM current_stock").fetchall()[-1][-2]))
        for i in item_names_qty.keys():
            if i in item_names_qty_past:
                item_names_qty_past[i]+=item_names_qty[i]
            else:
                item_names_qty_past[i]=item_names_qty[i]
            # item_names_qty_past.update(item_names_qty)
            # print(item_names_qty_past)
        return str(item_names_qty_past)
    else:
        # print("current stock is not 0")
        item_names_qty_past=dict(eval(get_current_stock(time)[0][1]))
        if task=="add":
            for i in item_names_qty.keys():
                if i in item_names_qty_past:
                    item_names_qty_past[i]+=item_names_qty[i]
                else:
                    item_names_qty_past[i]=item_names_qty[i]
            # item_names_qty_past.update(item_names_qty)
            # print(item_names_qty_past)
            return str(item_names_qty_past)
        elif task =="sub":
            for i in item_names_qty_past.keys():
                if i in item_names_qty:
                    item_names_qty_past[i]-=item_names_qty[i]
            # item_names_qty_past.update(item_names_qty)
            # print(item_names_qty_past)
            return str(item_names_qty_past)

        

def update_current_stock(item_names_qty, time):
    
    data = get_current_stock(time)
    date=str(time).split()[0]

    if len(data)>0:
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

    item_names_qty=add_sub(task="add", item_names_qty=item_names_qty, time=time)

    update_current_stock(item_names_qty, time)

    return "new stock push to inventory"

def record_change_in_stock(item_names_qty, person_updated, event, time):
    cursor.execute("""
    INSERT INTO change_in_stock 
    (item_names_qty, person_updated, event, time)
    VALUES (?,?,?,?);
    """, (item_names_qty, person_updated, event, time))
    item_names_qty=add_sub(task="sub", item_names_qty=item_names_qty, time=time)
    update_current_stock(item_names_qty, time)
    return "change in stock recorded"

"""
functions to perform read opeations
"""
def read_past_tranctions(num):
    no_of_rows=int(cursor.execute("SELECT COUNT(*) FROM change_in_stock").fetchone()[0])
    num1=no_of_rows/10
    start_id=(num*10)+ 1
    if num == num1:
        end_id=no_of_rows 
    else:
        end_id=(num+1)*10
    results=cursor.execute("""SELECT * FROM 
    change_in_stock WHERE sno 
    BETWEEN ? AND ?""", 
    (start_id, end_id)).fetchall()[::-1]
    return results

def update_current_day_sale(time, person, item_names_qty):
    date=str(time).split()[0]

    # today=cursor.execute("""SELECT * FROM current_sale
    # WHERE time LIKE '{}%';
    # """.format(date)).fetchall()

    # users=cursor.execute("""SELECT DISTINCT person_updated
    #  FROM change_in_stock WHERE
    #    time LIKE '{}%'""".format(date)).fetchall()

    # users_lst=list()
    # for i in users:
    #     pprint(i)
    #     users_lst.append(i[0])

    # if len(today)==0:
    #     cursor.execute("""INSERT INTO current_sale
    #     (item_person_qty, time) VALUES (?,?) WHERE
    #     time LIKE ?;""", ())
    

    
    # return users_lst
    
def task(op):
    if op=="new":
        msg=push_new_stock(item_names_qty=item_names_qty, time=time, a_s_invest=a_s_invest)
        print(msg)
    elif op=="change":
        msg=record_change_in_stock(item_names_qty=item_names_qty, person_updated=person_updated, event=event, time=time)
        print(msg)

    # print("")
    current_stock_table=cursor.execute("SELECT * FROM current_stock").fetchall()
    new_stock_table=cursor.execute("SELECT * FROM new_stock").fetchall()
    change_in_stock_table=cursor.execute("SELECT * FROM change_in_stock").fetchall()
    print("")
    pprint("current_stock_table")
    pprint(current_stock_table)
    print("")
    pprint("new_stock_table")
    pprint(new_stock_table)
    print("")
    pprint("change_in_stock_table")
    pprint(change_in_stock_table)


def delete_table_data():
    cursor.execute("DELETE FROM change_in_stock")
    cursor.execute("DELETE FROM current_stock")
    cursor.execute("DELETE FROM new_stock")
    return("tables erased")


    # print(dict(eval(get_current_stock(time)[0][1])))

item_names_qty=str({"gooday":1000, "parle":3000, "bourbon":4000, "namkeen":6000, "cake":8000})
item_names_qty=str({"gooday":1, "parle":3, "bourbon":4, "namkeen":6, "cake":8})
time=str(datetime.datetime.now())
a_s_invest=10000
# time='2023-06-31 20:38:49.970614'
person_updated="sobik"
event="sold"

# delete_table_data()
# task(op="change")
# pprint(read_past_tranctions(num=1))
# pprint(cursor.execute("SELECT * FROM current_stock").fetchall())
# item_names_qty_past=cursor.execute("SELECT * FROM current_stock").fetchall()[-1][-2]
# print(item_names_qty_past)

for i in range(0,5):
    time='2023-07-0{} 20:38:49.970614'.format(i+1)
    task(op="new")

# pprint(current_day_sale(time=time))

conn.commit()
conn.close()


