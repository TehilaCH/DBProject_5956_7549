import random
from datetime import datetime, timedelta

# רשימות של מיקומים לדוגמה
locations = ["Tel Aviv", "Jerusalem", "Haifa", "Beer Sheva", "Rehovot", "Netanya", "Petah Tikva", "Holon", "Afula",
             "Ashkelon"]


# יצירת תאריך אקראי
def random_date(start_date, end_date):
    return start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )


# הגדרת תאריכים תחילת וסוף לאירוע
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

# יצירת הקובץ עם פקודות SQL
with open("medical_event_inserts.sql", "w", encoding='utf-8') as f:
    for i in range(1, 401):  # 400 אירועים בדיוק
        location = random.choice(locations)
        event_date = random_date(start_date, end_date).date()
        number_of_injured = random.randint(1, 50)  # מספר פצועים בין 1 ל-50

        # יצירת הפקודה SQL
        sql = f"INSERT INTO Medical_event (event_id, event_location, number_of_injured, event_date) VALUES ({i}, '{location}', {number_of_injured}, '{event_date}');\n"
        f.write(sql)

print("✅ קובץ 'medical_event_inserts.sql' נוצר בהצלחה עם 400 אירועים.")
