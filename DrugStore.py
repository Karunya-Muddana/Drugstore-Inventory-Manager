import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext

conn = sqlite3.connect('drugstore.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Drugs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL
    )
    ''')
conn.commit()
conn.close()

# Database functions
def add_drug(name, manufacturer, price, stock_quantity):
    conn = sqlite3.connect('drugstore.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Drugs (name, manufacturer, price, stock_quantity)
    VALUES (?, ?, ?, ?)
    ''', (name, manufacturer, price, stock_quantity))
    conn.commit()
    conn.close()

def delete_drug(drug_id):
    conn = sqlite3.connect('drugstore.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Drugs WHERE id = ?', (drug_id,))
    conn.commit()
    conn.close()

def fetch_all_drugs():
    conn = sqlite3.connect('drugstore.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Drugs")
    rows = cursor.fetchall()
    conn.close()
    return rows

# UI Functions
def on_submit_add(window, name_var, manufacturer_var, price_var, quantity_var):
    try:
        name = name_var.get()
        manufacturer = manufacturer_var.get()
        price = float(price_var.get())
        quantity = int(quantity_var.get())

        if not name or not manufacturer:
            messagebox.showerror("Error", "Name and Manufacturer cannot be empty.")
            return

        add_drug(name, manufacturer, price, quantity)
        messagebox.showinfo("Success", f"Added {name} to database.")

        name_var.set("")
        manufacturer_var.set("")
        price_var.set("")
        quantity_var.set("")
        window.destroy()

    except ValueError:
        messagebox.showerror("Error", "Price must be a number and Quantity must be an integer.")

def on_submit_remove(window, id_var):
    try:
        drug_id = int(id_var.get())
        delete_drug(drug_id)
        messagebox.showinfo("Success", f"Removed drug with ID {drug_id} from the database.")
        id_var.set("")
        window.destroy()
    except ValueError:
        messagebox.showerror("Error", "ID must be an integer.")

def open_add_window():
    add_win = tk.Toplevel()
    add_win.title("Add Drug")
    add_win.geometry("350x250")

    name_var = tk.StringVar()
    manufacturer_var = tk.StringVar()
    price_var = tk.StringVar()
    quantity_var = tk.StringVar()

    tk.Label(add_win, text="Drug Name").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(add_win, textvariable=name_var).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_win, text="Manufacturer").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(add_win, textvariable=manufacturer_var).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_win, text="Price").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(add_win, textvariable=price_var).grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_win, text="Stock Quantity").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(add_win, textvariable=quantity_var).grid(row=3, column=1, padx=10, pady=5)

    tk.Button(add_win, text="Submit", command=lambda: on_submit_add(add_win, name_var, manufacturer_var, price_var, quantity_var)).grid(row=4, column=0, columnspan=2, pady=10)

def open_remove_window():
    remove_win = tk.Toplevel()
    remove_win.title("Remove Drug")
    remove_win.geometry("350x100")

    id_var = tk.StringVar()

    tk.Label(remove_win, text="Drug ID to Remove").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(remove_win, textvariable=id_var).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(remove_win, text="Submit", command=lambda: on_submit_remove(remove_win, id_var)).grid(row=1, column=0, columnspan=2, pady=10)

def open_view_window():
    view_win = tk.Toplevel()
    view_win.title("View Drugs Database")
    view_win.geometry("600x400")

    # Add a ScrolledText widget (text area with scrollbar)
    text_area = scrolledtext.ScrolledText(view_win, width=70, height=20)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Fetch data and insert into text widget
    rows = fetch_all_drugs()
    if not rows:
        text_area.insert(tk.END, "No records found in the database.")
    else:
        header = f"{'ID':<5} {'Name':<20} {'Manufacturer':<20} {'Price':<10} {'Stock Qty':<10}\n"
        text_area.insert(tk.END, header)
        text_area.insert(tk.END, "-"*70 + "\n")
        for row in rows:
            # row = (id, name, manufacturer, price, stock_quantity)
            line = f"{row[0]:<5} {row[1]:<20} {row[2]:<20} {row[3]:<10.2f} {row[4]:<10}\n"
            text_area.insert(tk.END, line)

    text_area.configure(state='disabled')  # Make text read-only

# Main UI
def main_terminal():
    root = tk.Tk()
    root.title("Drugstore Inventory Manager")
    root.geometry("270x100")

    tk.Button(root, text="Add Entry", width=15, command=open_add_window).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(root, text="Remove Entry", width=15, command=open_remove_window).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="View Database", width=15, command=open_view_window).grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    
    main_terminal()
