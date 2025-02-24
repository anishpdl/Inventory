import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk,Image
import sqlite3
import tkinter.font as font
import runpy
import config
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
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user TEXT NOT NULL
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
        name = entries["Item Name"].get()
        category = entries["Category"].get()
        quantity = int(entries["Quantity"].get())
        price = float(entries["Price"].get())
        supplier = entries["Supplier"].get()

        # Ensure logged_user is not None or empty
        if not config.logged_user:
            raise ValueError("User not logged in. Please log in first.")

        connection = create_database_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO inventory_items (item_name, item_category, stock_quantity, item_price, supplier_info, user)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, category, quantity, price, supplier, config.logged_user))
        connection.commit()
        connection.close()

        log_inventory_activity("ADD", None, None, f"Added: {name} with {quantity} units")
        messagebox.showinfo("Success", f"{name} has been successfully added to inventory!")
        refresh_inventory_list()
    except ValueError as ve:
        messagebox.showerror("User Error", str(ve))
    except Exception as error:
        messagebox.showerror("Error", f"An error occurred while adding the item: {error}")


def remove_inventory_item():
    selected_item = inventory_table.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to delete.")
        return
    
    item_details = inventory_table.item(selected_item)

    item_name = item_details['values'][1]
     
    connection = sqlite3.connect('inventory_data.db') 
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM inventory_items WHERE item_name = ?", (item_name,))
    result = cursor.fetchone()
    item_id=result[0]

    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM inventory_items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    connection.close()

    if item:
        connection = create_database_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM inventory_items WHERE id = ? AND user = ?", (item_id,config.logged_user))
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
    cursor.execute("SELECT item_name, item_category, stock_quantity, item_price, supplier_info, date_added FROM inventory_items WHERE user = ?", (config.logged_user,))
    rows = cursor.fetchall()
    connection.close()


    # Insert rows with Serial Number
    for sn, row in enumerate(rows, start=1):  # SN starts from 1
        inventory_table.insert("", "end", values=(sn, *row))

    # for row in rows:
    #     inventory_table.insert("", "end", values=row)

def search_inventory_items():
    search_query = search_btn.get()

    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, item_name, item_category, stock_quantity, item_price, supplier_info, date_added FROM inventory_items WHERE item_name LIKE ? AND user = ?", ('%' + search_query + '%', config.logged_user))
    rows = cursor.fetchall()
    connection.close()

    # Clear previous entries
    for row in inventory_table.get_children():
        inventory_table.delete(row)

    # Insert the new search results
    for sn, row in enumerate(rows, start=1):  # SN starts from 1
        item_id, item_name, item_category, stock_quantity, item_price, supplier_info, date_added = row
        # Insert values, including date_added
        inventory_table.insert("", "end", values=(sn, item_name, item_category, stock_quantity, item_price, supplier_info, date_added)) 




def check_for_low_stock():
    low_stock_threshold = 5
    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT item_name, stock_quantity FROM inventory_items WHERE stock_quantity < ? AND user = ?", (low_stock_threshold,config.logged_user))
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
    cursor.execute("SELECT item_category, SUM(stock_quantity) FROM inventory_items WHERE user = ? GROUP BY item_category", (config.logged_user,))
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

# Create main window
main_app = tk.Tk()
main_app.title("Inventory Management System")
main_app.geometry("1920x1080")
main_app.attributes("-fullscreen", True)
main_app.configure(bg="#f7fafc")  # Very light background

# Get screen dimensions
screen_width = main_app.winfo_screenwidth()
screen_height = main_app.winfo_screenheight()

# ================= Header Section ==================
header_frame = tk.Frame(main_app, bg="#34495e", height=65)
header_frame.pack(side=tk.TOP, fill=tk.X)

# Logo in Header
try:
    logo_img = Image.open(r"assets/logo.png")
except Exception as e:
    logo_img = Image.open("logo.png")
logo_img = logo_img.resize((55, 55))
logo_photo = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(header_frame, image=logo_photo, bg="#34495e")
logo_label.pack(side=tk.LEFT, padx=20, pady=5)

# Title in Header
title_label = tk.Label(header_frame, text="Cloud Inventory", font=("Comic Sans MS", 24, "bold"), bg="#34495e", fg="white")
title_label.pack(side=tk.LEFT, padx=10)

# Header Buttons (Minimize & Close)
buttonFont = font.Font(size=18, weight="bold")

def minimize_app():
    main_app.iconify()

def close_app():
    if messagebox.askquestion('Exit Application', 'Are you sure you want to close the application?', icon='warning') == 'yes':
        main_app.destroy()

min_btn = tk.Button(header_frame, text="-", command=minimize_app, bg="#34495e", fg="white", bd=0, font=buttonFont,
                    activebackground="#2c3e50", activeforeground="white", cursor="hand2")
min_btn.pack(side=tk.RIGHT, padx=10, pady=10)

close_btn = tk.Button(header_frame, text="✕", command=close_app, bg="#34495e", fg="white", bd=0, font=buttonFont,
                      activebackground="#e74c3c", activeforeground="white", cursor="hand2")
close_btn.pack(side=tk.RIGHT, padx=10, pady=10)

# ================= Profile and Logout Section ==================
profile_frame = tk.Frame(main_app, bg="white", bd=2, relief=tk.RIDGE)
profile_frame.place(x=1240, y=screen_height-870, width=200, height=75)
profile_frame.lift()

# Profile Image
try:
    profile_img = Image.open("assets/logo.png")
except Exception as e:
    profile_img = Image.open("logo.png")
profile_img = profile_img.resize((50, 50))
profile_photo = ImageTk.PhotoImage(profile_img)
profile_img_label = tk.Label(profile_frame, image=profile_photo, bg="white")
profile_img_label.grid(row=0, column=0, padx=10, pady=10)

