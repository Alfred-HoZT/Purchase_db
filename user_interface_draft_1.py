from tkinter import *
from tkcalendar import Calendar
from tkinter import ttk
import sqlite3

root = Tk()
root.title("Purchase Database")
root.geometry("1000x400")

conn = sqlite3.connect("purchase_db.db")
c = conn.cursor()

# Creating Frames
tree_frame = Frame(root)
purchase_frame = Frame(root)

# Creating the frame for the input entries
entry_frame = Frame(root, padx=5, pady=5)
entry_frame.pack(padx=10, pady=10, expand=True, fill=X)

purchase_frame.pack(expand=True, fill=X)
tree_frame.pack()

currency_options = ["SGD", "USD"]
currency_var = StringVar()
currency_var.set(currency_options[0])

unit_options = ["g", "kg"]
unit_var = StringVar()
unit_var.set(unit_options[0])

# clear all entry boxes
def empty_all():
    cas_number.set('')
    product_name.set('')
    catalogue_num.set('')
    unit_price.delete(0, END)
    unit_qty.delete(0, END)
    supplier.set('')
    website.delete(0, END)

    if purchased_var.get() == "1":
        date_of_order.delete(0, END)
        requester.delete(0, END)
        wbs.delete(0, END)
        delivery_status.set('')


# Submit new records to database
def submit():
    
    conn = sqlite3.connect("purchase_db.db")
    c = conn.cursor()

    cas_retrieved = cas_number_var.get()

    c.execute("INSERT INTO product (cas_number, name) VALUES (?,?)", (cas_number_var.get(), product_name_var.get()))

    c.execute("INSERT INTO supplier (name) VALUES (?)", (supplier_var.get(),))

    c.execute("SELECT last_insert_rowid()")
    supp_rowid = c.fetchone()[0]

    c.execute("""INSERT INTO catalogue (catalogue_num, currency, unit_price, unit_qty, unit, website, supplier_id, cas_number)
    VALUES (?,?,?,?,?,?,?,?)""", (
        catalogue_num_var.get(),
        currency_var.get(),
        unit_price.get(),
        unit_qty.get(),
        unit_var.get(),
        website.get(),
        supp_rowid,
        cas_number_var.get()
    ))
    
    c.execute("SELECT last_insert_rowid()")
    cat_rowid = c.fetchone()[0]

    if purchased_var.get() == "1":
        c.execute("""INSERT INTO purchased (date_of_order, requester, wbs, delivery_status, catalogue_id)
                    VALUES (?,?,?,?,?)""", (
                        date_of_order.get(),
                        requester.get(),
                        wbs.get(),
                        delivery_status_var.get(),
                        cat_rowid
                    ))

    conn.commit()
    conn.close()
    empty_all()


# Double clicking on record places them in the entry boxes
def select(e):
    # Clear entry boxes
    empty_all()

    # Grab record number
    selected = my_tree.focus()
    # Grab record values
    values = list(my_tree.item(selected, "values"))

    for i, val in enumerate(values):
        if val == "None":
            values[i] = ""

    date_of_order.insert(0, values[0])
    requester.insert(0, values[2])
    wbs.insert(0, values[3])
    delivery_status.set(values[1])

    cas_number.set(values[5])
    product_name.set(values[4])
    catalogue_num.set(values[7])
    unit_price.insert(0, values[9])
    unit_qty.insert(0, values[10])
    supplier.set(values[6])
    website.insert(0, values[12])



