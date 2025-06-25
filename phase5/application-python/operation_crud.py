from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from db_config import get_connection

def open_operation_crud():
    win = Toplevel()
    win.title("Operation Management System")
    win.geometry("1150x700")
    win.configure(bg="#e8f5e9")

    # לאפשר תצוגה מתרחבת בעמודות ובשורות
    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=1)

    label_bg = "#e8f5e9"
    button_bg = "#33691e"
    button_fg = "white"

    labels = [
        "Operation ID:", "Operation Name:", "Objective:", "Location:",
        "Start Date (YYYY-MM-DD):", "End Date (YYYY-MM-DD):",
        "Commander ID:", "Role Type:"
    ]
    entries = []

    input_frame = Frame(win, bg=label_bg)
    input_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nw")

    for i, text in enumerate(labels):
        Label(input_frame, text=text, bg=label_bg, anchor="w", width=25, font=("Arial", 11, "bold")) \
            .grid(row=i, column=0, padx=5, pady=5, sticky=W)
        entry = Entry(input_frame, width=30, font=("Arial", 11))
        entry.grid(row=i, column=1, padx=5, pady=5, sticky=W)
        entries.append(entry)

    entries[7].insert(0, "commander")

    # Frame לטבלה וסרגלים - תופס את כל המקום הזמין
    tree_frame = Frame(win)
    tree_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

    # מאפשר ל- tree_frame להתרחב
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    columns = ("OperationID", "Name", "Objective", "Location", "Start", "End", "CommanderID", "Role")

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

    # סרגל גלילה אופקי ואנכי
    y_scrollbar = Scrollbar(tree_frame, orient=VERTICAL)
    y_scrollbar.grid(row=0, column=1, sticky='ns')

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
        tree.column(col, width=200, anchor=CENTER)

    tree.tag_configure('oddrow', background='#f1f8e9')
    tree.tag_configure('evenrow', background='#dcedc8')

    # פונקציות עזר ותפעול נותרו כפי שהיו (לשמור על הקוד שלך)

    def clear_fields():
        for e in entries:
            e.delete(0, END)
        entries[7].insert(0, "commander")

    def validate_inputs(allow_partial=False):
        try:
            operation_id = entries[0].get().strip()
            if not operation_id.isdigit():
                raise ValueError("Operation ID must be an integer.")

            required_indexes = [1, 4, 5, 6, 7] if not allow_partial else []
            for i in required_indexes:
                if not entries[i].get().strip():
                    raise ValueError(f"The field '{labels[i]}' cannot be empty.")

            start_str = entries[4].get().strip()
            end_str = entries[5].get().strip()
            if start_str and end_str:
                start = datetime.strptime(start_str, "%Y-%m-%d")
                end = datetime.strptime(end_str, "%Y-%m-%d")
                if end < start:
                    raise ValueError("End date cannot be earlier than start date.")

            return True
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
            return False
        except Exception:
            messagebox.showerror("Date Error", "Dates must be in YYYY-MM-DD format.")
            return False

    def show_operations():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT OperationID, OperationName, Objective, Location, startDate, endDate, ID, role_type
                FROM Operation
                ORDER BY OperationID DESC
            """)
            result = cur.fetchall()

            for item in tree.get_children():
                tree.delete(item)

            for i, row in enumerate(result):
                row_data = [row[0], row[1] or "---", row[2] or "---", row[3] or "---",
                            row[4], row[5], row[6], row[7]]
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=row_data, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def insert_operation():
        if not validate_inputs(): return
        try:
            values = [e.get().strip() or None for e in entries]
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Operation (OperationID, OperationName, Objective, Location, startDate, endDate, ID, role_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, values)
            conn.commit()
            messagebox.showinfo("Success", "Operation added successfully.")
            clear_fields()
            show_operations()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def update_operation():
        if not entries[0].get().strip().isdigit():
            messagebox.showerror("Error", "Please enter a valid Operation ID to update.")
            return
        if not validate_inputs(allow_partial=True): return
        try:
            fields, values = [], []
            field_names = ["OperationName", "Objective", "Location", "startDate", "endDate", "ID", "role_type"]
            for i in range(1, 8):
                value = entries[i].get().strip()
                if value:
                    fields.append(f"{field_names[i-1]} = %s")
                    values.append(value)
            if not fields:
                messagebox.showwarning("No Changes", "No fields were filled to update.")
                return

            values.append(entries[0].get())
            query = f"UPDATE Operation SET {', '.join(fields)} WHERE OperationID = %s"
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query, values)
            if cur.rowcount == 0:
                raise Exception("No operation found with this ID.")
            conn.commit()
            messagebox.showinfo("Success", "Operation updated successfully.")
            clear_fields()
            show_operations()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def delete_operation():
        operation_id = entries[0].get().strip()  # מפתח ראשי
        if not operation_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid Operation ID to delete.")
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM Operation WHERE OperationID = %s", (operation_id,))
            if cur.rowcount == 0:
                raise Exception("No operation found with this ID.")
            conn.commit()
            messagebox.showinfo("Success", "Operation deleted successfully.")
            clear_fields()
            show_operations()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    # לחצנים
    Button(input_frame, text="📋 Show All Operations", command=show_operations, bg=button_bg, fg=button_fg, width=25) \
        .grid(row=8, column=0, pady=10)
    Button(input_frame, text="➕ Insert", command=insert_operation, bg="#2e7d32", fg="white", width=25) \
        .grid(row=8, column=1)
    Button(input_frame, text="✏️ Update", command=update_operation, bg="#f9a825", fg="black", width=25) \
        .grid(row=9, column=0)
    Button(input_frame, text="🗑️ Delete", command=delete_operation, bg="#c62828", fg="white", width=25) \
        .grid(row=9, column=1)


