from tkinter import *
from tkcalendar import Calendar
from tkinter import ttk
import sqlite3
from datetime import date
from tkinter import filedialog
from table_creation import *
# from data_package import *

"""
- README - 
1. Only execute this file. On execution, app will prompt if you want to reset the database to the original data. Click accordingly.
2. The top row allows switching between 3 different views, Main, Receive and Search.
3. Main Frame - User can add new product details into database. Click "Submit" to finalise details.
4. Receive Frame - does not perform any function currently.
5. Search Frame - top row with search function does not work. Otherwise, can click "Go" to show all rows in database.
-> Double clicking on each row will fill all entry boxes below accordingly. 
-> User can change details and click on "Submit" to confirm changes.
-> Click on "Go" again to view changes made. 
-> Note that changes to Catalogue Number, CAS Number, Product Name and Supplier Name will change for all rows. (to be rectified)
"""

root = Tk()
root.title("Purchase Database")
root.geometry("1200x600")

# Popup window feature to ask if user wants to reset the database 
def restart_yes():
    restart("Yes")
    restart_frame.destroy()

restart_frame = Toplevel(root)
restart_label = Label(restart_frame, text="Do you want to reset the database?")
restart_yes_btn = Button(restart_frame, text="Yes", command=restart_yes)
restart_no_btn = Button(restart_frame, text="No", command=restart_frame.destroy)

restart_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
restart_yes_btn.grid(row=1, column=0, padx=20, pady=20)
restart_no_btn.grid(row=1, column=1, padx=20, pady=20)
restart_frame.attributes('-topmost', True)

#---------------------------------------------------------#
## Creating a fullscreen scrollbar
# Create a master frame
master_frame = Frame(root)
master_frame.pack(fill=BOTH, expand=1)

# Create A Canvas
master_canvas = Canvas(master_frame, bg='white')
master_canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Add A Scrollbar To The Canvas
fullscreen_scrollbar = ttk.Scrollbar(master_frame, orient=VERTICAL, command=master_canvas.yview)
fullscreen_scrollbar.pack(side=RIGHT, fill=Y)

# Configure The Canvas
master_canvas.configure(yscrollcommand=fullscreen_scrollbar.set)
master_canvas.bind('<Configure>', lambda e: master_canvas.configure(scrollregion = master_canvas.bbox("all")))

# Creating the second frame in master_canvas
second_frame = Frame(master_canvas)

root.update_idletasks() 
height = root.winfo_height()
width = root.winfo_width()

# Add the second frame to a window in the canvas
master_canvas.create_window((width/2, 0), window=second_frame, anchor='n')
def centerCanvasOrigin(e):
    root.update()

# master_canvas.bind("<Configure>", centerCanvasOrigin)

#---------------------------------------------------------#
# Connect to database 
conn = sqlite3.connect("purchase_db.db")
c = conn.cursor()

# Main function
def main():
    search_frame.pack_forget()
    receive_frame.pack_forget()
    main_frame.pack()

sql_columns = {
    "Date" : "purchase.date_of_order",
    "Requester" : "purchase.requester",
    "WBS" : "purchase.wbs",
    "Product Name" : "product.name",
    "CAS Number" : "product.cas_number",
    "Supplier" : "supplier.name",
    "Catalogue Number" : "catalogue.catalogue_num",
    "Currency" : "catalogue.currency",
    "Unit Price" : "catalogue.unit_price",
    "Unit Quantity" : "catalogue.unit_qty",
    "Unit" : "catalogue.unit",
    "Units Bought" : "purchase.units_bought",
    "Website" : "catalogue.website"
}

def reset_tree():
    # Delete existing rows
    x = my_tree.get_children()
    for record in x:
        my_tree.delete(record)
    
    conn = sqlite3.connect("purchase_db.db")
    c = conn.cursor()

    query_value = "%" + query.get() + "%"
    search_cond = query_var_update.get()
    records = []
    # print(sql_columns.values())

    if search_cond == "Search All":
        if not query.get():
            c.execute("""SELECT purchase.purchase_id, date_of_order, requester, wbs, product.name, product.cas_number, 
                supplier.name, catalogue.catalogue_id, catalogue_num, currency, unit_price, unit_qty, unit, units_bought, website 
                FROM catalogue JOIN product ON product.cas_number=catalogue.cas_number 
                JOIN supplier ON supplier.supplier_id=catalogue.supplier_id
                JOIN purchase ON purchase.catalogue_id=catalogue.catalogue_id""")
            # print(c.fetchall)
            records = c.fetchall()
        else:
            for cond in sql_columns.values():
                sql_command = f"""SELECT purchase.purchase_id, purchase.date_of_order, purchase.requester, purchase.wbs, product.name, product.cas_number, 
                    supplier.name, catalogue.catalogue_id, catalogue.catalogue_num, catalogue.currency, catalogue.unit_price, catalogue.unit_qty, catalogue.unit, purchase.units_bought, catalogue.website 
                    FROM catalogue JOIN product ON product.cas_number=catalogue.cas_number 
                    JOIN supplier ON supplier.supplier_id=catalogue.supplier_id
                    JOIN purchase ON purchase.catalogue_id=catalogue.catalogue_id
                    WHERE {cond} LIKE ?;"""
                c.execute(sql_command, (query_value,))
                # print(cond, query_value)
                # print(cond, ":", data.fetchall())
                records += c.fetchall()
    else:
        sql_cond = sql_columns[search_cond]
        sql_command = f"""SELECT purchase.purchase_id, purchase.date_of_order, purchase.requester, purchase.wbs, product.name, product.cas_number, 
                    supplier.name, catalogue.catalogue_id, catalogue.catalogue_num, catalogue.currency, catalogue.unit_price, catalogue.unit_qty, catalogue.unit, purchase.units_bought, catalogue.website 
                    FROM catalogue JOIN product ON product.cas_number=catalogue.cas_number 
                    JOIN supplier ON supplier.supplier_id=catalogue.supplier_id
                    JOIN purchase ON purchase.catalogue_id=catalogue.catalogue_id
                    WHERE {sql_cond} LIKE ?;"""
        c.execute(sql_command, (query_value,))
        # print(data.fetchall())
        records += c.fetchall()
        # print(search_cond, ":", c.fetchall())

    # print("RECORDS HERE:", records)

    # Create tags
    my_tree.tag_configure('oddrow', background='light blue')
    my_tree.tag_configure('evenrow', background='white')

    count = 0 
    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text="Parent", values=(record[0], record[1], record[2], record[3], record[4],record[5],
                        record[6],record[7],record[8],record[9],record[10],record[11],record[12], record[13], record[14]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text="Parent", values=(record[0], record[1], record[2], record[3], record[4],record[5],
                        record[6],record[7],record[8],record[9],record[10],record[11],record[12], record[13], record[14]), tags=('oddrow',))
        count += 1

    conn.commit()
    conn.close()