# Packs Treeview table to bottom of screen
def show():
    conn = sqlite3.connect("purchase_db.db")
    c = conn.cursor()

    for widgets in tree_frame.winfo_children():
        widgets.destroy()

    global my_tree
    my_tree = ttk.Treeview(tree_frame)

    # Defining our columns
    my_tree['columns'] = ("Date", 
                        "Delivery Status",
                        "Requester", 
                        "WBS", 
                        "Product name", 
                        "CAS number",
                        "Supplier",
                        "Catalogue number",
                        "Currency",
                        "Unit Price",
                        "Unit Quantity",
                        "Unit",
                        "Website"
                        )

    my_tree.column("Date", width=80)
    my_tree.column("Delivery Status", width=80)
    my_tree.column("Requester", width=80)
    my_tree.column("WBS", width=80)
    my_tree.heading("Date", text="Date", anchor=W)
    my_tree.heading("Delivery Status", text="Delivery Status", anchor=W)
    my_tree.heading("Requester", text="Requester", anchor=W)
    my_tree.heading("WBS", text="WBS", anchor=W)
    
    # Formatting our columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Product name", width=80, stretch=YES)
    my_tree.column("CAS number", width=80)
    my_tree.column("Supplier", width=80)
    my_tree.column("Catalogue number", width=80)
    my_tree.column("Currency", width=80)
    my_tree.column("Unit Price", width=80)
    my_tree.column("Unit Quantity", width=80)
    my_tree.column("Unit", width=80)
    my_tree.column("Website", width=80)

    # Create Headings
    my_tree.heading("#0", text="Label", anchor=W)
    my_tree.heading("Product name", text="Product name", anchor=W)
    my_tree.heading("CAS number", text="CAS number", anchor=W)
    my_tree.heading("Supplier", text="Supplier", anchor=W)
    my_tree.heading("Catalogue number", text="Catalogue number", anchor=W)
    my_tree.heading("Currency", text="Currency", anchor=W)
    my_tree.heading("Unit Price", text="Unit Price", anchor=CENTER)
    my_tree.heading("Unit Quantity", text="Unit Quantity", anchor=W)
    my_tree.heading("Unit", text="Unit", anchor=W)
    my_tree.heading("Website", text="Website", anchor=W)

    my_tree.bind("<Double-1>", select)

    data = c.execute("""SELECT date_of_order, delivery_status, requester, wbs, product.name, product.cas_number, 
            supplier.name, catalogue_num, currency, unit_price, unit_qty, unit, website 
            FROM catalogue JOIN product ON product.cas_number=catalogue.cas_number 
            JOIN supplier ON supplier.supplier_id=catalogue.supplier_id
            LEFT JOIN purchased ON purchased.catalogue_id=catalogue.catalogue_id""")
    data = c.fetchall()
    count = 0
    for record in data:
        my_tree.insert(parent='', index='end', iid=count, text="Parent", values=(record[0], record[1], record[2], 
                        record[3], record[4],record[5],record[6],record[7],record[8],record[9],record[10],record[11], record[12]))
        count += 1

    print(data)
    my_tree.pack()

    conn.commit()
    conn.close()

# Creation of new Calendar window 
def calendar(entry):

    date_level = Toplevel()
    cal = Calendar(date_level, selectmode='day')
    cal.pack(pady=20)

    def get_date():
        entry.delete(0, END)
        entry.insert(0, cal.get_date())
        date_level.destroy()

    close_btn = Button(date_level, text="Confirm", command=get_date).pack(pady=20)

def purchased():
    # Creating Purchased entries
    if purchased_var.get() == "1":
        global date_of_order
        global date_of_order_label
        global requester
        global requester_label
        global wbs
        global wbs_label
        global date_btn
        global delivery_status_var
        global delivery_status
        global delivery_status_label
        global delivery_status
        global delivery_status_btn
        global delivery_status_label

        requester_var = StringVar()
        wbs_var = StringVar()
        delivery_status_var = StringVar()

        date_of_order = Entry(purchase_frame, width=40)
        date_of_order_label = Label(purchase_frame, text="Date of Order")
        requester = ttk.Combobox(purchase_frame, width=40, textvariable=requester_var)
        requester_label = Label(purchase_frame, text="Requester")
        wbs = ttk.Combobox(purchase_frame, width=40, textvariable=wbs_var)
        wbs_label = Label(purchase_frame, text="WBS")
        delivery_status = ttk.Combobox(purchase_frame, width=20, textvariable=delivery_status_var, values=("Not delivered",))
        delivery_status_label = Label(purchase_frame, text="Delivery Status")

        c.execute("SELECT DISTINCT requester FROM purchased")
        requester['values'] = join_tuples(c.fetchall())

        c.execute("SELECT DISTINCT wbs FROM purchased")
        wbs['values'] = join_tuples(c.fetchall())

        date_btn = Button(purchase_frame, text="Choose date", command=lambda: calendar(date_of_order))
        delivery_status_btn = Button(purchase_frame, text="Choose date", command=lambda: calendar(delivery_status))

        date_of_order.grid(row=8, column=1)
        date_of_order_label.grid(row=8, column=0)
        date_btn.grid(row=8, column=2)
        requester.grid(row=9, column=1)
        requester_label.grid(row=9, column=0)
        wbs.grid(row=10, column=1)
        wbs_label.grid(row=10, column=0)
        delivery_status.grid(row=11, column=1, sticky=W)
        delivery_status_label.grid(row=11, column=0)
        delivery_status_btn.grid(row=11, column=2)
    
    elif purchased_var.get() == "0":
        date_of_order.destroy()
        date_of_order_label.destroy()
        date_btn.destroy()
        date_btn.destroy()
        requester.destroy()
        requester_label.destroy()
        wbs.destroy()
        wbs_label.destroy()
        delivery_status.destroy()
        delivery_status_btn.destroy()
        delivery_status_label.destroy()


