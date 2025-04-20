-- קבלת כל הנתונים מכל הטבלאות
SELECT * FROM Paramedic;
SELECT * FROM Medical_event;
SELECT * FROM Medical_equipment;
SELECT * FROM Treatment;
SELECT * FROM Hospital;
SELECT * FROM uses;
SELECT * FROM Patient;
SELECT * FROM receives_treatment;

-- ספירת מספר הרשומות בכל טבלה
SELECT COUNT(*) AS total_paramedics FROM Paramedic;
SELECT COUNT(*) AS total_medical_events FROM Medical_event;
SELECT COUNT(*) AS total_medical_equipment FROM Medical_equipment;
SELECT COUNT(*) AS total_treatments FROM Treatment;
SELECT COUNT(*) AS total_hospitals FROM Hospital;
SELECT COUNT(*) AS total_uses FROM uses;
SELECT COUNT(*) AS total_patients FROM Patient;
SELECT COUNT(*) AS total_receives_treatment FROM receives_treatment;
