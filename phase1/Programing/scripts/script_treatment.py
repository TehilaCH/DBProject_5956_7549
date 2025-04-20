import random
from datetime import datetime, timedelta

# רשימות לדוגמה של סוגי טיפול
treatment_types = ["First Aid", "Surgery", "Bandaging", "Pain Relief", "Observation", "X-Ray"]


# יצירת תאריך אקראי
def random_date(start_date, end_date):
    return start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )


# הגדרת תאריכים תחילת וסוף לטיפולים
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

# רשימת paramedic_id שלך (מ-1 עד 400)
paramedic_ids = list(range(1, 401))  # נניח שהחובשים הם 400 ואנחנו מקשרים לכל טיפול חובש אקראי

# יצירת הקובץ עם פקודות SQL
with open("treatment_inserts.sql", "w", encoding='utf-8') as f:
    for i in range(1, 401):  # 400 טיפולים בדיוק
        # סוג טיפול אקראי
        treatment_type = random.choice(treatment_types)

        # משך זמן טיפול אקראי בין 30 ל-180 דקות
        treatment_duration = random.randint(30, 180)

        # יצירת תאריך טיפול אקראי
        treatment_date = random_date(start_date, end_date).date()

        # בחר פצוע אקראי מתוך 400 פצועים
        patient_id = random.randint(1, 400)

        # בחר חובש אקראי מתוך רשימת ה-paramedic_id
        paramedic_id = random.choice(paramedic_ids)

        # יצירת הפקודה SQL
        sql = f"INSERT INTO Treatment (treatment_id, treatment_duration, date, treatment_type, paramedic_id) VALUES ({i}, {treatment_duration}, '{treatment_date}', '{treatment_type}', {paramedic_id});\n"
        f.write(sql)

print("✅ קובץ 'treatment_inserts.sql' נוצר בהצלחה עם 400 טיפולים.")
