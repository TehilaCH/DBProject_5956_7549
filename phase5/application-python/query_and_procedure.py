from tkinter import *
from tkinter import messagebox
from db_config import get_connection

def open_query_and_procedure():
    win = Toplevel()
    win.title("הפעלת שאילתות ופרוצדורות")
    win.geometry("800x600")
    win.configure(bg="#fff9e6")

    Label(win, text="שאילתות ופרוצדורות", font=("Arial", 16, "bold"), bg="#fff9e6").pack(pady=10)

    output_text = Text(win, height=20, width=90, wrap=WORD, font=("Consolas", 11))
    output_text.pack(pady=10)

    def run_query1():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('''
                SELECT 
                    s.soldier_name, 
                    EXTRACT(MONTH FROM t.date) AS month, 
                    EXTRACT(YEAR FROM t.date) AS year, 
                    COUNT(*) AS number_of_treatments
                FROM Treatment t
                JOIN soldier s ON t.paramedic_id = s.soldier_id AND s.role_type = 'paramedic'
                GROUP BY s.soldier_name, month, year
                ORDER BY year DESC, month DESC;
            ''')
            results = cur.fetchall()
            output_text.delete("1.0", END)

            output_text.insert(END, "מספר הטיפולים שביצע כל פרמדיק בכל חודש ושנה:\n\n")

            if not results:
                output_text.insert(END, "לא נמצאו תוצאות.\n")
            else:
                for row in results:
                    output_text.insert(END, f"שם (soldier_name): {row[0]}\n")
                    output_text.insert(END, f"חודש (month): {int(row[1])}\n")
                    output_text.insert(END, f"שנה (year): {int(row[2])}\n")
                    output_text.insert(END, f"מספר טיפולים (number_of_treatments): {row[3]}\n")
                    output_text.insert(END, "-" * 40 + "\n")

            conn.close()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))

    def run_query2():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('''
                UPDATE Patient
                SET patient_type = 2
                WHERE soldier_id IN (
                    SELECT rt.soldier_id
                    FROM receives_treatment rt
                    JOIN Treatment t ON rt.treatment_id = t.treatment_id
                    WHERE rt.role_type = 'patient'
                    GROUP BY rt.soldier_id
                    HAVING COUNT(DISTINCT rt.treatment_id) > 3
                );
            ''')
            conn.commit()
            output_text.delete("1.0", END)
            output_text.insert(END, "✅ עדכון סוג פצוע:\nעודכנו כל הפצועים שעברו יותר מ-3 טיפולים.\n")
            conn.close()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))

    def run_function():
        try:
            conn = get_connection()
            cur = conn.cursor()

            # חשוב לפתוח טרנזקציה כדי להשתמש בקורסור
            cur.execute("BEGIN;")

            # הרצת הפונקציה עם שני פרמטרים בלבד (hospital_id, min_treatments)
            cur.execute("SELECT get_patients_in_hospital_by_treatments(%s, %s);", (2, 2))
            cursor_name = cur.fetchone()[0]  # מקבלים את שם הקורסור שהוחזר

            # שואבים את כל הנתונים מהקורסור הזה
            cur.execute(f"FETCH ALL FROM \"{cursor_name}\";")
            rows = cur.fetchall()

            output_text.delete("1.0", END)
            output_text.insert(END, "פצועים בבית חולים לפי סינון טיפולים:\n\n")

            if not rows:
                output_text.insert(END, "לא נמצאו פצועים העונים לקריטריונים.\n")
            else:
                for row in rows:
                    output_text.insert(END, f"מספר זיהוי (ID): {row[0]}\n")
                    output_text.insert(END, f"שם (Name): {row[1]}\n")
                    output_text.insert(END, f"ניסיון (Experience): {row[2]}\n")
                    output_text.insert(END, f"מזהה בי\"ח (Hospital ID): {row[3]}\n")
                    output_text.insert(END, "-" * 40 + "\n")

            # סגירת הקורסור והטרנזקציה
            cur.execute(f"CLOSE \"{cursor_name}\";")
            cur.execute("COMMIT;")
            cur.close()
            conn.close()

        except Exception as e:
            output_text.delete("1.0", END)
            output_text.insert(END, "שגיאה: " + str(e) + "\n")
            messagebox.showerror("שגיאה", str(e))

    def run_procedure():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("CALL promote_commander_if_qualified(%s, %s);", (5, 3))
            conn.commit()
            output_text.delete("1.0", END)
            output_text.insert(END, "✅ בוצע בהצלחה:\nעודכנו כל המפקדים עם ניסיון מעל 5 שנים שמפקדים על יותר מ-3 מבצעים.\n")
            cur.close()
            conn.close()
        except Exception as e:
            output_text.delete("1.0", END)
            output_text.insert(END, "שגיאה בהרצת הפרוצדורה:\n" + str(e))
            messagebox.showerror("שגיאה", str(e))

    Button(win, text="שאילתה 1 - טיפולים לפי פרמדיק", command=run_query1, width=40, bg="#336699", fg="white").pack(pady=5)
    Button(win, text="שאילתה 2 - עדכון סוג פצוע", command=run_query2, width=40, bg="#339966", fg="white").pack(pady=5)
    Button(win, text="הרצת פונקציה - פצועים בבית חולים", command=run_function, width=40, bg="#cc6600", fg="white").pack(pady=5)
    Button(win, text="הרצת פרוצדורה - קידום מפקדים", command=run_procedure, width=40, bg="#993366", fg="white").pack(pady=5)
