from tkinter import *
from tkcalendar import Calendar
from tkinter import ttk
import sqlite3
from datetime import date
from tkinter import filedialog
from table_creation_4 import *
import os

root=Tk()
root.title("Purchase Database")
root.geometry("1200x600")

# Creating the menubar
menubar = Menu(root)
root.config(menu=menubar)

# connects to database
conn = sqlite3.connect("purchase_db4.db")
c = conn.cursor()

# Remember order_id of active order
active_order_id = None

# Remember catalogue_id of active catalogue_id
active_catalogue_id = None

# Remember supplier_id of active order
supp_rowid = None

## Popup window feature to ask if user wants to reset the database 
def restart_yes():
    restart("Yes")
    restart_frame.destroy()

restart_frame = Toplevel(root)
restart_label = Label(restart_frame, text="Do you want to reset the database? \n Resetting will clear all existing data.")
restart_yes_btn = Button(restart_frame, text="Yes", command=restart_yes)
restart_no_btn = Button(restart_frame, text="No", command=restart_frame.destroy)

restart_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
restart_yes_btn.grid(row=1, column=0, padx=20, pady=20)
restart_no_btn.grid(row=1, column=1, padx=20, pady=20)
restart_frame.attributes('-topmost', True)

## ---------------- Master functions ---------------- ##
# Switch to receive_frame
def receive():
    main_frame.pack_forget()
    receive_frame.pack()

# Switch to main_frame
def main():
    receive_frame.pack_forget()
    main_frame.pack()

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

# Giving the Comboboxes values previously used
def join_tuples(lst):
    res = ()
    for x in lst:
        res += x
    return res

# Presents strings as active order
def active_order_join(target, active_order_list):
    active_order_str = " | ".join(active_order_list)
    target.config(text=active_order_str)
    return active_order_str

# Tagging of tree row
def tagging(my_tree, records):
    # Create tags
    my_tree.tag_configure('oddrow', background='light blue')
    my_tree.tag_configure('evenrow', background='white')

    count = 0 
    for record in records:
        tup = []
        for val in record:
            tup.append(val)
        tup = tuple(tup)

        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text="Parent", values=tup, tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text="Parent", values=tup, tags=('oddrow',))
        count += 1


# Function to insert values from Treeview into target entry boxes 
def insert_all(entries, values, my_tree=None):

    if my_tree:
        # Grab record number
        selected = my_tree.focus()
        # Grab record values
        values = list(my_tree.item(selected, "values"))

    count = 0
    for entry in entries:
        if isinstance(entry, ttk.Combobox):
            entry.set(values[count])
        elif isinstance(entry, Entry):
            entry.insert(0, values[count])
        elif isinstance(entry, StringVar):
            entry.set(values[count])

        count += 1

## ---------------- End of Master functions ------------- ##

def reset_tree(my_tree):
    # Delete existing rows
    x = my_tree.get_children()
    for record in x:
        my_tree.delete(record)
    
    conn = sqlite3.connect("purchase_db4.db")
    c = conn.cursor()

    c.execute("""SELECT date_of_order, invoice_id, supplier.name, wbs, requester
                        FROM purchase_order 
                        JOIN supplier 
                        ON supplier.supplier_id=purchase_order.supplier_id""")
    records = c.fetchall()

    tagging(my_tree, records)

    conn.commit()
    conn.close()

def reset_open_tree(my_tree):
    # Delete existing rows
    x = my_tree.get_children()
    for record in x:
        my_tree.delete(record)
    
    conn = sqlite3.connect("purchase_db4.db")
    c = conn.cursor()

    c.execute("""SELECT date_of_order, invoice_id, supplier.name, wbs, requester, invoice_address
                    FROM purchase_order 
                    JOIN supplier 
                    ON supplier.supplier_id=purchase_order.supplier_id""")
    records = c.fetchall()

    tagging(my_tree, records)

    conn.commit()
    conn.close()

