from tkinter import *
from tkinter import messagebox
from db_config import get_connection

def open_requires_crud():
    win = Toplevel()
    win.title("ניהול דרישות ציוד למבצע")
    win.geometry("850x500")
    win.configure(bg="#fff8f0")

    Label(win, text="מזהה ציוד (EquipmentID):", bg="#fff8f0").grid(row=0, column=0, padx=10, pady=5, sticky=E)
    Label(win, text="מזהה מבצע (OperationID):", bg="#fff8f0").grid(row=1, column=0, padx=10, pady=5, sticky=E)
    Label(win, text="כמות נדרשת (RequiredQuantity):", bg="#fff8f0").grid(row=2, column=0, padx=10, pady=5, sticky=E)
    Label(win, text="סוג ציוד (equipment_type):", bg="#fff8f0").grid(row=3, column=0, padx=10, pady=5, sticky=E)

    equip_id_entry = Entry(win, width=30)
    op_id_entry = Entry(win, width=30)
    quantity_entry = Entry(win, width=30)
    type_entry = Entry(win, width=30)
    type_entry.insert(0, "operational")

    equip_id_entry.grid(row=0, column=1)
    op_id_entry.grid(row=1, column=1)
    quantity_entry.grid(row=2, column=1)
    type_entry.grid(row=3, column=1)

    # תיבת תצוגה נגללת
    frame = Frame(win)
    frame.grid(row=0, column=2, rowspan=10, padx=10, pady=10, sticky="nsew")

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    output = Text(frame, width=60, height=25, font=("Arial", 12), yscrollcommand=scrollbar.set)
    output.pack(side=LEFT, fill=BOTH)

    scrollbar.config(command=output.yview)

    def clear_fields():
        equip_id_entry.delete(0, END)
        op_id_entry.delete(0, END)
        quantity_entry.delete(0, END)
        type_entry.delete(0, END)
        type_entry.insert(0, "operational")

    def validate_inputs():
        try:
            if not equip_id_entry.get().isdigit():
                raise ValueError("מזהה ציוד חייב להיות מספר שלם.")

            if not op_id_entry.get().isdigit():
                raise ValueError("מזהה מבצע חייב להיות מספר שלם.")

            if not quantity_entry.get().isdigit() or int(quantity_entry.get()) <= 0:
                raise ValueError("כמות נדרשת חייבת להיות מספר שלם חיובי.")

            if type_entry.get().strip().lower() not in ['medical', 'operational']:
                raise ValueError("סוג הציוד חייב להיות medical או operational.")

            return True

        except ValueError as ve:
            messagebox.showerror("שגיאת קלט", str(ve))
            return False

    def show_requires():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM Requires ORDER BY OperationID DESC
            """)
            rows = cur.fetchall()
            output.delete(1.0, END)
            output.insert(END, "📋 דרישות ציוד לפי מבצעים:\n")
            output.insert(END, "=" * 90 + "\n")
            for row in rows:
                output.insert(END, f"מבצע: {row[1]} | ציוד: {row[0]} | סוג: {row[3]} | כמות: {row[2]}\n")
                output.insert(END, "-" * 90 + "\n")
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def insert_requires():
        if not validate_inputs():
            return
        try:
            equipment_id = int(equip_id_entry.get())
            operation_id = int(op_id_entry.get())
            required_quantity = int(quantity_entry.get())
            equipment_type = type_entry.get().strip().lower()

            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT 1 FROM Requires WHERE EquipmentID=%s AND OperationID=%s AND equipment_type=%s
            """, (equipment_id, operation_id, equipment_type))
            if cur.fetchone():
                messagebox.showwarning("שגיאה", "דרישה זו כבר קיימת במערכת.")
                return

            cur.execute("""
                INSERT INTO Requires (EquipmentID, OperationID, RequiredQuantity, equipment_type)
                VALUES (%s, %s, %s, %s)
            """, (equipment_id, operation_id, required_quantity, equipment_type))

            conn.commit()
            messagebox.showinfo("הצלחה", "הדרישה נוספה בהצלחה.")
            clear_fields()
            show_requires()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def update_requires():
        if not validate_inputs():
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE Requires
                SET RequiredQuantity = %s
                WHERE EquipmentID = %s AND OperationID = %s AND equipment_type = %s
            """, (
                quantity_entry.get(), equip_id_entry.get(),
                op_id_entry.get(), type_entry.get().strip().lower()
            ))
            if cur.rowcount == 0:
                messagebox.showwarning("עדכון נכשל", "לא נמצאה דרישה לעדכון.")
            else:
                conn.commit()
                messagebox.showinfo("הצלחה", "הדרישה עודכנה בהצלחה.")
                clear_fields()
                show_requires()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
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
            """, (
                equip_id_entry.get(), op_id_entry.get(), type_entry.get().strip().lower()
            ))
            if cur.rowcount == 0:
                messagebox.showwarning("שגיאה", "לא נמצאה דרישה למחיקה.")
            else:
                conn.commit()
                messagebox.showinfo("הצלחה", "הדרישה נמחקה.")
                clear_fields()
                show_requires()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    # כפתורים
    Button(win, text="הצג דרישות", command=show_requires, bg="#004d00", fg="white", width=25).grid(row=4, column=0, pady=10)
    Button(win, text="הוספה", command=insert_requires, bg="#006699", fg="white", width=25).grid(row=4, column=1)
    Button(win, text="עדכון", command=update_requires, bg="#cc9900", fg="black", width=25).grid(row=5, column=0)
    Button(win, text="מחיקה", command=delete_requires, bg="#990000", fg="white", width=25).grid(row=5, column=1)
