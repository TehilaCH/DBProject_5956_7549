from tkinter import *
from tkinter import messagebox, ttk
from db_config import get_connection

def open_equipment_crud():
    win = Toplevel()
    win.title("Equipment Management")
    win.geometry("1150x700")
    win.configure(bg="#e8f5e9")

    # לאפשר תצוגה מתרחבת בעמודות ובשורות
    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=1)

    label_bg = "#e8f5e9"
    button_bg = "#33691e"
    button_fg = "white"

    labels = ["Equipment ID:", "Equipment Name:", "Quantity:", "Type (medical/operational):"]
    entries = []

    input_frame = Frame(win, bg=label_bg)
    input_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nw")

    for i, text in enumerate(labels):
        Label(input_frame, text=text, bg=label_bg, anchor="w", width=25, font=("Arial", 11, "bold")) \
            .grid(row=i, column=0, padx=5, pady=5, sticky=W)
        entry = Entry(input_frame, width=30, font=("Arial", 11))
        entry.grid(row=i, column=1, padx=5, pady=5, sticky=W)
        entries.append(entry)

    # Frame לטבלה וסרגלים - תופס את כל המקום הזמין
    tree_frame = Frame(win)
    tree_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

    # מאפשר ל- tree_frame להתרחב
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    columns = ("EquipmentID", "Name", "Quantity", "Type")

    style = ttk.Style()
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="white",
                    borderwidth=1,
                    relief="solid",
                    font=("Arial", 10))
    style.configure("Treeview.Heading",
                    font=("Arial", 11, "bold"),
                    background="#a5d6a7",
                    relief="raised")
    style.map('Treeview', background=[('selected', '#aed581')])

    # סרגל גלילה אנכי בצד ימין
    y_scrollbar = Scrollbar(tree_frame, orient=VERTICAL)
    y_scrollbar.grid(row=0, column=1, sticky='ns')

    # סרגל גלילה אופקי בתחתית, עם קוביית גלילה מימין ל-Treeview אבל כדי שייראה בצד שמאל - נוסיף padding
    x_scrollbar = Scrollbar(tree_frame, orient=HORIZONTAL)
    x_scrollbar.grid(row=1, column=0, sticky='ew')

    tree = ttk.Treeview(tree_frame,
                        columns=columns,
                        show='headings',
                        style="Treeview",
                        yscrollcommand=y_scrollbar.set,
                        xscrollcommand=x_scrollbar.set)

    tree.grid(row=0, column=0, sticky='nsew')

    y_scrollbar.config(command=tree.yview)
    x_scrollbar.config(command=tree.xview)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=250, anchor=CENTER)

    tree.tag_configure('oddrow', background='#f1f8e9')
    tree.tag_configure('evenrow', background='#dcedc8')

    def clear_fields():
        for e in entries:
            e.delete(0, END)

    def validate_inputs(allow_partial=False):
        try:
            if not entries[0].get().strip().isdigit():
                raise ValueError("Equipment ID must be an integer.")
            if not allow_partial:
                for i in range(1, 4):
                    if not entries[i].get().strip():
                        raise ValueError(f"The field '{labels[i]}' cannot be empty.")
            if entries[2].get() and (not entries[2].get().isdigit() or int(entries[2].get()) <= 0):
                raise ValueError("Quantity must be a positive integer.")
            if entries[3].get() and entries[3].get().lower() not in ["medical", "operational"]:
                raise ValueError("Type must be either 'medical' or 'operational'.")
            return True
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
            return False

    def show_equipment():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT equipment_id, equipment_name, quantity, equipment_type FROM equipment ORDER BY equipment_id DESC")
            result = cur.fetchall()

            tree.delete(*tree.get_children())
            for i, row in enumerate(result):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=row, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def insert_equipment():
        if not validate_inputs(): return
        try:
            values = [e.get().strip() for e in entries]
            values[3] = values[3].lower()
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM equipment WHERE equipment_id = %s AND equipment_type = %s", (values[0], values[3]))
            if cur.fetchone():
                messagebox.showwarning("Notice", "This equipment already exists.")
                return
            cur.execute("""
                INSERT INTO equipment (equipment_id, equipment_name, quantity, equipment_type)
                VALUES (%s, %s, %s, %s)
            """, values)
            conn.commit()
            messagebox.showinfo("Success", "Equipment added successfully.")
            clear_fields()
            show_equipment()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def update_equipment():
        if not entries[0].get().strip().isdigit():
            messagebox.showerror("Error", "Please enter a valid Equipment ID.")
            return
        if not validate_inputs(allow_partial=True): return
        try:
            fields, values = [], []
            field_names = ["equipment_name", "quantity", "equipment_type"]
            for i in range(1, 4):
                val = entries[i].get().strip()
                if val:
                    fields.append(f"{field_names[i-1]} = %s")
                    values.append(val.lower() if i == 3 else val)
            if not fields:
                messagebox.showwarning("No Changes", "No fields to update.")
                return
            values.append(entries[0].get())
            query = f"UPDATE equipment SET {', '.join(fields)} WHERE equipment_id = %s"
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query, values)
            if cur.rowcount == 0:
                raise Exception("No equipment found with this ID.")
            conn.commit()
            messagebox.showinfo("Success", "Equipment updated successfully.")
            clear_fields()
            show_equipment()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def delete_equipment():
        eid = entries[0].get().strip()
        if not eid.isdigit():
            messagebox.showerror("Error", "Please enter a valid Equipment ID.")
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM equipment WHERE equipment_id = %s", (eid,))
            if cur.rowcount == 0:
                raise Exception("No equipment found with this ID.")
            conn.commit()
            messagebox.showinfo("Success", "Equipment deleted successfully.")
            clear_fields()
            show_equipment()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    # לחצנים
    Button(input_frame, text="📋 Show All Equipment", command=show_equipment, bg=button_bg, fg=button_fg, width=25) \
        .grid(row=4, column=0, pady=10)
    Button(input_frame, text="➕ Insert", command=insert_equipment, bg="#2e7d32", fg="white", width=25) \
        .grid(row=4, column=1)
    Button(input_frame, text="✏️ Update", command=update_equipment, bg="#f9a825", fg="black", width=25) \
        .grid(row=5, column=0)
    Button(input_frame, text="🗑️ Delete", command=delete_equipment, bg="#c62828", fg="white", width=25) \
        .grid(row=5, column=1)