def reset_receive_tree(my_tree):
    # Delete existing rows
    x = my_tree.get_children()
    for record in x:
        my_tree.delete(record)
    
    conn = sqlite3.connect("purchase_db4.db")
    c = conn.cursor()

    query_value = "%" + query.get() + "%"
    search_cond = query_var_update.get()
    records = []
    # print(sql_columns.values())

    if active_order_id == None:
        query_confirmation_label.config(text="No order chosen!")
    else:
        if search_cond == "Search All":
            if not query.get():
                c.execute("""SELECT catalogue.catalogue_id, product.name, product.cas_number, 
                    catalogue_num, currency, unit_price, unit_qty, unit, 
                    units_received||" "||CHAR(47)||" "||units_bought, website 
                    FROM catalogue JOIN product ON product.cas_number=catalogue.cas_number 
                    JOIN supplier ON supplier.supplier_id=catalogue.supplier_id
                    JOIN item ON item.catalogue_id=catalogue.catalogue_id 
                    JOIN purchase_order ON purchase_order.order_id=item.order_id
                    WHERE item.order_id=?
                    """, (
                    str(active_order_id)
                    ))
                data = c.fetchall()
                records = data
            # else:
                # for cond in sql_columns.values():
                #     sql_command = f"""SELECT purchase_order.order_id, purchase_order.date_of_order, purchase_order.requester, purchase_order.wbs, product.name, product.cas_number, 
                #         supplier.name, catalogue.catalogue_id, catalogue.catalogue_num, catalogue.currency, catalogue.unit_price, catalogue.unit_qty, catalogue.unit, item.units_bought, catalogue.website 
                #         FROM catalogue JOIN product ON product.cas_number=catalogue.cas_number 
                #         JOIN supplier ON supplier.supplier_id=catalogue.supplier_id
                #         JOIN item ON item.catalogue_id=catalogue.catalogue_id 
                #         JOIN purchase_order ON purchase_order.order_id=item.order_id
                #         WHERE {cond} LIKE ?;"""
                #     c.execute(sql_command, (query_value,))
                #     # print(cond, query_value)
                #     # print(cond, ":", data.fetchall())
                #     records += c.fetchall()
        # else:
        #     sql_cond = sql_columns[search_cond]
        #     sql_command = f"""SELECT purchase_order.order_id, purchase_order.date_of_order, purchase_order.requester, purchase_order.wbs, product.name, product.cas_number, 
        #                 supplier.name, catalogue.catalogue_id, catalogue.catalogue_num, catalogue.currency, catalogue.unit_price, catalogue.unit_qty, catalogue.unit, item.units_bought, catalogue.website 
        #                 FROM catalogue JOIN product ON product.cas_number=catalogue.cas_number 
        #                 JOIN supplier ON supplier.supplier_id=catalogue.supplier_id
        #                 JOIN item ON item.catalogue_id=catalogue.catalogue_id 
        #                 JOIN purchase_order ON purchase_order.order_id=item.order_id
        #                 WHERE {sql_cond} LIKE ?;"""
        #     c.execute(sql_command, (query_value,))
        #     # print(data.fetchall())
        #     records += c.fetchall()
        #     # print(search_cond, ":", c.fetchall())

        # print("RECORDS HERE:", records)

        tagging(my_tree, records)

        conn.commit()
        conn.close()

        query_confirmation_label.config(text="Results Shown.")


