
'''2022-03-29	Wen	A-0008389-00-00	Magnesium sulfate	7487-88-9	BLD Pharm
BD137048 98%	USD 9 (500 g)	1	https://www.bldpharm.com/products/7487-88-9.html
'''

import sqlite3

conn = sqlite3.connect("purchases.db")
c = conn.cursor()

# def add_product(prod):
#     c.execute("INSERT INTO product VALUES (?)", prod)
#
# def remove_product(prod):
#     c.execute("DELETE FROM product WHERE product.name = prod")

def add_query(table, columns, val):
    # making an insert query to add new entities
    return f"INSERT INTO {table} (name) VALUES ('magnesium sulfate');" # need to refine: automate any no. of columns, and values.

def remove_query(table, col, val):
    # making a delete query to remove selected entities
    return f"DELETE FROM {table} WHERE {table}.{col} = '{val}';"

def query(request):
    if request == "Add":
        table = input("Which table? ")
        columns = get_columns(table)
        values = ask_input(columns)
        return add_query(table, columns, values)

    elif request == "Delete":
        table = input("Which table? ")
        col = input("Enter reference column: ")
        values = input("Enter reference value: ")
        return remove_query(table, col, values)

    else:
        print("Your request is denied. Please input the appropriate values.")
        call()

# def query(table, attr, request):
#     dic = {"Delete":("DELETE FROM", "WHERE)", "Add":("INSERT INTO", "VALUES"), "Show":("SELECT", "")} # to be aligned with GUI
#     act = dic[request]
#     try:
#         query = f"{act[0]} {table} {act[1]} ({attr})"
#         return query
#     except:
#         print("Your query is denied. Please try again.")

def read_query(query):
    with conn:
        print("-------- " + query + " --------")
        c.execute(query)
        print("Query approved.")


def get_columns(table):
    # returns the column headers
    with conn:
        data = c.execute(f"SELECT * FROM {table}")
    return tuple(map(lambda x: x[0], data.description))[1:]


def ask_input(columns):
    # depending on what columns there are, ask for each of them
    lst = []
    for col in columns:
        value = input(f"Enter value for '{col}': ")
        lst.append(value)
    return tuple(lst)


def call():
    request = input("""What do you want to do?
                    1) Add
                    2) Delete
                    """)

    read_query(query(request))

call()

# c.execute("SELECT * FROM product")
# print(c.fetchall())