# Creating entries
cas_number_var = StringVar()
product_name_var = StringVar()
catalogue_num_var = StringVar()
supplier_var = StringVar()

cas_number = ttk.Combobox(entry_frame, width=40, textvariable=cas_number_var)
product_name = ttk.Combobox(entry_frame, width=40, textvariable=product_name_var)
catalogue_num = ttk.Combobox(entry_frame, width=40, textvariable=catalogue_num_var)
currency = OptionMenu(entry_frame, currency_var, *currency_options)
unit_price = Entry(entry_frame, width=40)
unit_qty = Entry(entry_frame, width=40)
unit = OptionMenu(entry_frame, unit_var, *unit_options)
supplier = ttk.Combobox(entry_frame, width=40, textvariable=supplier_var)
website = Entry(entry_frame, width=40)

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


# Creating labels
cas_number_label = Label(entry_frame, text="CAS Number")
product_name_label = Label(entry_frame, text="Product Name")
catalogue_num_label = Label(entry_frame, text="Catalogue Number")
# currency_label = Label(root, text="Currency")
unit_price_label = Label(entry_frame, text="Unit Price")
unit_qty_label = Label(entry_frame, text="Unit Qty")
# unit_label = Label(root, text="Unit")
supplier_label = Label(entry_frame, text="Supplier Name")
website_label = Label(entry_frame, text="Website")

# Putting the labels and entries up
cas_number_label.grid(row=0, column=0, pady=(10,0))
cas_number.grid(row=0, column=1, columnspan=2, pady=(10,0))
product_name_label.grid(row=1, column=0, pady=(10,0))
product_name.grid(row=1, column=1, columnspan=2, pady=(10,0))
catalogue_num_label.grid(row=2, column=0, pady=(10,0))
catalogue_num.grid(row=2, column=1, columnspan=2, pady=(10,0))
# currency_label.grid(row=0, column=0)
currency.grid(row=3, column=1, pady=(10,0))
unit_price_label.grid(row=3, column=0, pady=(10,0))
unit_price.grid(row=3, column=2, columnspan=2, pady=(10,0))
unit_qty_label.grid(row=4, column=0, pady=(10,0))
unit_qty.grid(row=4, column=1, columnspan=2, pady=(10,0))
# unit_label.grid(row=0, column=0)
unit.grid(row=4, column=3, pady=(10,0))
supplier_label.grid(row=5, column=0, pady=(10,0))
supplier.grid(row=5, column=1, columnspan=2, pady=(10,0))
website_label.grid(row=6, column=0, pady=(10,0))
website.grid(row=6, column=1, columnspan=2, pady=(10,0))


# Submit Button (inserting into database)
submit_btn = Button(entry_frame, text="Submit", command=submit)
submit_btn.grid(row=12, column=0)

# Show Button 
show_btn = Button(entry_frame, text="Show catalogue", command=show)
show_btn.grid(row=13, column=0)

# Purchased Button
purchased_var = StringVar()

purchased_btn = Checkbutton(entry_frame, text="Purchase Made", variable=purchased_var, command=purchased)
purchased_btn.deselect()
purchased_btn.grid(row=7, column=0, pady=(15,0))


root.mainloop() 