def receive():
    main_frame.pack_forget()
    search_frame.pack_forget()
    receive_frame.pack()
    lmms_number.focus_force()

def search():
    receive_frame.pack_forget()
    main_frame.pack_forget()
    search_frame.pack()

# clear all entry boxes
def empty_all(entries):
    # print(entries)
    for entry in entries:
        if isinstance(entry, ttk.Combobox):
            entry.set("")
        elif isinstance(entry, Entry):
            entry.delete(0, END)
        elif isinstance(entry, tuple):
            if isinstance(entry[0], StringVar):
                entry[0].set(entry[1])

# Function to insert values from Treeview into target entry boxes 
def insert_all(entries, record = None):

    # Clears the entry box for date purchased
    entries[0].delete(0, END)

    values = None
    if record:
        values = list(record)
    else:
        # Grab record number
        selected = my_tree.focus()
        # Grab record values
        values = list(my_tree.item(selected, "values"))
        del values[0]
        del values[6]

    print("Insert all:", values)

    # Removes None values
    for i, val in enumerate(values):
        if val == "None" or val == None:
            values[i] = ""

    count = 0
    for entry in entries:
        # if record and entry == catalogue_num:
        #     count += 1
        if isinstance(entry, ttk.Combobox):
            # print(values[count], entry)
            entry.set(values[count])
        elif isinstance(entry, Entry):
            # print(values[count], entry)
            entry.insert(0, values[count])
        elif isinstance(entry, StringVar):
            # print(values[count], entry)
            entry.set(values[count])

        count += 1

# Top Frame
icon_frame = Frame(second_frame)

# Add the icon frame To a Window In The Canvas
icon_frame.pack()
# height = root.winfo_height()
# width = root.winfo_width()
# print(height, width)

# master_canvas.create_window((width/2,height/2), window=icon_frame, anchor="center")

main_frame_button = Button(icon_frame, text="Main", command=main)
receive_frame_button = Button(icon_frame, text="Receive", command=receive)
search_frame_button = Button(icon_frame, text="Search", command=search)

main_frame_button.grid(row=0, column=0, padx=10, pady=10, sticky=W)
receive_frame_button.grid(row=0, column=1, padx=10, pady=10, sticky=W)
search_frame_button.grid(row=0, column=2, padx=10, pady=10, sticky=W)

#---------------------------------------------------------#
# Creating frames


# Main console Frame
main_frame = Frame(second_frame)
main_frame.pack()

# Quotation Frame as part of Main frame
quote_frame = Frame(main_frame)
quote_frame.pack(anchor='w', padx=20, pady=10)

# -- Creating content for quote frame
quote_no = Entry(quote_frame, width=20)
quote_no_label = Label(quote_frame, text="Quotation Number")
quote_no.grid(row=0, column=1, sticky='w')
quote_no_label.grid(row=0, column=0, sticky='w')

# Product frame as part of Main frame
product_frame = LabelFrame(main_frame, text="Product Details", padx=15, pady=20)
product_frame.pack()

# Purchase Frame as part of Main frame
purchase_frame = LabelFrame(main_frame, text="Purchase", padx=15, pady=20)
purchase_frame.pack()

# Receive console Frame
receive_frame = Frame(second_frame)

# Auto-populate frame as part of Receive Frame
auto_frame = Frame(receive_frame)
auto_frame.pack(anchor='center', padx=20, pady=10)

# New Entry frame as part of Receive Frame
new_entry_frame = LabelFrame(receive_frame, text="New Entry", padx=20, pady=20)
new_entry_frame.pack(padx=20)

# Search console Frame
search_frame = Frame(second_frame)

# Search queries frame
query_frame = Frame(search_frame)
query_frame.pack(pady=20)

# Search Tree Frame
search_tree_frame = Frame(search_frame)
search_tree_frame.pack(anchor='center')

# Update Frame as part of search_frame
update_frame = LabelFrame(search_frame, padx=10, pady=10)
update_frame.pack(padx=10, pady=10, anchor='center', fill=BOTH, expand=1)


## Creating content for main frame

# Creating labels
catalogue_num_label = Label(product_frame, text="Catalogue Number")
product_name_label = Label(product_frame, text="Product Name")
cas_number_label = Label(product_frame, text="CAS Number")

catalogue_num_var = StringVar()
product_name_var = StringVar()
cas_number_var = StringVar()

catalogue_num = ttk.Combobox(product_frame, width=20, textvariable=catalogue_num_var)
product_name = ttk.Combobox(product_frame, width=20, textvariable=product_name_var)
cas_number = ttk.Combobox(product_frame, width=20, textvariable=cas_number_var)


