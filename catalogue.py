
'''2022-03-29	Wen	A-0008389-00-00	Magnesium sulfate	7487-88-9	BLD Pharm
BD137048 98%	USD 9 (500 g)	1	https://www.bldpharm.com/products/7487-88-9.html
'''

import sqlite3

conn = sqlite3.connect("purchases.db")
c = conn.cursor()

# with conn:
#     c.execute("SELECT * FROM catalogue")
#     print(c.fetchall())

with conn:
    # clear the table 'catalogue'
    c.execute("""DELETE FROM catalogue""")


def add_catalogue(catalogue_num, currency, unit_price, unit_qty, unit, website, supplier_id, CAS_number):
    with conn:
        c.execute("""INSERT INTO catalogue (catalogue_num, currency, unit_price, unit_qty, unit, website, supplier_id, CAS_number)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (catalogue_num, currency, unit_price, unit_qty, unit, website, supplier_id, CAS_number)
                    )


def remove_catalogue(cat_num):
    # eg. remove_catalogue("BD137048 98%")
    with conn:
        c.execute("""DELETE FROM catalogue WHERE catalogue.catalogue_num = ?""", (cat_num,))

def update_catalogue():
    # relate to which column: create a new row in catalogue table
    # check whether the particular data already exists within the table. (all must tally)
    # add a date column under catalogue table - when the information was checked (timestamp)


def show_by_catalogue(catalogue_num = None):
    # by default returns all catalogues, but option given to specify catalogue_num
    # eg. show_by_catalogue("BD137048 98%")
    with conn:
        if not catalogue_num:
            c.execute("""SELECT * FROM catalogue""")
        else:
            c.execute("""SELECT * FROM catalogue WHERE catalogue.catalogue_num = catalogue_num""")

        print(c.fetchall())


def show_by_cas(cas_number, limit = None):
    # eg. show_by_cas("7485-88-9")
    with conn:
        if not limit:
            c.execute("""SELECT * FROM catalogue WHERE catalogue.cas_number = ? ORDER BY unit_price ASC""", (cas_number,))
        else:
            c.execute("""SELECT * FROM catalogue WHERE catalogue.cas_number = ? ORDER BY unit_price ASC LIMIT ?""", (cas_number, limit))

        print(c.fetchall())


add_catalogue('BD137048 98%', 'USD', '9', '500', 'g', 'https://www.bldpharm.com/products/7487-88-9.html', '1', '7485-88-9') # BLD Pharm, magnesium sulfate
add_catalogue('M7506-500G', 'USD', '237', '500', 'g', 'https://www.sigmaaldrich.com/SG/en/product/sigald/m7506', '2', '7485-88-9') # Sigma Aldrich, magnesium sulfate
add_catalogue('BD305858 98%', 'USD', '22', '500', 'g', 'https://www.bldpharm.com/products/546-93-0.html', '1', '546-93-0') # BLD Pharm, magnesium sulfate

show_by_catalogue()
print("--------------")
show_by_cas('7485-88-9')
print("--------------")
remove_catalogue('BD137048 98%')
show_by_catalogue()


# with conn:
#     c.execute("""INSERT INTO catalogue (catalogue_num, currency, unit_price, unit_qty, unit, website, supplier_id, CAS_number)
#                     VALUES ('BD137048 98%', 'USD', '9', '500', 'g', 'https://www.bldpharm.com/products/7487-88-9.html', '1', '7485-88-9');
#                 """)


# with conn:
#     c.execute("SELECT * FROM catalogue")
#     print(c.fetchall())
