--כל האירועים שהתרחשו בשנת 2024:

SELECT 
    Medical_event.event_id,                -- מזהה האירוע הרפואי
    Paramedic.paramedic_name,             -- שם הפרמדיק שביצע את הטיפול
    Patient.patient_name,                 -- שם הפצוע
    Medical_event.event_date,             -- תאריך האירוע
    Hospital.hospital_name                -- שם בית החולים שאליו פונָה הפצוע
FROM Medical_event
JOIN Patient 
    ON Patient.event_id = Medical_event.event_id
    -- מחברים בין טבלת האירועים לבין טבלת הפצועים: כל פצוע שייך לאירוע מסוים

JOIN Hospital 
    ON Patient.hospital_id = Hospital.hospital_id
    -- מחברים את הפצוע לבית החולים אליו פונה, לפי מזהה בית החולים

JOIN receives_treatment 
    ON receives_treatment.patient_id = Patient.patient_id
    -- מחברים את טבלת הקשר בין פצועים לטיפולים – כדי לדעת איזה טיפול קיבל כל פצוע

JOIN Treatment 
    ON Treatment.treatment_id = receives_treatment.treatment_id
    -- מחברים את פרטי הטיפול עצמו לפי מזהה הטיפול

JOIN Paramedic 
    ON Paramedic.paramedic_id = Treatment.paramedic_id
    -- מחברים את הטיפול לפרמדיק שביצע אותו, לפי מזהה הפרמדיק

WHERE EXTRACT(YEAR FROM Medical_event.event_date) = 2024;
-- מסננים את התוצאה כך שתציג רק אירועים שהתרחשו בשנת 2024