def auto_main_popup(records):
    def select_autofill(records=None):
        empty_all(main_frame_insert_list)

        if not records:
            # Grab record number
            selected = my_tree.focus()
            # Grab record values
            records = my_tree.item(selected, "values")
            # print("Select_autofill:", records)

        insert_all(main_frame_insert_list, records)
        select_level.destroy()

    if len(records) > 1:
        select_level = Toplevel()
        select_level.geometry("1000x400")
        # Creating Treeview for select_level
        my_tree = ttk.Treeview(select_level, columns=("Date", 
                                "Requester", 
                                "WBS", 
                                "Product name", 
                                "CAS number",
                                "Supplier",
                                # no need to add catalogue_id as we are not updating the database
                                "Catalogue number",
                                "Currency",
                                "Unit Price",
                                "Unit Quantity",
                                "Unit",
                                "Units Bought",
                                "Website"))

        select_autofill_btn = Button(select_level, text="Select", command=select_autofill)

        # Packing my_tree to select_level
        my_tree.pack(expand=TRUE, fill=X)
        select_autofill_btn.pack(padx=10, pady=10, anchor=NE)

        # Formatting our columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Date", width=80)
        my_tree.column("Requester", width=80)
        my_tree.column("WBS", width=80)
        my_tree.column("Product name", width=80, stretch=YES)
        my_tree.column("CAS number", width=80)
        my_tree.column("Supplier", width=80)
        my_tree.column("Catalogue number", width=80)
        my_tree.column("Currency", width=60)
        my_tree.column("Unit Price", width=80)
        my_tree.column("Unit Quantity", width=80)
        my_tree.column("Unit", width=50)
        my_tree.column("Units Bought", width=50)
        my_tree.column("Website", width=80)

        # Create Headings
        my_tree.heading("#0", text="Label", anchor=W)
        my_tree.heading("Date", text="Date", anchor=W)
        my_tree.heading("Requester", text="Requester", anchor=W)
        my_tree.heading("WBS", text="WBS", anchor=W)
        my_tree.heading("Product name", text="Product name", anchor=W)
        my_tree.heading("CAS number", text="CAS number", anchor=W)
        my_tree.heading("Supplier", text="Supplier", anchor=W)
        my_tree.heading("Catalogue number", text="Catalogue number", anchor=W)
        my_tree.heading("Currency", text="Currency", anchor=W)
        my_tree.heading("Unit Price", text="Unit Price", anchor=CENTER)
        my_tree.heading("Unit Quantity", text="Unit Quantity", anchor=W)
        my_tree.heading("Unit", text="Unit", anchor=W)
        my_tree.heading("Units Bought", text="Unit Bought", anchor=CENTER)
        my_tree.heading("Website", text="Website", anchor=W)

        count = 0
        for record in records:
            my_tree.insert(parent='', index='end', iid=count, text="Parent", values=(record[0], record[1], record[2], 
                        record[3], record[4],record[5],record[6],record[7],record[8],record[9],record[10],record[11], record[12]))
            count += 1
    elif len(records) == 0:
        confirmation_label.config(text="No records found!")
    else:
        # print("Length 1: ", records)
        select_autofill(records[0])
        # catalogue_num.set(records[0][6])

def auto_main():
    global records
    
    conn = sqlite3.connect("purchase_db.db")
    c = conn.cursor()

    cat_num_submit = catalogue_num_var.get().strip()
    cas_num_submit = cas_number_var.get().strip()
    prod_name_submit = product_name_var.get().strip()
    # print(cat_num_submit)

    if cat_num_submit:
        c.execute("""SELECT purchase.date_of_order, purchase.requester, purchase.wbs, product.name, product.cas_number, 
            supplier.name, catalogue.catalogue_num, catalogue.currency, catalogue.unit_price, catalogue.unit_qty, catalogue.unit, purchase.units_bought, catalogue.website 
            FROM catalogue
            JOIN product ON product.cas_number=catalogue.cas_number 
            JOIN supplier ON supplier.supplier_id=catalogue.supplier_id
            LEFT JOIN purchase ON purchase.catalogue_id=catalogue.catalogue_id
            WHERE catalogue.catalogue_num = ? """, (cat_num_submit,))
        records = c.fetchall()
        # print("Cat_num:", records)
        # insert_all(main_frame_insert_list, record = record)
        auto_main_popup(records)

    elif cas_num_submit:
        c.execute("""SELECT purchase.date_of_order, purchase.requester, purchase.wbs, product.name, product.cas_number, 
            supplier.name, catalogue.catalogue_num, catalogue.currency, catalogue.unit_price, catalogue.unit_qty, catalogue.unit, purchase.units_bought, catalogue.website 
            FROM catalogue
            JOIN product ON product.cas_number=catalogue.cas_number 
            JOIN supplier ON supplier.supplier_id=catalogue.supplier_id
            LEFT JOIN purchase ON purchase.catalogue_id=catalogue.catalogue_id
            WHERE product.cas_number = ? """, (cas_num_submit,))

        records = c.fetchall()
        # print("CAS_num_submit:",records)
        auto_main_popup(records)

    else:
        confirmation_label.config(text="No Value Provided.")



autofill_main = Button(product_frame, text="Autofill", command=auto_main)

# Packing the content for main frame
catalogue_num_label.grid(row=0, column=0, pady=5)
catalogue_num.grid(row=0, column=1, pady=5, sticky=W)
cas_number_label.grid(row=0, column=2, pady=5, padx=(30,0))
cas_number.grid(row=0, column=3, pady=5, sticky=W)
product_name_label.grid(row=1, column=0, pady=5, padx=(30,0))
product_name.grid(row=1, column=1, pady=5, sticky=W)
autofill_main.grid(row=1, column=3, pady=5, sticky=E)

#---------------------------------------------------------#
## Creating content for purchase frame (in main frame)
supplier_var = StringVar()
wbs_var = StringVar()
requester_var = StringVar()

supplier_label = Label(product_frame, text="Supplier Name")
website_label = Label(product_frame, text="Website")
date_purchased_label = Label(product_frame, text="Date of Purchase")
wbs_label = Label(product_frame, text="WBS")
requester_label = Label(product_frame, text="Requester")

