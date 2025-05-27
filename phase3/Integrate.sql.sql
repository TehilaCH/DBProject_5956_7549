-- יצירת טבלת-על soldier
CREATE TABLE IF NOT EXISTS soldier (
  soldier_id INT,
  soldier_name VARCHAR(50),
  experience INTEGER,
  role_type VARCHAR(20) CHECK (role_type IN ('patient', 'paramedic', 'commander')),
  PRIMARY KEY (soldier_id, role_type)
);


-- ברירת מחדל לניסיון
ALTER TABLE soldier
ALTER COLUMN experience SET DEFAULT 0;

-- מיזוג פרמדיקים
INSERT INTO soldier (soldier_id, soldier_name, experience, role_type)
SELECT paramedic_id, paramedic_name, experience, 'paramedic'
FROM paramedic
WHERE NOT EXISTS (
  SELECT 1 FROM soldier WHERE soldier_id = paramedic.paramedic_id AND role_type = 'paramedic'
);

-- עדכון פרמדיקים
ALTER TABLE paramedic
DROP COLUMN paramedic_name,
DROP COLUMN experience;

-- 1. יצירת עמודת role_type בטבלה paramedic עם ערך קבוע
ALTER TABLE paramedic ADD COLUMN role_type VARCHAR(20) DEFAULT 'paramedic' NOT NULL;

-- לפני מחיקת המפתח נמחק את המפתח הזר בטיפול 
ALTER TABLE treatment DROP CONSTRAINT treatment_paramedic_id_fkey;

ALTER TABLE paramedic
DROP CONSTRAINT paramedic_pkey;

ALTER TABLE paramedic
RENAME COLUMN paramedic_id TO soldier_id;


ALTER TABLE paramedic 
ADD PRIMARY KEY (soldier_id, role_type),
ADD FOREIGN KEY (soldier_id, role_type) REFERENCES soldier(soldier_id, role_type);

-- הוספת העמודה role_type לטבלת treatment
ALTER TABLE treatment ADD COLUMN role_type VARCHAR(20) DEFAULT 'paramedic' NOT NULL;

--החזרת המפתח הזר החדש לטיפול 
ALTER TABLE treatment
ADD CONSTRAINT treatment_paramedic_id_fkey
FOREIGN KEY (paramedic_id, role_type) REFERENCES soldier(soldier_id, role_type);


-- מיזוג מפקדים
INSERT INTO soldier (soldier_id, soldier_name, experience, role_type)
SELECT id, name, experienceYears, 'commander'
FROM commander
WHERE NOT EXISTS (
  SELECT 1 FROM soldier WHERE soldier_id = commander.id AND role_type = 'commander'
);

-- עדכון מפקדים
ALTER TABLE commander
DROP COLUMN name,
DROP COLUMN experienceYears;

ALTER TABLE commander ADD COLUMN role_type VARCHAR(20) DEFAULT 'commander' NOT NULL;

--  הסרת מפתח זר בטבלה operation שמפנה ל-commander
ALTER TABLE operation DROP CONSTRAINT operation_id_fkey;

ALTER TABLE commander
DROP CONSTRAINT commander_pkey;

ALTER TABLE commander
RENAME COLUMN id TO soldier_id;

ALTER TABLE commander
ADD PRIMARY KEY (soldier_id, role_type),
ADD FOREIGN KEY (soldier_id, role_type) REFERENCES soldier(soldier_id, role_type);

ALTER TABLE operation ADD COLUMN role_type VARCHAR(20) DEFAULT 'commander' NOT NULL;

-- 5. הוספת מחדש מפתח זר בטבלה operation שמפנה כעת ל-soldier

ALTER TABLE operation
ADD CONSTRAINT operation_commander_id_fkey
FOREIGN KEY (ID, role_type) REFERENCES soldier(soldier_id, role_type);

-- מיזוג פצועים
INSERT INTO soldier (soldier_id, soldier_name, experience, role_type)
SELECT patient_id, patient_name, NULL, 'patient'
FROM patient
WHERE NOT EXISTS (
  SELECT 1 FROM soldier WHERE soldier_id = patient.patient_id AND role_type = 'patient'
);

-- עדכון פצועים
ALTER TABLE patient
DROP COLUMN patient_name;

