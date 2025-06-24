from tkinter import *
from tkinter import messagebox
from db_config import get_connection

def open_equipment_crud():
    win = Toplevel()
    win.title("ניהול ציוד")
    win.geometry("850x500")
    win.configure(bg="#fff0f5")

    Label(win, text="Equipment ID:", bg="#fff0f5").grid(row=0, column=0, padx=10, pady=5, sticky=E)
    Label(win, text="Equipment Name:", bg="#fff0f5").grid(row=1, column=0, padx=10, pady=5, sticky=E)
    Label(win, text="Quantity:", bg="#fff0f5").grid(row=2, column=0, padx=10, pady=5, sticky=E)
    Label(win, text="Type (medical/operational):", bg="#fff0f5").grid(row=3, column=0, padx=10, pady=5, sticky=E)

    id_entry = Entry(win, width=30)
    name_entry = Entry(win, width=30)
    qty_entry = Entry(win, width=30)
    type_entry = Entry(win, width=30)

    id_entry.grid(row=0, column=1)
    name_entry.grid(row=1, column=1)
    qty_entry.grid(row=2, column=1)
    type_entry.grid(row=3, column=1)

    # תצוגה נגללת לציוד
    frame = Frame(win)
    frame.grid(row=0, column=2, rowspan=12, padx=10, pady=10, sticky="nsew")

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    output = Text(frame, width=60, height=25, font=("Arial", 12), yscrollcommand=scrollbar.set)
    output.pack(side=LEFT, fill=BOTH)

    scrollbar.config(command=output.yview)

    def clear_fields():
        id_entry.delete(0, END)
        name_entry.delete(0, END)
        qty_entry.delete(0, END)
        type_entry.delete(0, END)

    def validate_inputs():
        try:
            # מזהה ציוד מספרי
            if not id_entry.get().isdigit():
                raise ValueError("מזהה הציוד חייב להיות מספר שלם.")

            if not name_entry.get().strip():
                raise ValueError("שם הציוד לא יכול להיות ריק.")

            if not qty_entry.get().isdigit() or int(qty_entry.get()) <= 0:
                raise ValueError("הכמות חייבת להיות מספר שלם חיובי.")

            if type_entry.get().lower() not in ["medical", "operational"]:
                raise ValueError("סוג הציוד חייב להיות medical או operational.")

            return True

        except ValueError as ve:
            messagebox.showerror("שגיאת קלט", str(ve))
            return False

    def show_equipment():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM equipment ORDER BY equipment_id DESC")
            result = cur.fetchall()
            output.delete(1.0, END)
            output.insert(END, "📦 רשימת ציוד:\n")
            output.insert(END, "=" * 70 + "\n")

            for row in result:
                output.insert(END, f"מזהה: {row[0]} | שם: {row[1]}\n")
                output.insert(END, f"כמות: {row[2]} | סוג: {row[3]}\n")
                output.insert(END, "-" * 70 + "\n")

        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def insert_equipment():
        if not validate_inputs():
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            equipment_id = id_entry.get()
            equipment_type = type_entry.get().lower()

            cur.execute("SELECT 1 FROM equipment WHERE equipment_id = %s AND equipment_type = %s",
                        (equipment_id, equipment_type))
            if cur.fetchone():
                messagebox.showwarning("שימו לב", "הציוד הזה כבר קיים במערכת!")
                return

            cur.execute("""
                INSERT INTO equipment (equipment_id, equipment_name, quantity, equipment_type)
                VALUES (%s, %s, %s, %s)
            """, (
                equipment_id,
                name_entry.get(),
                qty_entry.get(),
                equipment_type
            ))
            conn.commit()
            messagebox.showinfo("הצלחה", "הציוד נוסף בהצלחה.")
            clear_fields()
            show_equipment()

        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def update_equipment():
        if not validate_inputs():
            return
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT 1 FROM equipment WHERE equipment_id = %s AND equipment_type = %s",
                        (id_entry.get(), type_entry.get().lower()))
            if not cur.fetchone():
                messagebox.showwarning("לא נמצא", "הציוד לא קיים – לא ניתן לעדכן.")
                return

            cur.execute("""
                UPDATE equipment
                SET equipment_name = %s, quantity = %s
                WHERE equipment_id = %s AND equipment_type = %s
            """, (
                name_entry.get(), qty_entry.get(),
                id_entry.get(), type_entry.get().lower()
            ))
            conn.commit()
            messagebox.showinfo("הצלחה", "הציוד עודכן בהצלחה.")
            clear_fields()
            show_equipment()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    def delete_equipment():
        try:
            conn = get_connection()
            cur = conn.cursor()
            equipment_id = id_entry.get()
            equipment_type = type_entry.get().lower()

            cur.execute("SELECT 1 FROM equipment WHERE equipment_id = %s AND equipment_type = %s",
                        (equipment_id, equipment_type))
            if not cur.fetchone():
                messagebox.showwarning("שגיאה", "הציוד לא קיים במערכת – לא ניתן למחוק.")
                return

            cur.execute("DELETE FROM equipment WHERE equipment_id = %s AND equipment_type = %s",
                        (equipment_id, equipment_type))
            conn.commit()
            messagebox.showinfo("הצלחה", "הציוד נמחק בהצלחה.")
            clear_fields()
            show_equipment()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    # כפתורים
    Button(win, text="הצג ציוד", command=show_equipment, bg="#008080", fg="white", width=25).grid(row=4, column=0, pady=10)
    Button(win, text="הוספה", command=insert_equipment, bg="#006699", fg="white", width=25).grid(row=4, column=1)
    Button(win, text="עדכון", command=update_equipment, bg="#cc9900", fg="black", width=25).grid(row=5, column=0)
    Button(win, text="מחיקה", command=delete_equipment, bg="#990000", fg="white", width=25).grid(row=5, column=1)
