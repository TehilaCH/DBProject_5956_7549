-- חובשים שביצעו טיפולים באירועים עם יותר מ-10 פצועים 

SELECT DISTINCT                                      -- בוחר את התוצאות הייחודיות, כדי שלא יהיו כפילויות בתוצאות
    paramedic.paramedic_name,                         -- מציג את שם הפרמדיק
    medical_event.event_location,                     -- מציג את מיקום האירוע
    medical_event.number_of_injured                   -- מציג את מספר הפצועים באירוע
FROM 
    Paramedic paramedic                               -- טבלת הפרמדיקים
JOIN 
    Treatment treatment ON paramedic.paramedic_id = treatment.paramedic_id   -- מצטרף לטבלת הטיפולים ומחבר את מזהה הפרמדיק לכל טיפול
JOIN 
    receives_treatment receives_treatment ON treatment.treatment_id = receives_treatment.treatment_id  -- מצטרף לטבלת הטיפולים של החולים ומחבר את הטיפולים לחולים
JOIN 
    Patient patient ON receives_treatment.patient_id = patient.patient_id    -- מצטרף לטבלת החולים ומחבר את החולים לפי מזהה החולה
JOIN 
    Medical_event medical_event ON patient.event_id = medical_event.event_id -- מצטרף לטבלת האירועים ומחבר את האירועים לחולה לפי מזהה האירוע
WHERE 
    medical_event.number_of_injured > 10;           -- מסנן את התוצאות כך שיתווספו רק אירועים שבהם היו יותר מ-10 פצועים
