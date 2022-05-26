
'''2022-03-29	Wen	A-0008389-00-00	Magnesium sulfate	7487-88-9	BLD Pharm
BD137048 98%	USD 9 (500 g)	1	https://www.bldpharm.com/products/7487-88-9.html
'''

import sqlite3

conn = sqlite3.connect("purchases.db")
c = conn.cursor()

with conn:
    # clear the table 'purchased'
    c.execute("""DELETE FROM purchased""")


def add_purchase(date_of_order, requester, wbs, delivery_status, catalogue_id):
    with conn:
        c.execute("""INSERT INTO purchased (date_of_order, requester, wbs, delivery_status, catalogue_id)
                        VALUES (?, ?, ?, ?, ?);
                    """,
                    (date_of_order, requester, wbs, delivery_status, catalogue_id)
                    )

def remove_purchase(purchase_id):
    with conn:
        c.execute("""DELETE FROM purchased WHERE purchased.purchased_id = ?""", (purchase_id,))


def find_purchase_id(catalogue_id):
    with conn:
        id = c.execute("""SELECT purchase_id FROM purchased WHERE purchased.catalogue_id = catalogue_id""")
        return id


def show_by_date(date):
    with conn:
        c.execute("""SELECT * FROM purchased WHERE purchased.date_of_order = ? ORDER BY purchased.date_of_order ASC""", (date,))
        print(c.fetchall())


# need to work on. Make generable selection.
def show_by(criteria, value):
    with conn:
        c.execute(f"""SELECT * FROM purchased WHERE purchased.{criteria} = {value} ORDER BY purchased.{criteria} ASC;""")
        print(c.fetchall())


# How will user know purchase_id? What will they put?
def delivered(date, purchase_id):
    with conn:
        c.execute("""UPDATE purchased SET purchased.delivery_status = ? WHERE purchased.purchase_id = ?""", (date, purchase_id))


add_purchase('2022-03-29', 'Wen', 'A-0008389-00-00 ', '2022-04-03', '1')
add_purchase('2022-03-29', 'Wen', 'A-0008389-00-00 ', '2022-04-03', '2')
add_purchase('2022-04-03', 'Wen', 'A-0008389-00-00 ', 'Null', '1')
add_purchase('2022-04-20', 'Wen', 'A-0008389-00-00 ', 'Null', '3')

show_by_date("2022-03-29")
print("--------------")
# show_by('date_of_order', "2022-03-29")

show_by_date("2022-04-03")
print("--------------")
# delivered("2022-05-01", "3")
show_by_date("2022-04-03")