def submit_new_active_order():
    # "13/05/2022 | 13112000 | Sigma Aldrich | A-0008389-00-00 | Alfred"
    # Date of purchase | Quotation Number | Supplier | WBS | Requester

    active_quote_no = quote_no.get().strip()
    active_supplier = supplier_var.get().strip()
    active_date_purchased = date_purchased.get().strip()
    active_wbs = wbs_var.get().strip()
    active_requester = requester_var.get().strip()

    active_order_list = [active_date_purchased, active_quote_no, active_supplier, active_wbs, active_requester]
    active_order_join(active_order_content, active_order_list)

    conn = sqlite3.connect("purchase_db4.db")
    c = conn.cursor()

    # insert supplier name into supplier table if does not exist
    c.execute("INSERT OR IGNORE INTO supplier (name) VALUES (?)", (active_supplier,))
    
    # retrieve supplier_id from supplier table
    c.execute("SELECT supplier_id FROM supplier WHERE name = ? ", (active_supplier,))

    global supp_rowid
    supp_rowid = c.fetchone()[0]

    # print(supp_rowid)

    # inserts new order into purchase_order table
    c.execute("""INSERT INTO purchase_order (date_of_order, wbs, requester, invoice_id, invoice_address, supplier_id)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (active_date_purchased,
                active_wbs,
                active_requester,
                active_quote_no,
                root.filename,
                supp_rowid)
                )
    
    global active_order_id
    c.execute("SELECT last_insert_rowid();")
    active_order_id = c.fetchone()[0]

    c.execute("""SELECT * FROM purchase_order""")
    print(c.fetchall())

    conn.commit()
    conn.close()
    new_top_level.destroy()

def submit_product():
    # resets main_confirmation_label
    main_confirmation_label.config(text="")

    conn = sqlite3.connect("purchase_db4.db")
    c = conn.cursor()

    prod_name_submit = product_name_var.get().strip()
    cas_num_submit = cas_number_var.get().strip()
    cat_num_submit = catalogue_num_var.get().strip()

    # Checks if cas_number is already in database, and if it is, then don't insert again
    c.execute("INSERT OR IGNORE INTO product (cas_number, name) VALUES (?,?)", (cas_num_submit, prod_name_submit))
    print("Supp_rowid:", supp_rowid)

    if supp_rowid == None:
        main_confirmation_label.config(text="Order not selected!")
    else:
        c.execute("""INSERT OR IGNORE INTO catalogue (catalogue_num, currency, unit_price, unit_qty, unit, website, supplier_id, cas_number)
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

        c.execute("""SELECT catalogue_id FROM catalogue WHERE catalogue.catalogue_num=? AND
                    catalogue.unit_price=? AND catalogue.unit_qty=? AND catalogue.unit=?""", (
                        cat_num_submit, 
                        unit_price.get(), 
                        unit_qty.get(),
                        unit_var.get()
                    ))
        cat_id = c.fetchone()[0]

        c.execute("""INSERT INTO item (catalogue_id, order_id, units_bought)
                        VALUES (?,?,?)""", (
                        cat_id, 
                        active_order_id,
                        units_bought.get()
                        ))

        main_confirmation_label.config(text="Record Submitted!")

        # refreshes the available drop down menu options
        c.execute("""SELECT DISTINCT cas_number FROM product""")
        cas_number['values'] = join_tuples(c.fetchall())

        c.execute("""SELECT DISTINCT name FROM product""")
        product_name['values'] = join_tuples(c.fetchall())

        c.execute("""SELECT DISTINCT catalogue_num FROM catalogue""")
        catalogue_num['values'] = join_tuples(c.fetchall())

        conn.commit()
        conn.close()
        empty_all(main_frame_entries_list)
        main_confirmation_label.config(text="")


def submit_lmms():
    conn = sqlite3.connect("purchase_db4.db")
    c = conn.cursor()

    if active_catalogue_id == None and active_order_id == None:
        lmms_confirmation_label.config(text="No order and catalogue chosen!")
    elif active_catalogue_id == None:
        lmms_confirmation_label.config(text="No catalogue chosen!")
    elif active_order_id == None:
        lmms_confirmation_label.config(text="No order chosen!")
    else:
        c.execute("INSERT INTO lmms (lmms, catalogue_id, order_id) VALUES (?,?,?)", (
                    lmms_num.get(),
                    active_catalogue_id,
                    active_order_id
                    ))

        c.execute("SELECT lmms FROM lmms WHERE catalogue_id=? AND order_id=?", (
                    active_catalogue_id,
                    active_order_id
                    ))
        length = c.fetchall()
        print(length)
        og_units_received = str(len(length))
        print("og_units:", og_units_received)

        c.execute("""UPDATE item SET units_received=?, batch_num=?, exp_date=?
                        WHERE catalogue_id=? AND order_id=?""", (
                        og_units_received,
                        batch_num.get(),
                        exp_date.get(),
                        active_catalogue_id,
                        active_order_id
                        ))

        c.execute("SELECT * FROM item")
        print(c.fetchall())
        empty_all(lmms_frame_submit_list)

        conn.commit()
        conn.close()
        lmms_confirmation_label.config(text="LMMS Submitted!")

        reset_receive_tree(receive_tree)

# ----------------------- Testing code ----------------------- #
# c.execute("""SELECT * FROM lmms""")
# print("LMMS:", c.fetchall())
# c.execute("""SELECT * FROM product""")
# print("Product:", c.fetchall())
# ----------------------- Testing code ends ------------------ #

def popup_new():
    def open_file():
        # preset initial directory
        root.filename = filedialog.askopenfilename(initialdir="gallery_image_viewer/images", title="Select A File", filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
        invoice_link.insert(0, root.filename)
        # os.system('"%s"' % root.filename)

    global new_top_level
    new_top_level = Toplevel(root)
    new_top_level.geometry("400x300")

    global supplier_var
    global wbs_var
    global requester_var

    supplier_var = StringVar()
    wbs_var = StringVar()
    requester_var = StringVar()

    global quote_no
    global date_purchased

    quote_no = Entry(new_top_level, width=20)
    quote_no_label = Label(new_top_level, text="Quotation Number:")
    supplier_label = Label(new_top_level, text="Supplier Name")
    supplier = ttk.Combobox(new_top_level, width=20, textvariable=supplier_var)
    date_purchased_label = Label(new_top_level, text="Date of Purchase")
    date_purchased = Entry(new_top_level, width=20)
    wbs_label = Label(new_top_level, text="WBS")
    wbs = ttk.Combobox(new_top_level, width=20, textvariable=wbs_var)
    requester_label = Label(new_top_level, text="Requester")
    requester = ttk.Combobox(new_top_level, width=20, textvariable=requester_var)
    invoice_num_label = Label(new_top_level, text="Invoice Address:")
    invoice_link = Entry(new_top_level, width=20)
    invoice_selection = Button(new_top_level, text="Select File", command=open_file)

    new_date_btn = Button(new_top_level, text="Choose date", command=lambda: calendar(date_purchased))

    submit_new_order_btn = Button(new_top_level, text="Submit", command=submit_new_active_order)

    quote_no_label.grid(row=0, column=0, pady=(20,5))
    quote_no.grid(row=0, column=1, pady=(20,5))
    supplier.grid(row=1, column=1, pady=(20,5))
    supplier_label.grid(row=1, column=0, pady=(20,5))
    date_purchased.grid(row=2, column=1, pady=5)
    date_purchased_label.grid(row=2, column=0, pady=5)
    new_date_btn.grid(row=2, column=2, padx=5, pady=5, sticky=W)
    wbs.grid(row=3, column=1, pady=5)
    wbs_label.grid(row=3, column=0, pady=5)
    requester.grid(row=4, column=1, pady=5)
    requester_label.grid(row=4, column=0, pady=5)
    submit_new_order_btn.grid(row=6, column=3, pady=5)
    invoice_num_label.grid(row=5, column=0, padx=5, pady=5)
    invoice_link.grid(row=5, column=1, padx=5, pady=5)
    invoice_selection.grid(row=5, column=2, padx=5, pady=5)

    # autofill date entry box with today's date
    today = date.today()
    date_purchased.insert(0, today.strftime("%d/%m/%Y"))

    
def popup_continue():
    continue_top_level = Toplevel(root)
    
    continue_tree = ttk.Treeview(continue_top_level)

    continue_tree['columns'] = (
        'Date of Order',
        'Quote Number',
        'Supplier',
        'WBS',
        'Requester'
    )

    continue_tree.column("Date of Order", width=80)
    continue_tree.column("Quote Number", width=80)
    continue_tree.column("Supplier", width=80)
    continue_tree.column("WBS", width=80)
    continue_tree.column("Requester", width=80)

    continue_tree.column('#0', width=0, stretch=NO)
    
    continue_tree.heading("#0", text='Label')
    continue_tree.heading('Date of Order', text='Date of Order')
    continue_tree.heading('Quote Number', text='Quote Number')
    continue_tree.heading('Supplier', text='Supplier')
    continue_tree.heading('WBS', text='WBS')
    continue_tree.heading('Requester', text='Requester')

    continue_tree.pack(padx=20, pady=20)
    reset_tree(continue_tree)

    def select(my_tree):
        # Grab record number
        selected = my_tree.focus()
        # Grab record values
        records = my_tree.item(selected, "values")
        # Put selected values into active order section
        active_order_join(active_order_content, records)
        doo, qu_no, supp_name, wbs, req = records

        # To update active_order_id
        with sqlite3.connect("purchase_db4.db") as conn:
            c = conn.cursor()
            c.execute("SELECT supplier_id FROM supplier WHERE name=?",
                        (supp_name,))

            global supp_rowid
            supp_rowid = int(c.fetchone()[0])

            c.execute("""SELECT order_id FROM purchase_order WHERE date_of_order=? AND invoice_id=? AND
                            supplier_id=? AND wbs=? AND requester=?""", 
                            (doo, qu_no, supp_rowid, wbs, req))

            global active_order_id
            active_order_id = c.fetchone()[0]

        continue_top_level.destroy()

    my_button = Button(continue_top_level, text="Select", command=lambda: select(continue_tree))
    my_button.pack(padx=20, pady=20)

def select_active_item(my_tree):
    # Grab record number
    selected = my_tree.focus()
    # Grab record values
    values = list(my_tree.item(selected, "values"))

    global active_catalogue_id
    active_catalogue_id = values[0]

    active_order_join(active_item_content, values[1:])
    # empty_all(lmms_frame_entries_list)

def open_file():
    open_file_top_level = Toplevel(root)

    global open_file_tree
    
    open_file_tree = ttk.Treeview(open_file_top_level)

    open_file_tree['columns'] = (
        'Date of Order',
        'Quote Number',
        'Supplier',
        'WBS',
        'Requester',
        'Invoice Link'
    )

    open_file_tree.column("Date of Order", width=80)
    open_file_tree.column("Quote Number", width=80)
    open_file_tree.column("Supplier", width=80)
    open_file_tree.column("WBS", width=80)
    open_file_tree.column("Requester", width=80)
    open_file_tree.column("Invoice Link", width=100)

    open_file_tree.column('#0', width=0, stretch=NO)
    
    open_file_tree.heading("#0", text='Label')
    open_file_tree.heading('Date of Order', text='Date of Order')
    open_file_tree.heading('Quote Number', text='Quote Number')
    open_file_tree.heading('Supplier', text='Supplier')
    open_file_tree.heading('WBS', text='WBS')
    open_file_tree.heading('Requester', text='Requester')
    open_file_tree.heading("Invoice Link", text="Invoice Link")

    open_file_tree.pack(padx=20, pady=20)
    reset_open_tree(open_file_tree)

    def opening(my_tree):
        # Grab record number
        selected = my_tree.focus()
        # Grab record values
        records = my_tree.item(selected, "values")
        # Put selected values into active order section
        active_link = records[-1]

        os.system('"%s"' % active_link)

        open_file_top_level.destroy()

    my_button = Button(open_file_top_level, text="Select", command=lambda: opening(open_file_tree))
    my_button.pack(padx=20, pady=20)


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
        if select_level:
            select_level.destroy()

    if len(records) > 1:
        select_level = Toplevel()
        select_level.geometry("1000x400")
        # Creating Treeview for select_level
        my_tree = ttk.Treeview(select_level, columns=( 
                                "Product name", 
                                "CAS number",
                                "Catalogue number",
                                "Currency",
                                "Unit Price",
                                "Unit Quantity",
                                "Unit",
                                "Website"))

        select_autofill_btn = Button(select_level, text="Select", command=select_autofill)

        # Packing my_tree to select_level
        my_tree.pack(expand=TRUE, fill=X)
        select_autofill_btn.pack(padx=10, pady=10, anchor=NE)

        # Formatting our columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Product name", width=80, stretch=YES)
        my_tree.column("CAS number", width=80)
        my_tree.column("Catalogue number", width=80)
        my_tree.column("Currency", width=60)
        my_tree.column("Unit Price", width=80)
        my_tree.column("Unit Quantity", width=80)
        my_tree.column("Unit", width=50)
        my_tree.column("Website", width=80)

        # Create Headings
        my_tree.heading("#0", text="Label", anchor=W)
        my_tree.heading("Product name", text="Product name", anchor=W)
        my_tree.heading("CAS number", text="CAS number", anchor=W)
        my_tree.heading("Catalogue number", text="Catalogue number", anchor=W)
        my_tree.heading("Currency", text="Currency", anchor=W)
        my_tree.heading("Unit Price", text="Unit Price", anchor=CENTER)
        my_tree.heading("Unit Quantity", text="Unit Quantity", anchor=W)
        my_tree.heading("Unit", text="Unit", anchor=W)
        my_tree.heading("Website", text="Website", anchor=W)

        count = 0
        for record in records:
            my_tree.insert(parent='', index='end', iid=count, text="Parent", values=(record[0], record[1], record[2], 
                        record[3], record[4],record[5],record[6],record[7]))
            count += 1
    elif len(records) == 0:
        main_confirmation_label.config(text="No records found!")
    else:
        select_level = None
        select_autofill(records[0])

def auto_main():
    global records
    
    conn = sqlite3.connect("purchase_db4.db")
    c = conn.cursor()

    cat_num_submit = catalogue_num_var.get().strip()
    cas_num_submit = cas_number_var.get().strip()

    if cat_num_submit:
        c.execute("""SELECT product.name, product.cas_number, catalogue.catalogue_num, 
            catalogue.currency, catalogue.unit_price, catalogue.unit_qty, catalogue.unit, catalogue.website 
            FROM catalogue 
            JOIN product ON product.cas_number=catalogue.cas_number 
            JOIN supplier ON supplier.supplier_id=catalogue.supplier_id
            JOIN item ON item.catalogue_id=catalogue.catalogue_id 
            JOIN purchase_order ON purchase_order.order_id=item.order_id
            WHERE catalogue.catalogue_num = ? """, (cat_num_submit,))
        records = c.fetchall()
        # print("Cat_num:", records)
        auto_main_popup(records)

    elif cas_num_submit:
        c.execute("""SELECT product.name, product.cas_number, catalogue.catalogue_num, 
            catalogue.currency, catalogue.unit_price, catalogue.unit_qty, catalogue.unit, catalogue.website
            FROM catalogue 
            JOIN product ON product.cas_number=catalogue.cas_number 
            JOIN supplier ON supplier.supplier_id=catalogue.supplier_id
            JOIN item ON item.catalogue_id=catalogue.catalogue_id 
            JOIN purchase_order ON purchase_order.order_id=item.order_id
            WHERE product.cas_number = ? """, (cas_num_submit,))
        records = c.fetchall()
        # print("CAS_num_submit:",records)
        auto_main_popup(records)

    else:
        main_confirmation_label.config(text="No Value Provided.")

new_menu = Menu(menubar, tearoff=False)
new_menu.add_command(label='New Order', command=popup_new)
new_menu.add_command(label='Continue Saved Order', command=popup_continue)

add_menu = Menu(menubar, tearoff=False)
add_menu.add_command(label="Add Product", command=main)
add_menu.add_command(label="Update LMMS", command=receive)

menubar.add_cascade(label='Select', menu=new_menu, underline=0)
menubar.add_cascade(label='Add', menu=add_menu, underline=0)

## Creating active order section
active_order_frame = Frame(root, padx=20, pady=10)
active_order_frame.pack()

## Creating content for active_order_frame
active_order_label = Label(active_order_frame, text="Active Order")
active_order_label.config(fg="red")
active_order_content = Label(active_order_frame, text="-- None Selected --")

open_file_btn = Button(active_order_frame, text="Open File", command=open_file)

active_order_label.grid(row=0, column=1)
active_order_content.grid(row=1, column=1)
open_file_btn.grid(row=0, column=0, sticky='w')

# Creating separator between active order section and main_frame
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')

## Main console Frame
main_frame = LabelFrame(root, text="Product Details", padx=20, pady=20)
main_frame.pack(padx=20, pady=20)

## Creating content for main_frame
# Creating labels
catalogue_num_label = Label(main_frame, text="Catalogue Number")
product_name_label = Label(main_frame, text="Product Name")
cas_number_label = Label(main_frame, text="CAS Number")

catalogue_num_var = StringVar()
product_name_var = StringVar()
cas_number_var = StringVar()

catalogue_num = ttk.Combobox(main_frame, width=20, textvariable=catalogue_num_var)
product_name = ttk.Combobox(main_frame, width=20, textvariable=product_name_var)
cas_number = ttk.Combobox(main_frame, width=20, textvariable=cas_number_var)

autofill_btn_main = Button(main_frame, text="Autofill", command=auto_main)

# Dealing with currency for unit_price
currency_options = ["SGD", "USD"]
currency_var = StringVar()
currency_options_default = currency_options[0]
currency_var.set(currency_options_default)

# Dealing with units for unit_qty
unit_options = ["g", "kg", "ml", "L", ]
unit_var = StringVar()
unit_options_default = unit_options[0]
unit_var.set(unit_options_default)

website_label = Label(main_frame, text="Website")
unit_price_label = Label(main_frame, text="Unit Price")
unit_qty_label = Label(main_frame, text="Unit")
units_bought_label = Label(main_frame, text="Units Bought")
unit_qty_explanation = Label(main_frame, text="* Unit: the standard quantity of measure.")
units_bought_explanation = Label(main_frame, text="* Units Bought: the number of units purchased.")

website = Entry(main_frame, width=20)
currency = OptionMenu(main_frame, currency_var, *currency_options)
unit_price = Entry(main_frame, width=20)
unit_qty = Entry(main_frame, width=20)
unit = OptionMenu(main_frame, unit_var, *unit_options)
units_bought = Entry(main_frame, width=20)

# Label which will reflect outcome of clicking clear all and submit buttons
main_confirmation_label = Label(main_frame, text="")

# Clear all entry and submit entries buttons
clear_main_btn = Button(main_frame, text="Clear All", command=lambda: empty_all(main_frame_entries_list))
submit_main_btn = Button(main_frame, text="Submit", command=submit_product)

# Packing the content for main frame
catalogue_num_label.grid(row=0, column=0, pady=5)
catalogue_num.grid(row=0, column=1, pady=5, sticky=W)
cas_number_label.grid(row=0, column=2, pady=5, padx=(30,0))
cas_number.grid(row=0, column=3, pady=5, sticky=W)
product_name_label.grid(row=1, column=0, pady=5, padx=(30,0))
product_name.grid(row=1, column=1, pady=5, sticky=W)
autofill_btn_main.grid(row=1, column=3, pady=5, sticky=E)
website.grid(row=2, column=1, pady=(20,5))
website_label.grid(row=2, column=0, padx=(30,0), pady=(20,5))
unit_price.grid(row=3, column=1, pady=(10,5))
unit_price_label.grid(row=3, column=0, pady=(10,5))
currency.grid(row=3, column=2, pady=(10,5), sticky=W)
unit_qty.grid(row=4, column=1, pady=5)
unit_qty_label.grid(row=4, column=0, pady=5)
unit.grid(row=4, column=2, sticky=W, padx=5, pady=5)
unit_qty_explanation.grid(row=4, column=3, padx=5, pady=5, sticky=W)
units_bought.grid(row=6, column=1, pady=5)
units_bought_label.grid(row=6, column=0, pady=5)
units_bought_explanation.grid(row=6, column=3, padx=5, pady=5, sticky=W)
main_confirmation_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky=W)
clear_main_btn.grid(row=8, column=2, padx=5, pady=5, sticky=E)
submit_main_btn.grid(row=8, column=3, padx=5, pady=5, sticky=E)

order_btn = Button(main_frame, text="Order_id", command=lambda: print(active_order_id))
# order_btn.grid(row=10, column=3, padx=5, pady=5, stick=E)

supp_btn = Button(main_frame, text="Catalogue_rowid", command=lambda: print(active_catalogue_id))
# supp_btn.grid(row=10, column=2, padx=5, pady=5, stick=E)

# refreshes the available drop down menu options
c.execute("""SELECT DISTINCT cas_number FROM product""")
cas_number['values'] = join_tuples(c.fetchall())

c.execute("""SELECT DISTINCT name FROM product""")
product_name['values'] = join_tuples(c.fetchall())

c.execute("""SELECT DISTINCT catalogue_num FROM catalogue""")
catalogue_num['values'] = join_tuples(c.fetchall())


## ---------------- Receive console Frame ---------------- ##
receive_frame = Frame(root, padx=20, pady=5)

## Creating query_frame for searching and displaying in receive_tree
query_frame = Frame(receive_frame, padx=20)
query_frame.pack()

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
query_btn = Button(query_frame, text="Go", command=lambda: reset_receive_tree(receive_tree))

query_confirmation_label = Label(query_frame, text="")

query_label.grid(row=0, column=0, padx=5)
query.grid(row=0, column=1)
query_conditions.grid(row=0, column=2, padx=10)
query_btn.grid(row=0, column=3, padx=10)
query_confirmation_label.grid(row=1, column=0, columnspan=4, padx=10, pady=(10,0))

receive_tree = ttk.Treeview(receive_frame, columns=("Catalogue ID",
                                            "Product Name",
                                            "CAS number",
                                            "Catalogue number",
                                            "Currency",
                                            "Unit Price",
                                            "Unit Quantity",
                                            "Unit",
                                            "Tally",
                                            "Website"))

receive_tree.pack(padx=10, pady=10)

# Formatting our columns
receive_tree.column("#0", width=0, stretch=NO)
receive_tree.column("Catalogue ID", width=100)
receive_tree.column("Product Name", width=120, stretch=YES)
receive_tree.column("CAS number", width=100)
receive_tree.column("Catalogue number", width=100)
receive_tree.column("Currency", width=60)
receive_tree.column("Unit Price", width=80)
receive_tree.column("Unit Quantity", width=80)
receive_tree.column("Unit", width=50)
receive_tree.column("Tally", width=50)
receive_tree.column("Website", width=80)

# Create Headings
receive_tree.heading("#0", text="Label", anchor=W)
receive_tree.heading("Catalogue ID", text="Catalogue ID", anchor=W)
receive_tree.heading("Product Name", text="Product Name", anchor=W)
receive_tree.heading("CAS number", text="CAS number", anchor=W)
receive_tree.heading("Catalogue number", text="Catalogue number", anchor=W)
receive_tree.heading("Currency", text="Currency", anchor=W)
receive_tree.heading("Unit Price", text="Unit Price", anchor=CENTER)
receive_tree.heading("Unit Quantity", text="Unit Quantity", anchor=W)
receive_tree.heading("Unit", text="Unit", anchor=W)
receive_tree.heading("Tally", text="Tally", anchor=CENTER)
receive_tree.heading("Website", text="Website", anchor=W)

receive_tree.bind("<Double-1>", lambda e: select_active_item(receive_tree))


# Creating separator between receive_tree section and active ITEM section
separator = ttk.Separator(receive_frame, orient='horizontal')
separator.pack(fill='x', expand=TRUE)

## Creating active ITEM section
active_item_frame = Frame(receive_frame, padx=20, pady=10)
active_item_frame.pack()

## Creating content for active_order_frame
active_item_label = Label(active_item_frame, text="Active Item")
active_item_label.config(fg="red")
active_item_content = Label(active_item_frame, text="-- None Selected --")

active_item_label.grid(row=0, column=0, sticky='w')
active_item_content.grid(row=1, column=0, sticky='w')

# Creating separator between active ITEM section and lmms_frame
separator = ttk.Separator(receive_frame, orient='horizontal')
separator.pack(fill='x')


## Creating the lmms_frame
lmms_frame = LabelFrame(receive_frame, text="Item Details", padx=20, pady=20)
lmms_frame.pack()

## Creating content for lmms_frame
# Creating labels
lmms_num_label = Label(lmms_frame, text="LMMS Number:")
batch_num_label = Label(lmms_frame, text="Batch Number:")
exp_date_label = Label(lmms_frame, text="Expiry Date:")
delivery_date_label = Label(lmms_frame, text="Delivery Date:")

lmms_num = Entry(lmms_frame, width=20)
batch_num = Entry(lmms_frame, width=20)
exp_date = Entry(lmms_frame, width=20)
delivery_date = Entry(lmms_frame, width=20)

exp_date_btn = Button(lmms_frame, text="Choose date", command=lambda: calendar(exp_date))
receive_date_btn = Button(lmms_frame, text="Choose date", command=lambda: calendar(delivery_date))

# Clear all entry and submit entries buttons
clear_receive_btn = Button(lmms_frame, text="Clear All", command=lambda: empty_all(lmms_frame_entries_list))
submit_receive_btn = Button(lmms_frame, text="Submit", command=submit_lmms)

# Label which will reflect outcome of clicking clear all and submit buttons
lmms_confirmation_label = Label(lmms_frame, text="")

lmms_num_label.grid(row=1, column=0, padx=5, pady=5)
lmms_num.grid(row=1, column=1, padx=5, pady=5)
batch_num_label.grid(row=2, column=0, padx=5, pady=5)
batch_num.grid(row=2, column=1, padx=5, pady=5)
exp_date_label.grid(row=3, column=0, padx=5, pady=5)
exp_date.grid(row=3, column=1, padx=5, pady=5)
exp_date_btn.grid(row=3, column=2, padx=5, pady=5)
delivery_date_label.grid(row=4, column=0, padx=5, pady=5)
delivery_date.grid(row=4, column=1, padx=5, pady=5)
receive_date_btn.grid(row=4, column=2, padx=5, pady=5)
lmms_confirmation_label.grid(row=5, column=0, padx=5, pady=10)
clear_receive_btn.grid(row=5, column=1, padx=5, pady=10)
submit_receive_btn.grid(row=5, column=2, padx=5, pady=10)

# autofill date entry box with today's date
today = date.today()
delivery_date.insert(0, today.strftime("%d/%m/%Y"))

# Creating a list of all entry box names for empty_all function
main_frame_entries_list = [cas_number, product_name, catalogue_num, (currency_var, currency_options_default), (unit_var, unit_options_default), unit_price, unit_qty, website, units_bought]
lmms_frame_submit_list = [lmms_num]
lmms_frame_entries_list = [lmms_num, batch_num, exp_date, delivery_date]

main_frame_insert_list = [product_name, cas_number, catalogue_num, currency_var, unit_price, unit_qty, unit_var, website]

conn.commit()
conn.close()
root.mainloop()