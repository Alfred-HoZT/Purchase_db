import sqlite3
import auto_insert_examples

def delete():
    tables = ['product', 'supplier', 'catalogue', 'purchase', 'purchased_item']
    with sqlite3.connect("purchase_db.db") as conn:
        c = conn.cursor()
        for tab in tables:
            c.execute(f"DROP TABLE IF EXISTS {tab}")

create_supplier  = """CREATE TABLE IF NOT EXISTS supplier (
                    supplier_id INTEGER,
                    name VARCHAR(20),
                    PRIMARY KEY(supplier_id)
                    )"""

create_product   = """CREATE TABLE IF NOT EXISTS product (
                    cas_number VARCHAR(20),
                    name VARCHAR(20),
                    PRIMARY KEY(cas_number)
                    )"""

create_catalogue = """CREATE TABLE IF NOT EXISTS catalogue (
                    catalogue_id INTEGER,
                    catalogue_num VARCHAR(30),
                    currency VARCHAR(3),
                    unit_price DECIMAL(5, 3),
                    unit_qty DECIMAL(5, 3),
                    unit VARCHAR(5),
                    website VARCHAR(200),
                    supplier_id INT,
                    cas_number INT,
                    PRIMARY KEY(catalogue_id),
                    FOREIGN KEY(supplier_id) REFERENCES purchased(purchase_id),
                    FOREIGN KEY(CAS_number) REFERENCES supplier(supplier_id)
                    )"""

create_purchase = """CREATE TABLE IF NOT EXISTS purchase (
                    purchase_id INTEGER,
                    date_of_order DATE,
                    requester VARCHAR(15),
                    wbs VARCHAR(20),
                    delivery_status VARCHAR(20),
                    units_bought INTEGER,
                    quote_id VARCHAR(15),
                    catalogue_id INT,
                    PRIMARY KEY(purchase_id),
                    FOREIGN KEY(catalogue_id) REFERENCES catalogue(catalogue_id)
                    )"""

create_purchased_item = """CREATE TABLE IF NOT EXISTS purchased_item (
                    lmms VARCHAR(15),
                    mass_volume INTEGER,
                    unit VARCHAR(5),
                    batch_num VARCHAR(15),
                    exp_date DATE,
                    purchase_id INTEGER,
                    PRIMARY KEY(lmms),
                    FOREIGN KEY(purchase_id) REFERENCES purchase(purchase_id)
                    )"""

conn = sqlite3.connect("purchase_db.db")
c = conn.cursor()

def creation():
    create_list = [create_supplier, create_product, create_catalogue, create_purchase, create_purchased_item]
    for action in create_list:
        c.execute(action)
        conn.commit()

def restart(input):
    if input == "Yes":
        delete()
        creation()
        auto_insert_examples.insert()


"""
Uncomment -- restart("Yes") -- if you want to restart the database,
or -- restart("No") -- if you want to continue with what you have.
"""

# restart("Yes")
# restart("No")
