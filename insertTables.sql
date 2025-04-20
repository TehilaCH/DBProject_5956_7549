-- הכנסת נתונים לטבלת paramedic
INSERT INTO paramedic (paramedic_ID, paramedic_Name, experience) VALUES
(100001, 'David Cohen', 5),
(100002, 'Sarah Levy', 8),
(100003, 'John Doe', 3);

-- הכנסת נתונים לטבלת medical_event-- הכנסת נתונים לטבלת medical_event
INSERT INTO Medical_event (event_id, event_location, number_of_injured, event_date) VALUES
(20001, 'Tel Aviv', 3, '2024-03-29'),
(20002, 'Jerusalem', 5, '2024-03-30'),
(20003, 'Haifa', 2, '2024-04-01');

-- הכנסת נתונים לטבלת medical_equipment
INSERT INTO medical_equipment (equipment_Name, equipment_ID, quantity_) VALUES
(101, 3001, 10),
(102, 3002, 5),
(103, 3003, 8);

-- הכנסת נתונים לטבלת Treatment
INSERT INTO Treatment (treatment_duration, date, Treatment_type, Treatment_ID, paramedic_ID) VALUES
(30, '2024-03-29', 1, 40001, 100001),
(45, '2024-03-30', 2, 40002, 100002),
(20, '2024-04-01', 1, 40003, 100003);

-- הכנסת נתונים לטבלת Hospital
INSERT INTO Hospital (Hospital_Name, address, Hospital_ID) VALUES
('Ichilov', 'Tel Aviv', 5001),
('Shaare Zedek', 'Jerusalem', 5002),
('Rambam', 'Haifa', 5003);

-- הכנסת נתונים לטבלת uses
INSERT INTO uses (equipment_ID, Treatment_ID) VALUES
(3001, 40001),
(3002, 40002),
(3003, 40003);

-- הכנסת נתונים לטבלת patient
INSERT INTO patient (patient_ID, patient_Name, birthday, patient_type, event_ID, Hospital_ID) VALUES
(900001, 'Eli Ben Haim', '1990-05-20', 1, 20001, 5001),
(900002, 'Maya Ron', '1985-08-12', 2, 20002, 5002),
(900003, 'Avi Gold', '1995-01-30', 1, 20003, 5003);

-- הכנסת נתונים לטבלת receives_treatment
INSERT INTO receives_treatment (patient_ID, Treatment_ID) VALUES
(900001, 40001),
(900002, 40002),
(900003, 40003);
