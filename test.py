import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

def create_database_connection():
    return sqlite3.connect("inventory_data.db")

def initialize_database():
    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            item_category TEXT NOT NULL,
            stock_quantity INTEGER NOT NULL,
            item_price REAL NOT NULL,
            supplier_info TEXT,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            action_type TEXT,
            old_value TEXT,
            new_value TEXT,
            change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()

def add_new_inventory_item():
    try:
        name = item_name_input.get()
        category = category_dropdown.get()
        quantity = int(quantity_input.get())
        price = float(price_input.get())
        supplier = supplier_input.get()

        connection = create_database_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO inventory_items (item_name, item_category, stock_quantity, item_price, supplier_info)
            VALUES (?, ?, ?, ?, ?)
        """, (name, category, quantity, price, supplier))
        connection.commit()
        connection.close()

        log_inventory_activity("ADD", None, None, f"Added: {name} with {quantity} units")
        messagebox.showinfo("Success", f"{name} has been successfully added to inventory!")
        refresh_inventory_list()
    except Exception as error:
        messagebox.showerror("Error", f"An error occurred while adding the item: {error}")

def remove_inventory_item():
    selected_item = inventory_table.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to delete.")
        return

    item_id = inventory_table.item(selected_item)['values'][0]

    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM inventory_items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    connection.close()

    if item:
        connection = create_database_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM inventory_items WHERE id = ?", (item_id,))
        connection.commit()
        connection.close()

        log_inventory_activity("DELETE", item_id, f"{item[1]}: {item[3]} units", None)
        messagebox.showinfo("Deleted", f"{item[1]} has been removed from the inventory!")
        refresh_inventory_list()

def refresh_inventory_list():
    for row in inventory_table.get_children():
        inventory_table.delete(row)

    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM inventory_items")
    rows = cursor.fetchall()
    connection.close()

    for row in rows:
        inventory_table.insert("", "end", values=row)

def search_inventory_items():
    search_query = search_box.get().lower()

    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM inventory_items WHERE item_name LIKE ?", ('%' + search_query + '%',))
    rows = cursor.fetchall()
    connection.close()

    for row in inventory_table.get_children():
        inventory_table.delete(row)
    for row in rows:
        inventory_table.insert("", "end", values=row)

def check_for_low_stock():
    low_stock_threshold = 5
    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT item_name, stock_quantity FROM inventory_items WHERE stock_quantity < ?", (low_stock_threshold,))
    low_stock_items = cursor.fetchall()
    connection.close()

    if low_stock_items:
        alert_message = "\n".join([f"{item[0]}: {item[1]}" for item in low_stock_items])
        messagebox.showwarning("Low Stock Alert", f"The following items have low stock:\n{alert_message}")
    else:
        messagebox.showinfo("Stock Status", "All items are sufficiently stocked.")

def display_inventory_statistics():
    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT item_category, SUM(stock_quantity) FROM inventory_items GROUP BY item_category")
    stats = cursor.fetchall()
    connection.close()

    stats_message = ""
    for category, total_quantity in stats:
        stats_message += f"{category}: {total_quantity} items\n"

    if stats_message:
        messagebox.showinfo("Inventory Statistics", stats_message)
    else:
        messagebox.showinfo("Inventory Statistics", "No data available.")

def log_inventory_activity(action, item_id, old_value, new_value):
    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO inventory_changes (item_id, action_type, old_value, new_value)
        VALUES (?, ?, ?, ?)
    """, (item_id, action, old_value, new_value))
    connection.commit()
    connection.close()

# GUI SETUP
main_app = tk.Tk()
main_app.title("Inventory Management System")
main_app.geometry("1920x1080")
main_app.configure(bg="#e1f5fe")  # Light blue background

initialize_database()

# Input Section
input_frame = tk.Frame(main_app, padx=20, pady=10, bg="#e1f5fe")
input_frame.pack(fill=tk.X, pady=10)

