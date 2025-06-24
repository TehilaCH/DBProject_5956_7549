from tkinter import *
from operation_crud import open_operation_crud
from equipment_crud import open_equipment_crud
from requires_crud import open_requires_crud
from query_and_procedure import open_query_and_procedure

def main():
    root = Tk()
    root.title("ברוכים הבאים למערכת של צה״ל")
    root.geometry("600x450")
    root.configure(bg="#e6f2ff")

    Label(
        root,
        text="מערכת לניהול מבצעים, ציוד ודרישות",
        font=("Arial", 18, "bold"),
        bg="#e6f2ff",
        fg="#003366"
    ).pack(pady=30)

    Button(root, text="ניהול מבצעים", command=open_operation_crud,
           font=("Arial", 14), width=25, bg="#004d00", fg="white").pack(pady=10)

    Button(root, text="ניהול ציוד", command=open_equipment_crud,
           font=("Arial", 14), width=25, bg="#005580", fg="white").pack(pady=10)

    Button(root, text="ניהול דרישות ציוד", command=open_requires_crud,
           font=("Arial", 14), width=25, bg="#99004d", fg="white").pack(pady=10)

    Button(root, text="שאילתות ופרוצדורות", command=open_query_and_procedure,
           font=("Arial", 14), width=25, bg="#663399", fg="white").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