date_purchased = Entry(product_frame, width=20)

units_bought_label = Label(product_frame, text="Units Bought")
unit_price_label = Label(product_frame, text="Unit Price")
unit_qty_label = Label(product_frame, text="Unit Qty")
units_bought_label = Label(product_frame, text="Units Bought")

confirmation_label = Label(product_frame, text="")

currency_options = ["SGD", "USD"]
currency_var = StringVar()
currency_options_default = currency_options[0]
currency_var.set(currency_options_default)

unit_options = ["g", "kg", "ml", "L", ]
unit_var = StringVar()
unit_options_default = unit_options[0]
unit_var.set(unit_options_default)

supplier = ttk.Combobox(product_frame, width=20, textvariable=supplier_var)
website = Entry(product_frame, width=20)
wbs = ttk.Combobox(product_frame, width=20, textvariable=wbs_var)
requester = ttk.Combobox(product_frame, width=20, textvariable=requester_var)
currency = OptionMenu(product_frame, currency_var, *currency_options)
unit = OptionMenu(product_frame, unit_var, *unit_options)
unit_price = Entry(product_frame, width=20)
unit_qty = Entry(product_frame, width=20)
units_bought = Entry(product_frame, width=20)

# Creation of new Calendar window 
def calendar(entry):

    date_level = Toplevel()
    cal = Calendar(date_level, selectmode='day', date_pattern="dd/mm/y")
    cal.pack(pady=20)

    def get_date():
        entry.delete(0, END)
        entry.insert(0, cal.get_date())
        date_level.destroy()

    close_btn = Button(date_level, text="Confirm", command=get_date).pack(pady=20)

date_btn = Button(product_frame, text="Choose date", command=lambda: calendar(date_purchased))

# autofill date entry box with today's date
today = date.today()
date_purchased.insert(0, today.strftime("%d/%m/%Y"))

# creating a submit button, submits record to database
def submit():
    # resets confirmation_label
    confirmation_label.config(text="")

    conn = sqlite3.connect("purchase_db.db")
    c = conn.cursor()

    prod_name_submit = product_name_var.get().strip()
    cas_num_submit = cas_number_var.get().strip()
    supp_submit = supplier_var.get()
    cat_num_submit = catalogue_num_var.get().strip()
    req_submit = requester_var.get().strip()
    wbs_submit = wbs_var.get().strip()

    # Checks if cas_number is already in database, and if it is, then don't insert again
    c.execute("INSERT OR IGNORE INTO product (cas_number, name) VALUES (?,?)", (cas_num_submit, prod_name_submit))
    
    c.execute("INSERT OR IGNORE INTO supplier (name) VALUES (?)", (supp_submit,))

    # ----------------- View new inserted data -----------------
    # print(prod_name_submit)
    # print(cas_num_submit)
    # print(supp_submit)
    # print(cat_num_submit)
    # print(req_submit)
    # print(wbs_submit)

    c.execute("SELECT supplier_id FROM supplier WHERE name = ? ", (supp_submit,))
    supp_rowid = c.fetchone()[0]

    c.execute("""INSERT INTO catalogue (catalogue_num, currency, unit_price, unit_qty, unit, website, supplier_id, cas_number)
    VALUES (?,?,?,?,?,?,?,?)""", (
        cat_num_submit,
        currency_var.get(),
        unit_price.get(),
        unit_qty.get(),
        unit_var.get(),
        website.get(),
        supp_rowid,
        cas_num_submit
    ))
    
    c.execute("SELECT last_insert_rowid()")
    cat_rowid = c.fetchone()[0]

    c.execute("""INSERT INTO purchase (date_of_order, requester, wbs, units_bought, catalogue_id)
                VALUES (?,?,?,?,?)""", (
                    date_purchased.get(),
                    req_submit,
                    wbs_submit,
                    units_bought.get(),
                    cat_rowid
                ))

    confirmation_label.config(text="Record Submitted!")

    # refreshes the available drop down menu options
    c.execute("""SELECT DISTINCT cas_number FROM product""")
    cas_number['values'] = join_tuples(c.fetchall())

    c.execute("""SELECT DISTINCT name FROM product""")
    product_name['values'] = join_tuples(c.fetchall())

    c.execute("""SELECT DISTINCT catalogue_num FROM catalogue""")
    catalogue_num['values'] = join_tuples(c.fetchall())

    c.execute("""SELECT DISTINCT name FROM supplier""")
    supplier['values'] = join_tuples(c.fetchall())

    c.execute("""SELECT DISTINCT wbs FROM purchase""")
    wbs['values'] = join_tuples(c.fetchall())

    c.execute("""SELECT DISTINCT requester FROM purchase""")
    requester['values'] = join_tuples(c.fetchall())

    conn.commit()
    conn.close()
    empty_all(main_frame_entries_list)

    # cas_number.set('')
    # product_name.set('')
    # catalogue_num.set('')
    # unit_price.delete(0, END)
    # unit_qty.delete(0, END)
    # supplier.set('')
    # website.delete(0, END)
    # date_purchased.delete(0, END)
    # requester.delete(0, END)
    # wbs.delete(0, END)
    # units_bought.delete(0, END)


# ----------------- Testing code -----------------
# c.execute("SELECT supplier_id FROM supplier WHERE name = ? ", ("BLD Pharmmmm",))
# supp_rowid = c.fetchone()[0]
# print(supp_rowid)

# c.execute("SELECT EXISTS(SELECT * FROM product WHERE cas_number = ?)", ("9001-05",))
# product_id = c.fetchone()
# print(product_id)

# c.execute("SELECT * FROM supplier")
# supplier_id = c.fetchall()
# print(supplier_id)

# c.execute("SELECT * FROM catalogue")
# supplier_id = c.fetchall()
# print(supplier_id)

# c.execute("SELECT * FROM purchased")
# supplier_id = c.fetchall()
# print(supplier_id)

