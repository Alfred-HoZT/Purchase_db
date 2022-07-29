import sqlite3
import auto_insert_examples_4

def delete():
    tables = ['product', 'supplier', 'catalogue', 'purchase_order', 'item', 'lmms']
    with sqlite3.connect("purchase_db4.db") as conn:
        c = conn.cursor()
        for tab in tables:
            c.execute(f"DROP TABLE IF EXISTS {tab}")

create_supplier  = """CREATE TABLE IF NOT EXISTS supplier (
                    supplier_id INTEGER,
                    name VARCHAR(20) UNIQUE,
                    PRIMARY KEY(supplier_id)
                    )"""

create_product   = """CREATE TABLE IF NOT EXISTS product (
                    cas_number VARCHAR(20),
                    name VARCHAR(20) UNIQUE,
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
                    FOREIGN KEY(supplier_id) REFERENCES supplier(supplier_id),
                    FOREIGN KEY(cas_number) REFERENCES product(cas_number)
                    )"""

create_order = """CREATE TABLE IF NOT EXISTS purchase_order (
                    order_id INTEGER,
                    date_of_order DATE,
                    requester VARCHAR(15),
                    wbs VARCHAR(20),
                    delivery_status VARCHAR(20),
                    invoice_id VARCHAR(20) UNIQUE,
                    invoice_address VARCHAR(200),
                    supplier_id INT,
                    PRIMARY KEY(order_id),
                    FOREIGN KEY(supplier_id) REFERENCES supplier(supplier_id)
                    )"""

create_item = """CREATE TABLE IF NOT EXISTS item (
                    catalogue_id INTEGER,
                    order_id INTEGER,
                    batch_num VARCHAR(15),
                    exp_date DATE,
                    units_bought INTEGER,
                    units_received INTEGER DEFAULT 0,
                    PRIMARY KEY(catalogue_id, order_id),
                    FOREIGN KEY(catalogue_id) REFERENCES catalogue(catalogue_id),
                    FOREIGN KEY(order_id) REFERENCES purchase_order(order_id)
                    )"""

create_lmms = """CREATE TABLE IF NOT EXISTS lmms (
                    lmms VARCHAR UNIQUE,
                    catalogue_id INTEGER,
                    order_id INTEGER,
                    PRIMARY KEY(lmms),
                    FOREIGN KEY(catalogue_id) REFERENCES item(catalogue_id),
                    FOREIGN KEY(order_id) REFERENCES item(order_id)
                    )"""

create_catalogue_index = """CREATE UNIQUE INDEX catalogue_index 
                    ON catalogue (catalogue_num, unit_price, unit_qty, unit)"""

conn = sqlite3.connect("purchase_db4.db")
c = conn.cursor()

def creation():
    create_list = [create_supplier, create_product, create_catalogue, create_order, create_item, create_lmms, create_catalogue_index]
    # count = 0
    for action in create_list:
        c.execute(action)
        conn.commit()
        # count += 1

def restart(input):
    if input == "Yes":
        delete()
        creation()
        auto_insert_examples_4.insert()
        # c.execute("SELECT * FROM catalogue")
        # print("Cat:", c.fetchall())


"""
Uncomment -- restart("Yes") -- if you want to restart the database,
or -- restart("No") -- if you want to continue with what you have.
"""

# restart("Yes")
# restart("No")
