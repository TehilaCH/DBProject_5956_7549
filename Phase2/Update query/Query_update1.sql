--עדכון ניסיון פרמדיקים על פי סינון של מספר הפצועים:

UPDATE Paramedic
SET experience = experience + 1                        -- מוסיף שנה אחת לניסיון של כל פרמדיק
WHERE paramedic_id IN (                                 -- בוחר את מזהי הפרמדיקים שעמדו בתנאים
    SELECT DISTINCT t.paramedic_id                      -- בוחר את מזהי הפרמדיקים בטיפולים
    FROM Treatment t                                    -- מתוך טבלת הטיפולים
    JOIN receives_treatment rt                          -- מחבר את טבלת הטיפולים עם טבלת הקשר receives_treatment
        ON t.treatment_id = rt.treatment_id             -- מחבר לפי מזהה הטיפול
    JOIN Patient p                                      -- מחבר את המטופלים
        ON p.patient_id = rt.patient_id                 -- מחבר לפי מזהה המטופל
    JOIN Medical_event me                               -- מחבר לטבלת האירועים הרפואיים
        ON me.event_id = p.event_id                     -- מחבר לפי מזהה האירוע
    WHERE me.number_of_injured > 10                     -- רק אם מספר הפצועים באירוע היה יותר מ-10
);