# ----------------- Testing code END -----------------
clear_main_btn = Button(product_frame, text="Clear All", command=lambda: empty_all(main_frame_entries_list))
submit_btn = Button(product_frame, text="Submit", command=submit)

supplier.grid(row=2, column=1, pady=(20,5))
supplier_label.grid(row=2, column=0, pady=(20,5))
website.grid(row=2, column=3, pady=(20,5))
website_label.grid(row=2, column=2, padx=(30,0), pady=(20,5))
date_purchased.grid(row=3, column=1, pady=5)
date_purchased_label.grid(row=3, column=0, pady=5)
date_btn.grid(row=3, column=2, padx=5, pady=5, sticky=W)
wbs.grid(row=4, column=1, pady=5)
wbs_label.grid(row=4, column=0, pady=5)
requester.grid(row=5, column=1, pady=5)
requester_label.grid(row=5, column=0, pady=5)
unit_price.grid(row=6, column=1, pady=(10,5))
unit_price_label.grid(row=6, column=0, pady=(10,5))
currency.grid(row=6, column=2, pady=(10,5), sticky=W)
unit_qty.grid(row=7, column=1, pady=5)
unit_qty_label.grid(row=7, column=0, pady=5)
unit.grid(row=7, column=2, sticky=W, padx=5, pady=5)
units_bought.grid(row=8, column=1, pady=5)
units_bought_label.grid(row=8, column=0, pady=5)

confirmation_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky=W)
clear_main_btn.grid(row=9, column=2, padx=5, pady=5, sticky=E)
submit_btn.grid(row=9, column=3, padx=5, pady=5, sticky=E)

# Giving the Comboboxes values previously used
def join_tuples(lst):
    res = ()
    for x in lst:
        res += x
    return res

c.execute("""SELECT DISTINCT cas_number FROM product""")
cas_number['values'] = join_tuples(c.fetchall())

c.execute("""SELECT DISTINCT name FROM product""")
product_name['values'] = join_tuples(c.fetchall())

c.execute("""SELECT DISTINCT catalogue_num FROM catalogue""")
catalogue_num['values'] = join_tuples(c.fetchall())

c.execute("""SELECT DISTINCT name FROM supplier""")
supplier['values'] = join_tuples(c.fetchall())

c.execute("""SELECT DISTINCT wbs FROM purchase""")
wbs['values'] = join_tuples(c.fetchall())

c.execute("""SELECT DISTINCT requester FROM purchase""")
requester['values'] = join_tuples(c.fetchall())

#---------------------------------------------------------#
## Creating content for auto frame (in receive frame)
def upload():
    filename = filedialog.askopenfilename(title="Select A File")
    print('Selected:', filename)

def auto_search():
    conn = sqlite3.connect("purchase_db.db")
    c = conn.cursor()

    number = quote_no.get()
    c.execute("SELECT * FROM purchase WHERE quote_no=?", (number,))
    data = c.fetchall()
    count = 0
    for record in data:
        my_tree.insert(parent='', index='end', iid=count, text="Parent", values=(record[0], record[1], record[2], 
                        record[3], record[4],record[5],record[6],record[7],record[8],record[9],record[10],record[11], record[12]))
        count += 1

quote_no = Entry(auto_frame, width=20)
quote_no_label = Label(auto_frame, text="Quotation Number:")

file_upload_label = Label(auto_frame, text="File Upload:")
file_upload_btn = Button(auto_frame, text="Choose File", command=upload)

auto_search_btn = Button(auto_frame, text="Search", command=auto_search)

quote_no.grid(row=0, column=1, sticky='w')
quote_no_label.grid(row=0, column=0, sticky='w', padx=(0,5))
file_upload_btn.grid(row=0, column=3)
file_upload_label.grid(row=0, column=2, padx=(20,5))
auto_search_btn.grid(row=1, column=1, sticky='w', pady=10)

#---------------------------------------------------------#
## Creating content for new_entry_frame (in receive frame)

# Creating labels
new_catalogue_num_label = Label(new_entry_frame, text="Catalogue Number")
new_product_name_label = Label(new_entry_frame, text="Product Name")
new_cas_number_label = Label(new_entry_frame, text="CAS Number")

new_catalogue_num_var = StringVar()
new_product_name_var = StringVar()
new_cas_number_var = StringVar()

new_catalogue_num = ttk.Combobox(new_entry_frame, width=20, textvariable=new_catalogue_num_var)
new_product_name = ttk.Combobox(new_entry_frame, width=20, textvariable=new_product_name_var)
new_cas_number = ttk.Combobox(new_entry_frame, width=20, textvariable=new_cas_number_var)

var = StringVar()
check = Checkbutton(new_entry_frame, text="Chemical", variable=var, onvalue="On", offvalue="Off")
check.deselect()

lmms_number = Entry(new_entry_frame, width=20)
batch_number = Entry(new_entry_frame, width=20)
exp_date = Entry(new_entry_frame, width=20)

# Makes the user focus on the lmms_number entry
lmms_number.focus_force()

exp_date_btn = Button(new_entry_frame, text="Choose date", command=lambda: calendar(exp_date))

total_weight = Entry(new_entry_frame, width=20)
delivery_date = Entry(new_entry_frame, width=20)

lmms_number_label = Label(new_entry_frame, text="LMMS Number")
batch_number_label = Label(new_entry_frame, text="Batch Number")
exp_date_label = Label(new_entry_frame, text="Expiry Date")
total_weight_label = Label(new_entry_frame, text="Total Weight")
delivery_date_label = Label(new_entry_frame, text="Delivery Date")

new_catalogue_num_label.grid(row=0, column=0)
new_catalogue_num.grid(row=0, column=1)
new_product_name_label.grid(row=0, column=2, padx=(30,0), pady=(5,0))
new_product_name.grid(row=0, column=3)
new_cas_number_label.grid(row=1, column=2, padx=(30,0), pady=(5,0))
new_cas_number.grid(row=1, column=3, pady=5)

