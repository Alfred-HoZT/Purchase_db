import sqlite3

def insert():
    with sqlite3.connect("purchase_db4.db") as conn:
        c = conn.cursor()
        query_product = "INSERT OR IGNORE INTO product (cas_number, name) VALUES (?,?)"
        query_supplier = "INSERT OR IGNORE INTO supplier (name) VALUES (?)"
        query_catalogue = """INSERT OR IGNORE INTO catalogue (catalogue_num, currency, unit_price, unit_qty, unit, website, supplier_id, cas_number)
                            VALUES (?,?,?,?,?,?,?,?)"""
        query_order = """INSERT OR IGNORE INTO purchase_order (date_of_order, requester, wbs, invoice_id, invoice_address, supplier_id)
                            VALUES (?,?,?,?,?,?)"""
        query_item = """INSERT OR IGNORE INTO item (catalogue_id, order_id, batch_num, exp_date, units_bought, units_received)
                            VALUES (?,?,?,?,?,?)"""
        
        queries = [query_product, query_supplier, query_catalogue, query_order, query_item]

        entries = [
            [("141-53-7","Sodium formate"), ("BLD Pharm",), ("BD151459 98%", "USD", 11, 500, "g", "https://www.bldpharm.com/products/141-53-7.html", 1, "141-53-7"), ("04/02/2022", "Alfred", "A-0008389-00-00", "001", None, 1), (1, 1, "10308", "31/06/2023", 10, 0)],
            [("6108-23-2","Lithium formate hydrate"), ("BLD Pharm",), ("BD306353 98%", "USD", 1, 500, "g", "https://www.bldpharm.com/products/6108-23-2.html", 1, "6108-23-2"), ("04/02/2022", "Alfred", "A-0008389-00-00", "001", None, 1), (2, 1, "ADK1101", "31/11/2024", 10, 0)],
            [("554-13-2","Lithium carbonate"), ("BLD Pharm",), ("BD136448 99+%", "USD", 56, 500, "g", "https://www.bldpharm.com/products/554-13-2.html", 1, "554-13-2"), ("04/02/2022", "Alfred", "A-0008389-00-00", "001", None, 1), (3, 1, "LI236J", "30/07/2026", 5, 0)],
            [("7487-88-9","Magnesium sulfate"), ("BLD Pharm",), ("BD137048 98%", "USD", 9, 500, "g", "https://www.bldpharm.com/products/7487-88-9.html", 1, "7487-88-9"), ("04/02/2022", "Alfred", "A-0008389-00-00", "001", None, 1), (4, 1, "MAG121J", "31/06/2023", 15, 0)],
            [("7487-88-9","Magnesium sulfate"), ("BLD Pharm",), ("BD137048 98%", "USD", 9, 500, "g", "https://www.bldpharm.com/products/7487-88-9.html", 1, "7487-88-9"), ("09/05/2022", "Wen", "A-0008389-00-00", "002", None, 1), (4, 2, "MAG122B", "31/08/2023", 10, 0)],
            [("7487-88-9","Magnesium sulfate"), ("BLD Pharm",), ("BD137048 98%", "USD", 15, 1, "kg", "https://www.bldpharm.com/products/7487-88-9.html", 1, "7487-88-9"), ("09/05/2022", "Wen", "A-0008389-00-00", "002", None, 1), (5, 2, "MAG123B", "31/08/2023", 5, 0)],
            [("7558-80-7","Sodium phosphate monobasic"), ("Sigma Aldrich",), ("S0751-500G", "SGD", 119.00, 500, "g", "https://www.sigmaaldrich.com/SG/en/product/sial/s0751", 2, "7558-80-7"), ("15/05/2022", "Alfred", "A-0008389-00-00", "003", None, 2), (6, 3, "LN22021", "15/10/2025", 10, 0)],
            
            # check again following line
            [("9001-99-4","Ribonuclease A from bovine pancreas"), ("Sigma Aldrich",), ("R4875-100MG", "SGD", 187.00, 100, "mg", "https://www.sigmaaldrich.com/SG/en/product/sigma/r4875", 2, "9001-99-4"), ("04/02/2022", "Alfred", "A-0008389-00-00", "004", None, 2), (7, 3, "MS1230", "30/01/2023", 20, 0)],
            [("6108-23-2","Lithium formate hydrate"), ("BLD Pharm",), ("BD306353 98%", "USD", 1, 500, "g", "https://www.bldpharm.com/products/6108-23-2.html", 1, "6108-23-2"), ("04/02/2022", "Alfred", "A-0008389-00-00", "004", None, 1), (2, 4, "LI347K", "30/07/2026", 5, 0)],
            [("6108-23-2","Lithium formate hydrate"), ("BLD Pharm",), ("BD306353 98%", "USD", 1, 500, "g", "https://www.bldpharm.com/products/6108-23-2.html", 1, "6108-23-2"), ("05/02/2022", "Alfred", "A-0008389-00-00", "005", None, 1), (2, 5, "LI347K", "30/07/2026", 5, 0)],
            [("6108-23-2","Lithium formate hydrate"), ("BLD Pharm",), ("BD306353 98%", "USD", 1, 500, "g", "https://www.bldpharm.com/products/6108-23-2.html", 1, "6108-23-2"), ("06/02/2022", "Alfred", "A-0008389-00-00", "006", None, 1), (2, 6, "LI347K", "30/07/2026", 5, 0)],
            [("6108-23-2","Lithium formate hydrate"), ("BLD Pharm",), ("BD306353 98%", "USD", 1, 500, "g", "https://www.bldpharm.com/products/6108-23-2.html", 1, "6108-23-2"), ("07/02/2022", "Alfred", "A-0008389-00-00", "007", None, 1), (2, 7, "LI347K", "30/07/2026", 5, 0)],
        ]

        for entry in entries:
            for query, e in zip(queries, entry):
                c.execute(query, e)
                
