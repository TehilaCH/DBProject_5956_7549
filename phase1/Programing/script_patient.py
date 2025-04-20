import random
from datetime import datetime, timedelta

# רשימות עם שמות הפצועים והערים לדוגמה
first_names = ["David", "Yaara", "Miriam", "Yossi", "Dani", "Noa", "Avraham", "Ruth", "Shimon", "Yaakov"]
last_names = ["Cohen", "Levi", "Mizrahi", "Ben-David", "Shapira", "Goldstein", "Friedman", "Peretz", "Levy", "Katz"]


# יצירת תאריך אקראי
def random_date(start_date, end_date):
    return start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )


# הגדרת תאריכים תחילת וסוף לפצועים
start_date = datetime(1980, 1, 1)
end_date = datetime(2005, 12, 31)

# יצירת הקובץ עם פקודות SQL
with open("patient_inserts.sql", "w", encoding='utf-8') as f:
    for i in range(1, 401):  # 400 פצועים בדיוק
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        patient_name = f"{first_name} {last_name}"

        # יצירת תאריך לידה אקראי
        birthday = random_date(datetime(1980, 1, 1), datetime(2005, 12, 31)).date()

        # סוג פצוע אקראי (1 או 2 לדוגמה)
        patient_type = random.choice([1, 2])

        # יצירת event_id אקראי בין 1 ל-400 (ה-IDs אמורים להתאים לאירועים הקיימים בטבלת Medical_event)
        event_id = random.randint(1, 400)  # תוודא שה-ID הזה קיים בטבלת Medical_event

        # יצירת הפקודה SQL
        sql = f"INSERT INTO Patient (patient_id, patient_name, birthday, patient_type, event_id) VALUES ({i}, '{patient_name}', '{birthday}', {patient_type}, {event_id});\n"
        f.write(sql)

print("✅ קובץ 'patient_inserts.sql' נוצר בהצלחה עם 400 פצועים.")