-- הוספת עמודת role_type עם ערך קבוע
ALTER TABLE patient ADD COLUMN role_type VARCHAR(20) DEFAULT 'patient' NOT NULL;

-- הסרת מפתח זר קודם מטבלת receives_treatment
ALTER TABLE receives_treatment DROP CONSTRAINT receives_treatment_patient_id_fkey;


ALTER TABLE patient
DROP CONSTRAINT patient_pkey;

ALTER TABLE patient
RENAME COLUMN patient_id TO soldier_id;

ALTER TABLE patient ADD COLUMN role_type VARCHAR(20) DEFAULT 'patient' NOT NULL;

-- הוספת מפתח ראשי חדש ומפתח זר לטבלת soldier
ALTER TABLE patient
ADD PRIMARY KEY (soldier_id, role_type),
ADD FOREIGN KEY (soldier_id, role_type) REFERENCES soldier(soldier_id, role_type);

-- הוספת עמודת role_type עם ערך ברירת מחדל
ALTER TABLE receives_treatment ADD COLUMN role_type VARCHAR(20) DEFAULT 'patient' NOT NULL;

-- שינוי שם העמודה patient_id ל-soldier_id (כדי להתאים למבנה החדש)
ALTER TABLE receives_treatment RENAME COLUMN patient_id TO soldier_id;

-- הוספת מפתח זר חדש שמפנה ל-soldier
ALTER TABLE receives_treatment
ADD CONSTRAINT receives_treatment_patient_id_fkey
FOREIGN KEY (soldier_id, role_type) REFERENCES soldier(soldier_id, role_type);




ALTER TABLE equipment RENAME TO operational_equipment;

-- שלב 3: יצירת טבלת ציוד מאוחדת
CREATE TABLE IF NOT EXISTS equipment (
  equipment_id INT,
  equipment_name VARCHAR(50),
  quantity INT,
  equipment_type VARCHAR(20) CHECK (equipment_type IN ('medical', 'operational')),
  PRIMARY KEY (equipment_id, equipment_type)
);

-- מיזוג ציוד רפואי
INSERT INTO equipment (equipment_id, equipment_name, quantity, equipment_type)
SELECT equipment_id, equipment_name, quantity_, 'medical'
FROM medical_equipment
WHERE NOT EXISTS (
  SELECT 1 FROM equipment 
  WHERE equipment_id = medical_equipment.equipment_id AND equipment_type = 'medical'
);

-- מיזוג ציוד מבצעי
INSERT INTO equipment (equipment_id, equipment_name, quantity, equipment_type)
SELECT EquipmentID, Name, Quantity, 'operational'
FROM operational_equipment
WHERE NOT EXISTS (
  SELECT 1 FROM equipment 
  WHERE equipment_id = operational_equipment.EquipmentID AND equipment_type = 'operational'
);

-- הסרת המפתח הזר הישן
ALTER TABLE uses DROP CONSTRAINT uses_equipment_id_fkey;

-- הוספת עמודה חדשה לסיווג הציוד
ALTER TABLE uses ADD COLUMN equipment_type VARCHAR(20) DEFAULT 'medical' NOT NULL;

-- הוספת מפתח זר חדש לטבלה המאוחדת
ALTER TABLE uses
ADD CONSTRAINT uses_equipment_fk
FOREIGN KEY (equipment_id, equipment_type)
REFERENCES equipment(equipment_id, equipment_type);


-- 1. מחיקת המפתח הזר הישן
ALTER TABLE Requires DROP CONSTRAINT requires_equipmentid_fkey;

-- 2. הוספת העמודה equipment_type עם ערך ברירת מחדל "operational"
ALTER TABLE Requires ADD COLUMN equipment_type VARCHAR(20) DEFAULT 'operational' NOT NULL;

-- 3. הוספת מפתח זר חדש אל הטבלה המאוחדת
ALTER TABLE Requires
ADD CONSTRAINT requires_equipment_fk
FOREIGN KEY (equipmentid, equipment_type)
REFERENCES equipment(equipment_id, equipment_type);

DROP TABLE IF EXISTS operational_equipment;
DROP TABLE IF EXISTS medical_equipment;