# Item Name
tk.Label(input_frame, text="Item Name", bg="#e1f5fe", font=("Arial", 12)).grid(row=0, column=0, padx=10, sticky="w")
item_name_input = tk.Entry(input_frame, font=("Arial", 12))
item_name_input.grid(row=0, column=1, padx=10, pady=5)

# Category
tk.Label(input_frame, text="Category", bg="#e1f5fe", font=("Arial", 12)).grid(row=1, column=0, padx=10, sticky="w")
category_dropdown = ttk.Combobox(input_frame, values=["Electronics", "Clothing", "Food", "Other"], state="readonly", font=("Arial", 12))
category_dropdown.grid(row=1, column=1, padx=10, pady=5)
category_dropdown.current(0)

# Quantity
tk.Label(input_frame, text="Quantity", bg="#e1f5fe", font=("Arial", 12)).grid(row=2, column=0, padx=10, sticky="w")
quantity_input = tk.Entry(input_frame, font=("Arial", 12))
quantity_input.grid(row=2, column=1, padx=10, pady=5)

# Price
tk.Label(input_frame, text="Price", bg="#e1f5fe", font=("Arial", 12)).grid(row=3, column=0, padx=10, sticky="w")
price_input = tk.Entry(input_frame, font=("Arial", 12))
price_input.grid(row=3, column=1, padx=10, pady=5)

# Supplier
tk.Label(input_frame, text="Supplier", bg="#e1f5fe", font=("Arial", 12)).grid(row=4, column=0, padx=10, sticky="w")
supplier_input = tk.Entry(input_frame, font=("Arial", 12))
supplier_input.grid(row=4, column=1, padx=10, pady=5)

# Search Box
tk.Label(input_frame, text="Search", bg="#e1f5fe", font=("Arial", 12)).grid(row=5, column=0, padx=10, sticky="w")
search_box = tk.Entry(input_frame, font=("Arial", 12))
search_box.grid(row=5, column=1, padx=10, pady=5)

# Button Panel
button_frame = tk.Frame(main_app, bg="#e1f5fe")
button_frame.pack(pady=20)

# Add Item Button
tk.Button(button_frame, text="Add Item", command=add_new_inventory_item, bg="#4caf50", fg="white", font=("Arial", 12), padx=10, pady=10).grid(row=0, column=0, padx=10)

# Delete Item Button
tk.Button(button_frame, text="Delete Item", command=remove_inventory_item, bg="#f44336", fg="white", font=("Arial", 12), padx=10, pady=10).grid(row=0, column=1, padx=10)

# Show Stats Button
tk.Button(button_frame, text="Show Stats", command=display_inventory_statistics, bg="#2196f3", fg="white", font=("Arial", 12), padx=10, pady=10).grid(row=0, column=2, padx=10)

# Low Stock Alert Button
tk.Button(button_frame, text="Low Stock Alert", command=check_for_low_stock, bg="#ff9800", fg="white", font=("Arial", 12), padx=10, pady=10).grid(row=0, column=3, padx=10)

# Search Button
tk.Button(button_frame, text="Search", command=search_inventory_items, bg="#64b5f6", fg="white", font=("Arial", 12), padx=10, pady=10).grid(row=1, column=0, columnspan=4, pady=10)

# Treeview for Inventory Table
treeview_style = ttk.Style()
treeview_style.configure("Treeview", background="#ffffff", rowheight=30, font=("Arial", 12))
treeview_style.configure("Treeview.Heading", background="#64b5f6", foreground="black", font=("Arial", 13, "bold"))

columns = ("ID", "Item", "Category", "Quantity", "Cost", "Supplier", "Date Added")
inventory_table = ttk.Treeview(main_app, columns=columns, show="headings", style="Treeview")
inventory_table.pack(fill=tk.BOTH, padx=20, pady=20)

# Set up column headers
for col in columns:
    inventory_table.heading(col, text=col)
    inventory_table.column(col, width=120)

# Initial inventory load
refresh_inventory_list()

main_app.mainloop()