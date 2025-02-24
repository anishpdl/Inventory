import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import runpy
from PIL import ImageTk,Image
from tkinter.scrolledtext import ScrolledText
import config

db_path = "inventory_data.db"

def fetch_data(query, params=()):
    """Fetch data from the database based on the given query and parameters."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def get_stock_report():
    """Retrieve current stock levels."""
    items = fetch_data("SELECT item_name, stock_quantity FROM inventory_items WHERE user = ?",(config.logged_user,))
    return "\n".join([f"{item[0]}: {item[1]} units available" for item in items])

def get_purchase_report():
    """Retrieve recent purchase details."""
    purchases = fetch_data("SELECT item_id, new_value, change_time FROM inventory_changes WHERE action_type = 'add' AND \"user\" = ?", (config.logged_user,))
    return "\n".join([f"Item {p[0]}: {p[1]} units added on {p[2]}" for p in purchases])

def get_date_based_report(period='monthly'):
    """Retrieve inventory changes based on the selected period."""
    date_filters = {
        'daily': "DATE('now')",
        'weekly': "DATE('now', '-7 days')",
        'monthly': "DATE('now', '-1 month')",
        'yearly': "DATE('now', '-1 year')"
    }
    date_filter = date_filters.get(period, "DATE('now')")
    data = fetch_data(f"SELECT item_name, stock_quantity, date_added FROM inventory_items WHERE date_added >= {date_filter} AND user = ?",(config.logged_user,))
    return "\n".join([f"{d[0]}: {d[1]} units added on {d[2]}" for d in data])

def generate_stock_chart(frame):
    """Create and display a stock distribution bar chart."""
    items = fetch_data("SELECT item_name, stock_quantity FROM inventory_items WHERE user = ?",(config.logged_user,))
    item_names = [item[0] for item in items]
    quantities = [item[1] for item in items]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(item_names, quantities, color='#3498db')
    ax.set_title('Stock Distribution', fontsize=14, fontweight='bold', color='#34495E')
    ax.set_xlabel('Items', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.set_ylabel('Stock Quantity', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.tick_params(axis='x', rotation=45)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def update_reports():
    """Update the displayed reports."""
    stock_area.delete("1.0", tk.END)
    stock_area.insert(tk.END, get_stock_report())
    
    purchase_area.delete("1.0", tk.END)
    purchase_area.insert(tk.END, get_purchase_report())
    
    monthly_area.delete("1.0", tk.END)
    monthly_area.insert(tk.END, get_date_based_report('monthly'))

def create_dashboard():
    """Set up and display the inventory dashboard."""
    global stock_area, purchase_area, monthly_area
    root = tk.Tk()
    root.title("Inventory Dashboard")
    root.geometry("1920x1080")
    root.overrideredirect(False)
    root.attributes("-fullscreen", True)
    root.configure(bg="#f4f6f7")

        
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # ================= Header Section ==================
    header_frame = tk.Frame(root, bg="#34495e", height=65)
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
    buttonFont = tk.font.Font(size=18, weight="bold")

    def minimize_app():
        root.iconify()

    def close_app():
        if tk.messagebox.askquestion('Exit Application', 'Are you sure you want to close the application?', icon='warning') == 'yes':
            root.destroy()

    min_btn = tk.Button(header_frame, text="-", command=minimize_app, bg="#34495e", fg="white", bd=0, font=buttonFont,
                        activebackground="#2c3e50", activeforeground="white", cursor="hand2")
    min_btn.pack(side=tk.RIGHT, padx=10, pady=10)

    close_btn = tk.Button(header_frame, text="✕", command=close_app, bg="#34495e", fg="white", bd=0, font=buttonFont,
                        activebackground="#e74c3c", activeforeground="white", cursor="hand2")
    close_btn.pack(side=tk.RIGHT, padx=10, pady=10)

    
    # Main Frame
    main_frame = tk.Frame(root, bg="#ffffff", relief="raised", borderwidth=3)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Title
    title_label = ttk.Label(main_frame, text="📊 Reports Dashboard", font=("Arial", 20, "bold"), background="#ffffff", foreground="#2C3E50")
    title_label.pack(pady=10)
    
    # Create a frame for the reports section
    reports_frame = tk.Frame(main_frame, bg="#ffffff")
    reports_frame.pack(fill=tk.X, padx=20, pady=5)
    
    # Stock Report Section
    stock_frame = tk.LabelFrame(reports_frame, text="📦 Stock Report", font=("Arial", 14, "bold"),
                                bg="#ECF0F1", fg="#2980B9", padx=10, pady=10, relief="groove", borderwidth=2)
    stock_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
    stock_area = ScrolledText(stock_frame, wrap=tk.WORD, font=("Arial", 12), bg="#ffffff", relief="flat", height=10, width=40)
    stock_area.pack(fill=tk.BOTH, expand=True)
    
    # Purchase Report Section
    purchase_frame = tk.LabelFrame(reports_frame, text="🛒 Purchase Report", font=("Arial", 14, "bold"),
                                   bg="#ECF0F1", fg="#27AE60", padx=10, pady=10, relief="groove", borderwidth=2)
    purchase_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
    purchase_area = ScrolledText(purchase_frame, wrap=tk.WORD, font=("Arial", 12), bg="#ffffff", relief="flat", height=10, width=40)
    purchase_area.pack(fill=tk.BOTH, expand=True)
    
    # Monthly Report Section
    monthly_frame = tk.LabelFrame(reports_frame, text="📅 Monthly Report", font=("Arial", 14, "bold"),
                                  bg="#ECF0F1", fg="#8E44AD", padx=10, pady=10, relief="groove", borderwidth=2)
    monthly_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
    monthly_area = ScrolledText(monthly_frame, wrap=tk.WORD, font=("Arial", 12), bg="#ffffff", relief="flat", height=10, width=40)
    monthly_area.pack(fill=tk.BOTH, expand=True)
    
    # Chart Frame
    chart_frame = tk.Frame(main_frame, bg="#ffffff", relief="ridge", borderwidth=3)
    chart_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
    generate_stock_chart(chart_frame)
    
    # Refresh Button with hover effect
    def on_hover(e):
        refresh_button.config(background="#3498db", foreground="white")
    
    def on_leave(e):
        refresh_button.config(background="#ECF0F1", foreground="black")
    
    refresh_button = tk.Button(main_frame, text="🔄 Refresh Reports", command=update_reports, font=("Arial", 12, "bold"),
                               bg="#ECF0F1", fg="black", relief="raised", borderwidth=3, padx=10, pady=5)
    refresh_button.pack(pady=10)
    refresh_button.bind("<Enter>", on_hover)
    refresh_button.bind("<Leave>", on_leave)
    
    update_reports()
    root.mainloop()

if __name__ == "__main__":
    create_dashboard()