check.grid(row=2, column=0, pady=(20,10))

lmms_number.grid(row=3, column=1, pady=(5,0))
batch_number.grid(row=4, column=1, pady=(5,0))
exp_date.grid(row=5, column=1, pady=(5,0))

exp_date_btn.grid(row=5, column=2, pady=(5,0))

total_weight.grid(row=6, column=1, pady=(5,0))
delivery_date.grid(row=7, column=1, pady=(5,0))

lmms_number_label.grid(row=3, column=0, pady=(5,0))
batch_number_label.grid(row=4, column=0, pady=(5,0))
exp_date_label.grid(row=5, column=0, pady=(5,0))
total_weight_label.grid(row=6, column=0, pady=(5,0))
delivery_date_label.grid(row=7, column=0, pady=(5,0))

# Purchase Treeview Scrollbar
# tree_scroll_new = Scrollbar(search_tree_frame)
# tree_scroll_new.pack(side=RIGHT, fill=Y)

purchase_tree = ttk.Treeview(receive_frame, 
                        columns=("Purchase ID",
                        "Date", 
                        "Requester", 
                        "WBS", 
                        "Product name", 
                        "CAS number",
                        "Supplier",
                        "Catalogue ID",
                        "Catalogue number",
                        "Currency",
                        "Unit Price",
                        "Unit Quantity",
                        "Unit",
                        "Units Bought",
                        "Website"))

# Configure the scrollbar
# tree_scroll_new.config(command=purchase_tree.yview)

# Packing my_tree to search_tree_frame
purchase_tree.pack()

# Formatting our columns
purchase_tree.column("#0", width=0, stretch=NO)
purchase_tree.column("Purchase ID", width=0, stretch=NO)
purchase_tree.column("Date", width=80)
purchase_tree.column("Requester", width=80)
purchase_tree.column("WBS", width=80)
purchase_tree.column("Product name", width=80, stretch=YES)
purchase_tree.column("CAS number", width=80)
purchase_tree.column("Supplier", width=80)
purchase_tree.column("Catalogue ID", width=0, stretch=NO)
purchase_tree.column("Catalogue number", width=80)
purchase_tree.column("Currency", width=60)
purchase_tree.column("Unit Price", width=80)
purchase_tree.column("Unit Quantity", width=80)
purchase_tree.column("Unit", width=50)
purchase_tree.column("Units Bought", width=50)
purchase_tree.column("Website", width=80)

# Create Headings
purchase_tree.heading("#0", text="Label", anchor=W)
purchase_tree.heading("Purchase ID", text="Purchase ID", anchor=W)
purchase_tree.heading("Date", text="Date", anchor=W)
purchase_tree.heading("Requester", text="Requester", anchor=W)
purchase_tree.heading("WBS", text="WBS", anchor=W)
purchase_tree.heading("Product name", text="Product name", anchor=W)
purchase_tree.heading("CAS number", text="CAS number", anchor=W)
purchase_tree.heading("Supplier", text="Supplier", anchor=W)
purchase_tree.heading("Catalogue ID", text="Catalogue ID", anchor=CENTER)
purchase_tree.heading("Catalogue number", text="Catalogue number", anchor=W)
purchase_tree.heading("Currency", text="Currency", anchor=W)
purchase_tree.heading("Unit Price", text="Unit Price", anchor=CENTER)
purchase_tree.heading("Unit Quantity", text="Unit Quantity", anchor=W)
purchase_tree.heading("Unit", text="Unit", anchor=W)
purchase_tree.heading("Units Bought", text="Unit Bought", anchor=CENTER)
purchase_tree.heading("Website", text="Website", anchor=W)


#---------------------------------------------------------#
## Creating content for Tree frame

