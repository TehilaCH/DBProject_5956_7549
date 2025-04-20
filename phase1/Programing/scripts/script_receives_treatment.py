import random

num_patients = 400
num_treatments = 400
total_pairs = 400  # בדיוק 400 שורות

# כדי למנוע כפילויות, נשמור זוגות שכבר יצרנו
used_pairs = set()

with open("receives_treatment_inserts.sql", "w", encoding="utf-8") as f:
    count = 0
    while count < total_pairs:
        patient_id = random.randint(1, num_patients)
        treatment_id = random.randint(1, num_treatments)

        # בדיקה אם כבר השתמשנו בזוג הזה
        if (patient_id, treatment_id) not in used_pairs:
            used_pairs.add((patient_id, treatment_id))
            sql = f"INSERT INTO receives_treatment (patient_id, treatment_id) VALUES ({patient_id}, {treatment_id});\n"
            f.write(sql)
            count += 1

print("✅ קובץ 'receives_treatment_inserts.sql' נוצר בהצלחה עם בדיוק 400 שורות.")
