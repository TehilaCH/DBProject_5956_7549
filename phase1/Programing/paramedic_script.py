import pandas as pd
import psycopg2

# קריאת קובץ Mockaroo
df = pd.read_csv('ParamedicData.csv')

# התחברות למסד הנתונים
conn = psycopg2.connect(
    host="127.0.0.2",
    dbname="Medical_Corps",
    user="Tehila_user",
    password="Tehila2003"
)
cur = conn.cursor()

# הוספת הנתונים לטבלת Paramedic
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO Paramedic (paramedic_id, paramedic_name, experience)
        VALUES (%s, %s, %s)
    """, (int(row['paramedic_id']), row['paramedic_name'], int(row['experience'])))

conn.commit()
cur.close()
conn.close()