# Treeview Scrollbar
tree_scroll = Scrollbar(search_tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Creating Treeview
my_tree = ttk.Treeview(search_tree_frame, height=8, yscrollcommand=tree_scroll.set, 
                        columns=("Purchase ID",
                        "Date", 
                        "Requester", 
                        "WBS", 
                        "Product name", 
                        "CAS number",
                        "Supplier",
                        "Catalogue ID",
                        "Catalogue number",
                        "Currency",
                        "Unit Price",
                        "Unit Quantity",
                        "Unit",
                        "Units Bought",
                        "Website"))

# Configure the scrollbar
tree_scroll.config(command=my_tree.yview)

# Packing my_tree to search_tree_frame
my_tree.pack(expand=TRUE, fill=X)

# Formatting our columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Purchase ID", width=50)
my_tree.column("Date", width=80)
my_tree.column("Requester", width=80)
my_tree.column("WBS", width=80)
my_tree.column("Product name", width=80, stretch=YES)
my_tree.column("CAS number", width=80)
my_tree.column("Supplier", width=80)
my_tree.column("Catalogue ID", width=0, stretch=NO)
my_tree.column("Catalogue number", width=80)
my_tree.column("Currency", width=60)
my_tree.column("Unit Price", width=80)
my_tree.column("Unit Quantity", width=80)
my_tree.column("Unit", width=50)
my_tree.column("Units Bought", width=50)
my_tree.column("Website", width=80)

# Create Headings
my_tree.heading("#0", text="Label", anchor=W)
my_tree.heading("Purchase ID", text="Purchase ID", anchor=W)
my_tree.heading("Date", text="Date", anchor=W)
my_tree.heading("Requester", text="Requester", anchor=W)
my_tree.heading("WBS", text="WBS", anchor=W)
my_tree.heading("Product name", text="Product name", anchor=W)
my_tree.heading("CAS number", text="CAS number", anchor=W)
my_tree.heading("Supplier", text="Supplier", anchor=W)
my_tree.heading("Catalogue ID", text="Catalogue ID", anchor=CENTER)
my_tree.heading("Catalogue number", text="Catalogue number", anchor=W)
my_tree.heading("Currency", text="Currency", anchor=W)
my_tree.heading("Unit Price", text="Unit Price", anchor=CENTER)
my_tree.heading("Unit Quantity", text="Unit Quantity", anchor=W)
my_tree.heading("Unit", text="Unit", anchor=W)
my_tree.heading("Units Bought", text="Unit Bought", anchor=CENTER)
my_tree.heading("Website", text="Website", anchor=W)

# Add some style
style = ttk.Style()
# Pick a theme
# style.theme_use("default")

# Configure our Treeview colours

style.configure("Treeview", 
    background = "white",
    foreground = "black",
    rowheight = 25,
    fieldbackground = "white"
)

# Change selected color
style.map('Treeview', background=[('selected', 'blue')])

def select_update(e):
    empty_all(update_frame_entries_list)

    global selected_cat_id
    global selected_purchase_id
    # Grab record number
    selected = my_tree.focus()
    # Grab record values
    records = my_tree.item(selected, "values")

    selected_cat_id = records[7]
    selected_purchase_id = records[0]
    print(selected_cat_id)
    print(selected_purchase_id)

    # print("Select update:", values)

    insert_all(update_frame_entries_list)
    
my_tree.bind("<Double-1>", select_update)

# Function to update existing records from update_frame
def update_records():
    conn = sqlite3.connect("purchase_db.db")
    c = conn.cursor()

    print(selected_cat_id)

    prod_name_update = product_name_var_update.get().strip()
    cas_num_update = cas_number_var_update.get().strip()
    supp_update = supplier_var_update.get()
    cat_num_update = catalogue_num_var_update.get().strip()
    req_update = requester_var_update.get().strip()
    wbs_update = wbs_var_update.get().strip()

    def alert_update(msg):
        alert_frame = Toplevel(root)
        alert_label_update = Label(alert_frame, text=msg)
        alert_label_update.grid(row=0, column=0, columnspan=2)

        alert_yes_btn = Button(alert_frame, text="Yes", command=alert_frame.destroy)
        alert_no_btn = Button(alert_frame, text="No", command=alert_frame.destroy)
        alert_yes_btn.grid(row=1, column=0, padx=20, pady=20)
        alert_no_btn.grid(row=1, column=1, padx=20, pady=20)

        alert_frame.grab_set()
        root.wait_window(alert_frame)

    # if product cas_number is already in the database, popup alert
    c.execute("SELECT EXISTS(SELECT * FROM product WHERE cas_number = ?)", (cas_num_update,))
    result = c.fetchone()[0]
    # print("CAS_num:", result)
    if result:
        alert_update("""Product CAS Number / Name already exists in database.\n \
                        Changes will only be done for this record.\n \
                        Proceed?""")
    else:
        # else, insert statement for product cas_number and name
        c.execute("INSERT INTO product (cas_number, name) VALUES (?,?)", (cas_num_update, prod_name_update))

    # if supplier name is already in the database, popup alert
    c.execute("SELECT EXISTS(SELECT * FROM supplier WHERE name = ?)", (supp_update,))
    result2 = c.fetchone()[0]
    if result2:
        alert_update("""Supplier name already exists in database.\n \
                        Changes will only be done for this record.\n \
                        Proceed?""")
    else:
        # else, insert statement for supplier name 
        c.execute("INSERT INTO supplier (name) VALUES (?)", (supp_update,))

    # extract product cas_number - no need as can just use cas_num_update

    # extract supplier_id
    c.execute("SELECT supplier_id FROM supplier WHERE name = ? ", (supp_update,))
    supp_rowid = c.fetchone()[0]

    # using catalogue_id, update the data, including product and supplier id
    c.execute("""UPDATE catalogue SET catalogue_num = ?, currency = ?, unit_price = ?, unit_qty = ?, unit = ?, website = ?, supplier_id = ?, cas_number = ?
                WHERE catalogue_id = ?""",
                (cat_num_update,
                currency_var_update.get(),
                unit_price_update.get(),
                unit_qty_update.get(),
                unit_var_update.get(),
                website_update.get(),
                supp_rowid,
                cas_num_update,
                selected_cat_id
                ))

    c.execute("""UPDATE purchase SET date_of_order = ?, requester = ?, wbs = ?, units_bought = ?, catalogue_id = ?
                WHERE purchase_id = ?""", 
                (date_purchased_update.get(),
                req_update,
                wbs_update,
                units_bought_update.get(),
                selected_cat_id,
                selected_purchase_id
                ))

    print(selected_purchase_id)

    confirmation_label_update.config(text="Submitted Revision!")

    conn.commit()
    conn.close()

    reset_tree()
    empty_all(update_frame_entries_list)


#---------------------------------------------------------#
## Creating content for query frame

# Creating query entry boxes and labels
query_var_update = StringVar()
query_options = [
    "Search All",
    "Date",
    "Requester",
    "WBS",
    "Product Name",
    "CAS Number",
    "Supplier",
    "Catalogue Number",
    "Currency",
    "Unit Price",
    "Unit Quantity",
    "Unit",
    "Units Bought",
    "Website"
]
query_options_default = query_options[0]
query_var_update.set(query_options_default)
max_width = len(max(query_options, key=len))

query_label = Label(query_frame, text="Search:")
query = Entry(query_frame, width=20)
query_conditions = OptionMenu(query_frame, query_var_update, *query_options)
query_conditions.config(width=max_width)
query_btn = Button(query_frame, text="Go", command=reset_tree)

query_label.grid(row=0, column=0, padx=5)
query.grid(row=0, column=1)
query_conditions.grid(row=0, column=2, padx=10)
query_btn.grid(row=0, column=3, padx=10)

#---------------------------------------------------------#
## Creating content for update frame
# Displaying and updating of data using search function
nl = Label(update_frame, text="Name")
nl.grid(row=0, column=0)

catalogue_num_label = Label(update_frame, text="Catalogue Number")
product_name_label = Label(update_frame, text="Product Name")
cas_number_label = Label(update_frame, text="CAS Number")

catalogue_num_var_update = StringVar()
product_name_var_update = StringVar()
cas_number_var_update = StringVar()

catalogue_num_update = ttk.Combobox(update_frame, width=20, textvariable=catalogue_num_var_update)
product_name_update = ttk.Combobox(update_frame, width=20, textvariable=product_name_var_update)
cas_number_update = ttk.Combobox(update_frame, width=20, textvariable=cas_number_var_update)

supplier_var_update = StringVar()
wbs_var_update = StringVar()
requester_var_update = StringVar()

supplier_label = Label(update_frame, text="Supplier Name")
website_label = Label(update_frame, text="Website")
date_purchased_label = Label(update_frame, text="Date of Purchase")
wbs_label = Label(update_frame, text="WBS")
requester_label = Label(update_frame, text="Requester")

date_purchased_update = Entry(update_frame, width=20)

units_bought_label = Label(update_frame, text="Units Bought")
unit_price_label = Label(update_frame, text="Unit Price")
unit_qty_label = Label(update_frame, text="Unit Qty")
units_bought_label = Label(update_frame, text="Units Bought")

confirmation_label_update = Label(update_frame, text="")

# currency_options = ["SGD", "USD"]
currency_var_update = StringVar()
currency_var_update.set(currency_options_default)

# unit_options = ["g", "kg", "ml", "L", ]
unit_var_update = StringVar()
unit_var_update.set(unit_options_default)

supplier_update = ttk.Combobox(update_frame, width=20, textvariable=supplier_var_update)
website_update = Entry(update_frame, width=20)
wbs_update = ttk.Combobox(update_frame, width=20, textvariable=wbs_var_update)
requester_update = ttk.Combobox(update_frame, width=20, textvariable=requester_var_update)
currency_update = OptionMenu(update_frame, currency_var_update, *currency_options)
unit_update = OptionMenu(update_frame, unit_var_update, *unit_options)
unit_price_update = Entry(update_frame, width=20)
unit_qty_update = Entry(update_frame, width=20)
units_bought_update = Entry(update_frame, width=20)

date_btn_update = Button(update_frame, text="Choose date", command=lambda: calendar(date_purchased_update))

catalogue_num_label.grid(row=0, column=0, pady=5)
catalogue_num_update.grid(row=0, column=1, pady=5, sticky=W)
cas_number_label.grid(row=0, column=2, pady=5, padx=(30,0))
cas_number_update.grid(row=0, column=3, pady=5, sticky=W)
product_name_label.grid(row=1, column=0, pady=5, padx=(30,0))
product_name_update.grid(row=1, column=1, pady=5, sticky=W)

supplier_update.grid(row=2, column=1, pady=(20,5))
supplier_label.grid(row=2, column=0, pady=(20,5))
website_update.grid(row=2, column=3, pady=(20,5))
website_label.grid(row=2, column=2, padx=(30,0), pady=(20,5))
date_purchased_update.grid(row=3, column=1, pady=5)
date_purchased_label.grid(row=3, column=0, pady=5)
date_btn_update.grid(row=3, column=2, padx=5, pady=5, sticky=W)
wbs_update.grid(row=4, column=1, pady=5)
wbs_label.grid(row=4, column=0, pady=5)
requester_update.grid(row=5, column=1, pady=5)
requester_label.grid(row=5, column=0, pady=5)
unit_price_update.grid(row=6, column=1, pady=(10,5))
unit_price_label.grid(row=6, column=0, pady=(10,5))
currency_update.grid(row=6, column=2, pady=(10,5), sticky=W)
unit_qty_update.grid(row=7, column=1, pady=5)
unit_qty_label.grid(row=7, column=0, pady=5)
unit_update.grid(row=7, column=2, sticky=W, padx=5, pady=5)
units_bought_update.grid(row=8, column=1, pady=5)
units_bought_label.grid(row=8, column=0, pady=5)

confirmation_label_update.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
update_btn = Button(update_frame, text="Submit", command=update_records)
update_btn.grid(row=9, column=3, pady=5, sticky='e')

# refreshes the available drop down menu options
c.execute("""SELECT DISTINCT cas_number FROM product""")
cas_number_update['values'] = join_tuples(c.fetchall())

c.execute("""SELECT DISTINCT name FROM product""")
product_name_update['values'] = join_tuples(c.fetchall())

c.execute("""SELECT DISTINCT catalogue_num FROM catalogue""")
catalogue_num_update['values'] = join_tuples(c.fetchall())

c.execute("""SELECT DISTINCT name FROM supplier""")
supplier_update['values'] = join_tuples(c.fetchall())

c.execute("""SELECT DISTINCT wbs FROM purchase""")
wbs_update['values'] = join_tuples(c.fetchall())

c.execute("""SELECT DISTINCT requester FROM purchase""")
requester_update['values'] = join_tuples(c.fetchall())

# Creating a list of entry boxes in update_frame for empty_all
update_frame_entries_list = [date_purchased_update, requester_update, wbs_update, product_name_update, cas_number_update, supplier_update, catalogue_num_update, currency_var_update, unit_price_update, unit_qty_update, unit_var_update, units_bought_update, website_update]
main_frame_insert_list = [date_purchased, requester, wbs, product_name, cas_number, supplier, catalogue_num, currency_var, unit_price, unit_qty, unit_var, units_bought, website]

# Creating a list of all entry box names for empty_all function
main_frame_entries_list = [cas_number, product_name, catalogue_num, (currency_var, currency_options_default), (unit_var, unit_options_default), unit_price, unit_qty, supplier, website, date_purchased, requester, wbs, units_bought]

c.execute("SELECT * FROM product WHERE ? LIKE ?", ("cas_number", "141-53-7",))
print(c.fetchall())

conn.commit()
conn.close()

root.mainloop()