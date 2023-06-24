import sqlite3
import datetime
conn=sqlite3.connect("ase.sqlite", check_same_thread=False)

cursor=conn.cursor()

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

def delete_table_data():
    cursor.execute("DELETE FROM change_in_stock")
    cursor.execute("DELETE FROM current_stock")
    cursor.execute("DELETE FROM new_stock")
    return("tables erased")


item_names_qty=str({"gooday":10, "parle":30})
# time=str(datetime.datetime.now())
a_s_invest=10000
time='2023-06-28 20:38:49.970614'
person_updated="sobik"
event="sold"

def task():

    # msg=update_current_stock(item_names_qty=item_names_qty, time=time)
    # print(msg)

    # msg=push_new_stock(item_names_qty=item_names_qty, time=time, a_s_invest=a_s_invest)
    # print(msg)

    # msg=record_change_in_stock(item_names_qty=item_names_qty, person_updated=person_updated, event=event, time=time)
    # print(msg)

    # print("")
    current_stock_table=cursor.execute("SELECT * FROM current_stock").fetchall()
    new_stock_table=cursor.execute("SELECT * FROM new_stock").fetchall()
    change_in_stock_table=cursor.execute("SELECT * FROM change_in_stock").fetchall()
    print("current_stock_table")
    print(current_stock_table)
    print("new_stock_table")
    print(new_stock_table)
    print("change_in_stock_table")
    print(change_in_stock_table)

    # print(dict(eval(get_current_stock(time)[0][1])))

# delete_table_data()
task()

# item_names_qty_past=cursor.execute("SELECT * FROM current_stock").fetchall()[-1][-2]
# print(item_names_qty_past)

conn.commit()
conn.close()


