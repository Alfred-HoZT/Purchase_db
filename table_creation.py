import sqlite3

def delete():
    tables = ['product', 'supplier', 'catalogue', 'purchased']
    with sqlite3.connect("purchases.db") as conn:
        c = conn.cursor()
        for tab in tables:
            c.execute(f"DROP TABLE IF EXISTS {tab}")

delete()

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
                    CAS_number INT,
                    PRIMARY KEY(catalogue_id),
                    FOREIGN KEY(supplier_id) REFERENCES purchased(purchase_id),
                    FOREIGN KEY(CAS_number) REFERENCES supplier(supplier_id)
                    )"""

create_purchased = """CREATE TABLE IF NOT EXISTS purchased (
                    purchase_id INTEGER,
                    date_of_order DATE,
                    requester VARCHAR(15),
                    wbs VARCHAR(20),
                    delivery_status DATE,
                    catalogue_id INT,
                    PRIMARY KEY(purchase_id),
                    FOREIGN KEY(catalogue_id) REFERENCES catalogue(catalogue_id)
                    )"""

conn = sqlite3.connect("purchases.db")
c = conn.cursor()

def creation():
    create_list = [create_supplier, create_product, create_catalogue, create_purchased]
    # with sqlite3.connect("purchases.db") as conn:
    #     c = conn.cursor()
    #     for action in create_list:
    #         c.execute(action)
    for action in create_list:
        c.execute(action)
        conn.commit()

creation()
