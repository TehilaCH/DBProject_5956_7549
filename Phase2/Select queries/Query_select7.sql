-- חולים שטופלו בטיפולים שבוצעו על ידי חובשים עם ניסיון מעל 10

SELECT 
    patient.patient_name,                                        -- מציג את שם החולה
    paramedic.paramedic_name,                                     -- מציג את שם הפרמדיק
    paramedic.experience                                         -- מציג את מספר שנות הניסיון של הפרמדיק
FROM 
    Patient                                                      -- טבלת החולים
JOIN 
    receives_treatment receives_treatment ON patient.patient_id = receives_treatment.patient_id  -- מצטרף לטבלת הטיפולים של החולים ומחבר את החולים לפי מזהה החולה
JOIN 
    Treatment treatment ON receives_treatment.treatment_id = treatment.treatment_id  -- מצטרף לטבלת הטיפולים ומחבר את הטיפולים לפי מזהה הטיפול
JOIN 
    Paramedic paramedic ON treatment.paramedic_id = paramedic.paramedic_id  -- מצטרף לטבלת הפרמדיקים ומחבר את הטיפולים עם הפרמדיקים לפי מזהה הפרמדיק
WHERE 
    paramedic.experience > 10;                                    -- מסנן את התוצאות כך שיתווספו רק פרמדיקים עם יותר מ-10 שנות ניסיון
