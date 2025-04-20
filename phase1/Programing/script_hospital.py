import random

# רשימות עם שמות בתי חולים וערים לדוגמה
names = [
    "Sheba", "Ichilov", "Hadassah", "Rambam", "Assuta",
    "Soroka", "Kaplan", "Bnai Zion", "Meir", "Barzilai",
    "Wolfson", "HaEmek", "Laniado", "Ziv", "Poriya"
]

cities = [
    "Tel Aviv", "Jerusalem", "Haifa", "Beer Sheva",
    "Rehovot", "Netanya", "Petah Tikva", "Holon",
    "Afula", "Ashkelon", "Safed", "Tiberias", "Raanana", "Nazareth"
]

# יצירת הקובץ עם פקודות SQL
with open("hospital_inserts.sql", "w", encoding='utf-8') as f:
    for i in range(1, 401):  # 400 רשומות בדיוק
        name = random.choice(names) + " Hospital"
        address = random.choice(cities) + ", Street " + str(random.randint(1, 150))
        sql = f"INSERT INTO Hospital (hospital_id, hospital_name, address) VALUES ({i}, '{name}', '{address}');\n"
        f.write(sql)

print("✅ קובץ 'hospital_inserts.sql' נוצר בהצלחה עם 400 רשומות.")