# Username Label
username_label = tk.Label(profile_frame, text=config.logged_user, font=("Arial", 16, "bold"), bg="white", fg="#34495e")
username_label.grid(row=0, column=1, padx=5, sticky="w")

# Logout Button with Hover Effect
def logout():
    main_app.destroy()
    print("User logged out!")
    runpy.run_path('login.py')

def on_logout_enter(e):
    logout_btn.config(bg="#c0392b")
def on_logout_leave(e):
    logout_btn.config(bg="#e74c3c")

logout_btn = tk.Button(main_app, text="Logout", bg="#e74c3c", fg="white", font=("Arial", 16, "bold"), bd=0, cursor="hand2", command=logout)
logout_btn.place(x=screen_width-90, y=70)
logout_btn.bind("<Enter>", on_logout_enter)
logout_btn.bind("<Leave>", on_logout_leave)

# ================= Sidebar (Navigation) ==================
sidebar_frame = tk.Frame(main_app, bg="#2ecc71", width=260)
sidebar_frame.place(x=0, y=65, height=screen_height-65)

# Sidebar Title
sidebar_title = tk.Label(sidebar_frame, text="Navigation", bg="#27ae60", fg="white", font=("Arial", 18, "bold"))
sidebar_title.pack(pady=(20, 10), fill=tk.X)

# Example navigation button(s) for Sidebar
def dummy_nav():
    messagebox.showinfo("Navigation", "This feature is under development.")

nav_buttons = [("Dashboard", dummy_nav), ("Inventory", dummy_nav), ("Orders", dummy_nav), ("Reports", dummy_nav)]
for text, command in nav_buttons:
    btn = tk.Button(sidebar_frame, text=text, font=("Arial", 16), bg="#2ecc71", fg="white", bd=0, relief=tk.FLAT, cursor="hand2", command=command)
    btn.pack(pady=10, fill=tk.X, padx=20)
    # Hover effects for sidebar buttons
    btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#27ae60"))
    btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2ecc71"))

# ================= Main Content Area ==================
content_frame = tk.Frame(main_app, bg="#f7fafc")
content_frame.place(x=270, y=80, width=screen_width-280, height=screen_height-90)
content_frame.lower()

# ---------------- Input Section ----------------
input_frame = tk.LabelFrame(content_frame, text="Item Details", padx=25, pady=25, bg="#f7fafc", font=("Arial", 16, "bold"), fg="#34495e", bd=2, relief=tk.GROOVE)
input_frame.pack(fill=tk.X, padx=30, pady=20)
input_frame.lower()

# Arrange Input Labels and Entries using grid layout
labels = ["Item Name", "Category", "Quantity", "Price", "Supplier", "Search"]
entries = {}

for idx, label in enumerate(labels):
    tk.Label(input_frame, text=label, font=("Arial", 14), bg="#f7fafc", fg="#34495e").grid(row=idx, column=0, sticky="w", padx=10, pady=8)
    if label == "Category":
        combo = ttk.Combobox(input_frame, values=["Electronics", "Clothing", "Food", "Other"], state="readonly", font=("Arial", 14))
        combo.grid(row=idx, column=1, padx=10, pady=8, sticky="ew")
        combo.current(0)
        entries[label] = combo
    else:
        ent = tk.Entry(input_frame, font=("Arial", 14))
        ent.grid(row=idx, column=1, padx=10, pady=8, sticky="ew")
        entries[label] = ent

input_frame.grid_columnconfigure(1, weight=1)

# ---------------- Button Panel ----------------
button_frame = tk.Frame(content_frame, bg="#f7fafc")
button_frame.pack(pady=15)

btn_config = {"font": ("Arial", 16), "padx": 20, "pady": 12, "fg": "white", "bd": 0, "cursor": "hand2"}

add_item_btn = tk.Button(button_frame, text="Add Item", command=add_new_inventory_item, bg="#1abc9c", **btn_config)
add_item_btn.grid(row=0, column=0, padx=15)

delete_item_btn = tk.Button(button_frame, text="Delete Item", command=remove_inventory_item, bg="#e74c3c", **btn_config)
delete_item_btn.grid(row=0, column=1, padx=15)

stats_btn = tk.Button(button_frame, text="Show Stats", command=display_inventory_statistics, bg="#3498db", **btn_config)
stats_btn.grid(row=0, column=2, padx=15)

low_stock_btn = tk.Button(button_frame, text="Low Stock Alert", command=check_for_low_stock, bg="#f39c12", **btn_config)
low_stock_btn.grid(row=0, column=3, padx=15)

search_btn = tk.Button(button_frame, text="Search", command=search_inventory_items, bg="#9b59b6", **btn_config)
search_btn.grid(row=1, column=0, columnspan=4, pady=15)

# ---------------- Inventory Table ----------------
table_frame = tk.Frame(content_frame, bg="white", bd=2, relief=tk.RIDGE)
table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

# Ttk Treeview styling for a modern look
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=35,
                fieldbackground="white",
                font=("Arial", 14))
style.configure("Treeview.Heading",
                background="#3498db",
                foreground="white",
                font=("Arial", 15, "bold"))
style.map("Treeview", background=[("selected", "#d1ecf1")])

columns = ("SN", "Item", "Category", "Quantity", "Cost", "Supplier", "Date Added")
inventory_table = ttk.Treeview(table_frame, columns=columns, show="headings")
inventory_table.pack(fill=tk.BOTH, expand=True)

for col in columns:
    inventory_table.heading(col, text=col)
    inventory_table.column(col, width=150, anchor="center")

# Load initial inventory data
refresh_inventory_list()

main_app.mainloop()