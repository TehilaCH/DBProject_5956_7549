from tkinter import *
from tkinter import messagebox, ttk
from db_config import get_connection

def open_requires_crud():
    win = Toplevel()
    win.title("Requires Management")
    win.geometry("1150x700")
    win.configure(bg="#e8f5e9")

    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=1)

    label_bg = "#e8f5e9"
    button_bg = "#33691e"
    button_fg = "white"

    input_frame = Frame(win, bg=label_bg)
    input_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nw")

    labels = ["Equipment ID:", "Operation ID:", "Required Quantity:", "Equipment Type:"]
    equip_id_cb = ttk.Combobox(input_frame, width=28, font=("Arial", 11))
    op_id_cb = ttk.Combobox(input_frame, width=28, font=("Arial", 11))
    quantity_entry = Entry(input_frame, width=30, font=("Arial", 11))
    type_cb = ttk.Combobox(input_frame, values=["medical", "operational"], width=28, font=("Arial", 11))
    type_cb.set("operational")
    widgets = [equip_id_cb, op_id_cb, quantity_entry, type_cb]

    for i, text in enumerate(labels):
        Label(input_frame, text=text, bg=label_bg, anchor="w", width=25, font=("Arial", 11, "bold")) \
            .grid(row=i, column=0, padx=5, pady=5, sticky=W)
        widgets[i].grid(row=i, column=1, padx=5, pady=5, sticky=W)

    # Tree Frame
    tree_frame = Frame(win)
    tree_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    columns = ("EquipmentID", "OperationID", "RequiredQuantity", "Type")

    style = ttk.Style()
    style.configure("Treeview", background="white", foreground="black", rowheight=25,
                    fieldbackground="white", font=("Arial", 10))
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#a5d6a7")
    style.map("Treeview", background=[("selected", "#aed581")])

    y_scrollbar = Scrollbar(tree_frame, orient=VERTICAL)
    y_scrollbar.grid(row=0, column=1, sticky='ns')
    x_scrollbar = Scrollbar(tree_frame, orient=HORIZONTAL)
    x_scrollbar.grid(row=1, column=0, sticky='ew')

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview",
                        yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
    tree.grid(row=0, column=0, sticky="nsew")

    y_scrollbar.config(command=tree.yview)
    x_scrollbar.config(command=tree.xview)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor=CENTER)

    tree.tag_configure('oddrow', background='#f1f8e9')
    tree.tag_configure('evenrow', background='#dcedc8')

    def populate_comboboxes():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT equipment_id FROM equipment")
            equip_ids = [str(row[0]) for row in cur.fetchall()]
            cur.execute("SELECT OperationID FROM Operation")
            op_ids = [str(row[0]) for row in cur.fetchall()]
            equip_id_cb["values"] = equip_ids
            op_id_cb["values"] = op_ids
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def clear_fields():
        equip_id_cb.set("")
        op_id_cb.set("")
        quantity_entry.delete(0, END)
        type_cb.set("operational")

    def validate_inputs():
        try:
            if not equip_id_cb.get().isdigit(): raise ValueError("Equipment ID must be an integer.")
            if not op_id_cb.get().isdigit(): raise ValueError("Operation ID must be an integer.")
            if not quantity_entry.get().isdigit() or int(quantity_entry.get()) <= 0:
                raise ValueError("Quantity must be a positive integer.")
            if type_cb.get().lower() not in ["medical", "operational"]:
                raise ValueError("Type must be 'medical' or 'operational'.")
            return True
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
            return False

    def show_requires():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM Requires ORDER BY OperationID DESC")
            rows = cur.fetchall()
            tree.delete(*tree.get_children())
            for i, row in enumerate(rows):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=row, tags=(tag,))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def insert_requires():
        if not validate_inputs(): return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM Requires WHERE EquipmentID=%s AND OperationID=%s AND equipment_type=%s",
                        (equip_id_cb.get(), op_id_cb.get(), type_cb.get()))
            if cur.fetchone():
                messagebox.showwarning("Duplicate", "This requirement already exists.")
                return
            cur.execute("""
                INSERT INTO Requires (EquipmentID, OperationID, RequiredQuantity, equipment_type)
                VALUES (%s, %s, %s, %s)
            """, (equip_id_cb.get(), op_id_cb.get(), quantity_entry.get(), type_cb.get()))
            conn.commit()
            messagebox.showinfo("Success", "Requirement added successfully.")
            clear_fields()
            show_requires()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def update_requires():
        if not validate_inputs(): return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE Requires
                SET RequiredQuantity = %s
                WHERE EquipmentID = %s AND OperationID = %s AND equipment_type = %s
            """, (quantity_entry.get(), equip_id_cb.get(), op_id_cb.get(), type_cb.get()))
            if cur.rowcount == 0:
                messagebox.showwarning("Update Failed", "Requirement not found.")
            else:
                conn.commit()
                messagebox.showinfo("Success", "Requirement updated successfully.")
                clear_fields()
                show_requires()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def delete_requires():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                DELETE FROM Requires
                WHERE EquipmentID = %s AND OperationID = %s AND equipment_type = %s
            """, (equip_id_cb.get(), op_id_cb.get(), type_cb.get()))
            if cur.rowcount == 0:
                messagebox.showwarning("Delete Failed", "Requirement not found.")
            else:
                conn.commit()
                messagebox.showinfo("Success", "Requirement deleted successfully.")
                clear_fields()
                show_requires()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    Button(input_frame, text="📋 Show Requirements", command=show_requires, bg=button_bg, fg=button_fg, width=25).grid(row=4, column=0, pady=10)
    Button(input_frame, text="➕ Insert", command=insert_requires, bg="#2e7d32", fg="white", width=25).grid(row=4, column=1)
    Button(input_frame, text="✏️ Update", command=update_requires, bg="#f9a825", fg="black", width=25).grid(row=5, column=0)
    Button(input_frame, text="🗑️ Delete", command=delete_requires, bg="#c62828", fg="white", width=25).grid(row=5, column=1)

    populate_comboboxes()
