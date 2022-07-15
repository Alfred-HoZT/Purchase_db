import sqlite3

def insert():
    with sqlite3.connect("purchase_db.db") as conn:
        c = conn.cursor()
        query_product = "INSERT OR IGNORE INTO product (cas_number, name) VALUES (?,?)"
        query_supplier = "INSERT OR IGNORE INTO supplier (name) VALUES (?)"
        query_catalogue = """INSERT OR IGNORE INTO catalogue (catalogue_num, currency, unit_price, unit_qty, unit, website, supplier_id, cas_number)
                            VALUES (?,?,?,?,?,?,?,?)"""
        query_purchase = """INSERT OR IGNORE INTO purchase (date_of_order, requester, wbs, units_bought, catalogue_id)
                            VALUES (?,?,?,?,?)"""
        
        queries = [query_product, query_supplier, query_catalogue, query_purchase]

        entries = [
            [("141-53-7","Sodium formate"), ("BLD Pharm",), ("BD151459 98%", "USD", 11, 500, "g", "https://www.bldpharm.com/products/141-53-7.html", 1, "141-53-7"), ("04/02/2022", "Alfred", "A-0008389-00-00", 10, 1)],
            [("6108-23-2","Lithium formate hydrate"), ("BLD Pharm",), ("BD306353 98%", "USD", 1, 500, "g", "https://www.bldpharm.com/products/6108-23-2.html", 1, "6108-23-2"), ("01/02/2022", "Alfred", "A-0008389-00-00", 5, 2)],
            [("554-13-2","Lithium carbonate"), ("BLD Pharm",), ("BD136448 99+%", "USD", 56, 500, "g", "https://www.bldpharm.com/products/554-13-2.html", 1, "554-13-2"), ("01/02/2022", "Alfred", "A-0008389-00-00", 8, 3)],
            [("7487-88-9","Magnesium sulfate"), ("BLD Pharm",), ("BD137048 98%", "USD", 9, 500, "g", "https://www.bldpharm.com/products/7487-88-9.html", 1, "7487-88-9"), ("15/05/2022", "Wen", "A-0008389-00-00", 5, 4)],
            [("7487-88-9","Magnesium sulfate"), ("BLD Pharm",), ("BD137048 98%", "USD", 15, 1, "kg", "https://www.bldpharm.com/products/7487-88-9.html", 1, "7487-88-9"), ("09/05/2022", "Wen", "A-0008389-00-00", 2, 5)],
            [("7558-80-7","Sodium phosphate monobasic"), ("Sigma Aldrich",), ("S0751-500G", "SGD", 119.00, 500, "g", "https://www.sigmaaldrich.com/SG/en/product/sial/s0751", 2, "7558-80-7"), ("15/05/2022", "Alfred", "A-0008389-00-00", 5, 6)],
            
            # check again following line
            [("7487-88-9","Magnesium sulfate"), ("BLD Pharm",), ("BD137048 98%", "USD", 9, 500, "g", "https://www.bldpharm.com/products/7487-88-9.html", 1, "7487-88-9"), ("30/06/2022", "Wen", "A-0008389-00-00", 5, 4)],
            [("9001-99-4","Ribonuclease A from bovine pancreas"), ("Sigma Aldrich",), ("R4875-100MG", "SGD", 187.00, 100, "mg", "https://www.sigmaaldrich.com/SG/en/product/sigma/r4875", 2, "9001-99-4"), ("03/02/2022", "Alfred", "A-0008389-00-00", 20, 8)],
            [("6108-23-2","Lithium formate hydrate"), ("BLD Pharm",), ("BD306353 98%", "USD", 1, 500, "g", "https://www.bldpharm.com/products/6108-23-2.html", 1, "6108-23-2"), ("02/02/2022", "Alfred", "A-0008389-00-00", 5, 2)],
            [("6108-23-2","Lithium formate hydrate"), ("BLD Pharm",), ("BD306353 98%", "USD", 1, 500, "g", "https://www.bldpharm.com/products/6108-23-2.html", 1, "6108-23-2"), ("03/02/2022", "Alfred", "A-0008389-00-00", 5, 2)],
            [("6108-23-2","Lithium formate hydrate"), ("BLD Pharm",), ("BD306353 98%", "USD", 1, 500, "g", "https://www.bldpharm.com/products/6108-23-2.html", 1, "6108-23-2"), ("04/02/2022", "Alfred", "A-0008389-00-00", 5, 2)],
            [("6108-23-2","Lithium formate hydrate"), ("BLD Pharm",), ("BD306353 98%", "USD", 1, 500, "g", "https://www.bldpharm.com/products/6108-23-2.html", 1, "6108-23-2"), ("05/02/2022", "Alfred", "A-0008389-00-00", 5, 2)],
        ]

        for entry in entries:
            for query, e in zip(queries, entry):
                c.execute(query, e)
                

# insert()

