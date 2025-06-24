from tkinter import *
from tkinter import messagebox
from datetime import datetime
from db_config import get_connection  # ודא שזה קיים ומוגדר נכון

def open_operation_crud():
    win = Toplevel()
    win.title("ניהול מבצעים")
    win.geometry("850x600")
    win.configure(bg="#f0fff0")

    # תוויות
    labels = [
        "מזהה מבצע (Operation ID):",
        "שם המבצע (Operation Name):",
        "מטרה (Objective):",
        "מיקום (Location):",
        "תאריך התחלה (YYYY-MM-DD):",
        "תאריך סיום (YYYY-MM-DD):",
        "מזהה מפקד (Commander ID):",
        "סוג תפקיד (Role Type):"
    ]

    entries = []

    for i, text in enumerate(labels):
        Label(win, text=text, bg="#f0fff0", anchor="e", width=30).grid(row=i, column=0, padx=10, pady=5, sticky=E)
        entry = Entry(win, width=30)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)

    entries[7].insert(0, "commander")

    # תצוגת פלט עם גלילה
    frame = Frame(win)
    frame.grid(row=0, column=2, rowspan=12, padx=10, pady=10, sticky="nsew")

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    output = Text(frame, width=60, height=30, font=("Arial", 12), yscrollcommand=scrollbar.set)
    output.pack(side=LEFT, fill=BOTH)

    scrollbar.config(command=output.yview)

    # ניקוי שדות
    def clear_fields():
        for e in entries:
            e.delete(0, END)
        entries[7].insert(0, "commander")

    # בדיקת תקינות קלטים
    def validate_inputs():
        try:
            if not entries[0].get().isdigit():
                raise ValueError("מזהה מבצע חייב להיות מספר שלם.")

            for i, e in enumerate(entries):
                if not e.get().strip():
                    raise ValueError(f"שדה '{labels[i]}' לא יכול להיות ריק.")

            start = datetime.strptime(entries[4].get(), "%Y-%m-%d")
            end = datetime.strptime(entries[5].get(), "%Y-%m-%d")

            if end < start:
                raise ValueError("תאריך סיום לא יכול להיות מוקדם מתאריך התחלה.")

            return True

        except ValueError as ve:
            messagebox.showerror("שגיאת קלט", str(ve))
            return False

        except Exception:
            messagebox.showerror("שגיאת תאריך", "יש להזין תאריכים בפורמט YYYY-MM-DD.")
            return False

    # הצגת המבצעים
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
            output.delete(1.0, END)
            output.insert(END, "\U0001F4CB רשימת מבצעים:\n")
            output.insert(END, "=" * 70 + "\n")

            for row in result:
                output.insert(END, f"מזהה: {row[0]} | שם: {row[1]} | מטרה: {row[2]}\n")
                output.insert(END, f"מיקום: {row[3]} | התחלה: {row[4]} | סיום: {row[5]}\n")
                output.insert(END, f"מפקד: {row[6]} | תפקיד: {row[7]}\n")
                output.insert(END, "-" * 70 + "\n")

        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    # הוספת מבצע
    def insert_operation():
        if not validate_inputs():
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Operation (OperationID, OperationName, Objective, Location, startDate, endDate, ID, role_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(e.get() for e in entries))
            conn.commit()
            messagebox.showinfo("הצלחה", "מבצע נוסף בהצלחה.")
            clear_fields()
            show_operations()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    # עדכון מבצע
    def update_operation():
        if not validate_inputs():
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE Operation
                SET OperationName=%s, Objective=%s, Location=%s, startDate=%s, endDate=%s, ID=%s, role_type=%s
                WHERE OperationID=%s
            """, (
                entries[1].get(), entries[2].get(), entries[3].get(),
                entries[4].get(), entries[5].get(), entries[6].get(), entries[7].get(), entries[0].get()
            ))
            if cur.rowcount == 0:
                raise Exception("לא נמצא מבצע עם מזהה זה.")
            conn.commit()
            messagebox.showinfo("הצלחה", "מבצע עודכן בהצלחה.")
            clear_fields()
            show_operations()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    # מחיקת מבצע
    def delete_operation():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM Operation WHERE OperationID = %s", (entries[0].get(),))
            if cur.rowcount == 0:
                raise Exception("לא נמצא מבצע למחיקה עם מזהה זה.")
            conn.commit()
            messagebox.showinfo("הצלחה", "מבצע נמחק.")
            clear_fields()
            show_operations()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

    # כפתורים
    Button(win, text="הצג את כל המבצעים", command=show_operations, bg="#004d00", fg="white", width=25) \
        .grid(row=8, column=0, pady=10)
    Button(win, text="הוספה", command=insert_operation, bg="#006699", fg="white", width=25) \
        .grid(row=8, column=1)
    Button(win, text="עדכון", command=update_operation, bg="#cc9900", fg="black", width=25) \
        .grid(row=9, column=0)
    Button(win, text="מחיקה", command=delete_operation, bg="#990000", fg="white", width=25) \
        .grid(row=9, column=1)
