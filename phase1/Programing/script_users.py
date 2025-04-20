import random

num_treatments = 400
num_equipment = 400
total_pairs = 400  # ניצור בדיוק 400 שורות

# זוגות שכבר נוצרו (כדי להימנע משכפול)
used_pairs = set()

with open("uses_inserts.sql", "w", encoding="utf-8") as f:
    count = 0
    while count < total_pairs:
        equipment_id = random.randint(1, num_equipment)
        treatment_id = random.randint(1, num_treatments)

        if (equipment_id, treatment_id) not in used_pairs:
            used_pairs.add((equipment_id, treatment_id))
            sql = f"INSERT INTO uses (equipment_id, treatment_id) VALUES ({equipment_id}, {treatment_id});\n"
            f.write(sql)
            count += 1

print("✅ קובץ 'uses_inserts.sql' נוצר בהצלחה עם בדיוק 400 שורות.")
