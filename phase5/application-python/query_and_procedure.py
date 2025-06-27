from tkinter import *
from tkinter import messagebox, ttk
from db_config import get_connection

def open_query_and_procedure():
    win = Toplevel()
    win.title("Queries and Procedures")
    win.geometry("900x650")
    win.configure(bg="#fff9e6")

    Label(win, text="Queries and Procedures", font=("Arial", 16, "bold"), bg="#fff9e6").pack(pady=10)

    table_frame = Frame(win)
    table_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

    columns = ("col1", "col2", "col3", "col4")

    style = ttk.Style()
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="white",
                    font=("Arial", 11))
    style.configure("Treeview.Heading",
                    font=("Arial", 12, "bold"),
                    background="#f0f0f0")
    style.map('Treeview', background=[('selected', '#cde8ff')])

    y_scrollbar = Scrollbar(table_frame, orient=VERTICAL)
    y_scrollbar.pack(side=RIGHT, fill=Y)

    x_scrollbar = Scrollbar(table_frame, orient=HORIZONTAL)
    x_scrollbar.pack(side=BOTTOM, fill=X)

    tree = ttk.Treeview(table_frame,
                        columns=columns,
                        show='headings',
                        yscrollcommand=y_scrollbar.set,
                        xscrollcommand=x_scrollbar.set)

    y_scrollbar.config(command=tree.yview)
    x_scrollbar.config(command=tree.xview)

    tree.pack(fill=BOTH, expand=True)

    tree.tag_configure('oddrow', background='#f1f8e9')
    tree.tag_configure('evenrow', background='#dcedc8')

    def clear_tree():
        for item in tree.get_children():
            tree.delete(item)

    def update_table(data, headers):
        clear_tree()
        tree["columns"] = headers
        for col in headers:
            tree.heading(col, text=col)
            tree.column(col, width=220, anchor=CENTER)
        for i, row in enumerate(data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=row, tags=(tag,))

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
            headers = ["Soldier Name", "Month", "Year", "Number of Treatments"]
            update_table(results, headers)
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_query3():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('''
                SELECT 
                    s.soldier_id,
                    s.soldier_name,
                    COUNT(rt.treatment_id) AS treatment_count
                FROM 
                    soldier s
                JOIN 
                    receives_treatment rt 
                    ON s.soldier_id = rt.soldier_id AND s.role_type = 'patient' AND rt.role_type = 'patient'
                GROUP BY 
                    s.soldier_id, s.soldier_name
                HAVING 
                    COUNT(rt.treatment_id) > 2
                ORDER BY 
                    treatment_count DESC;
            ''')
            results = cur.fetchall()
            headers = ["Soldier ID", "Soldier Name", "Treatment Count"]
            update_table(results, headers)
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_function():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("BEGIN;")
            cur.execute("SELECT get_patients_in_hospital_by_treatments(%s, %s);", (2, 2))
            cursor_name = cur.fetchone()[0]
            cur.execute(f"FETCH ALL FROM \"{cursor_name}\";")
            rows = cur.fetchall()
            cur.execute(f"CLOSE \"{cursor_name}\";")
            cur.execute("COMMIT;")
            cur.close()
            conn.close()

            headers = ["Patient ID", "Name", "Experience", "Hospital ID"]
            update_table(rows, headers)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_procedure_and_show_commanders():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("CALL promote_commander_if_qualified();")
            conn.commit()
            cur.execute('''
                SELECT s.soldier_id, s.soldier_name, s.experience, c.rank
                FROM soldier s
                JOIN commander c ON s.soldier_id = c.soldier_id
                WHERE s.role_type = 'commander' AND c.role_type = 'commander'
                ORDER BY c.rank;
            ''')
            results = cur.fetchall()
            headers = ["Soldier ID", "Name", "Experience", "Rank"]
            update_table(results, headers)
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_commanders_before_update():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('''
                SELECT s.soldier_id, s.soldier_name, s.experience, c.rank
                FROM soldier s
                JOIN commander c ON s.soldier_id = c.soldier_id
                WHERE s.role_type = 'commander' AND c.role_type = 'commander'
                ORDER BY c.rank;
            ''')
            results = cur.fetchall()
            headers = ["Soldier ID", "Name", "Experience", "Rank"]
            update_table(results, headers)
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    buttons_frame = Frame(win, bg="#fff9e6")
    buttons_frame.pack(fill=X, pady=10)

    Button(buttons_frame, text="Query 1 - Treatments by Paramedic", command=run_query1,
           width=40, bg="#336699", fg="white").pack(pady=3)
    Button(buttons_frame, text="Run Function - Patients in Hospital", command=run_function,
           width=40, bg="#cc6600", fg="white").pack(pady=3)
    Button(buttons_frame, text="Query 3 - Patients with >2 Treatments", command=run_query3,
           width=40, bg="#339966", fg="white").pack(pady=3)
    Button(buttons_frame, text="Show Commanders Before Update", command=show_commanders_before_update,
           width=40, bg="#999966", fg="white").pack(pady=3)
    Button(buttons_frame, text="Promote Commanders & Show", command=run_procedure_and_show_commanders,
           width=40, bg="#9933cc", fg="white").pack(pady=3)

