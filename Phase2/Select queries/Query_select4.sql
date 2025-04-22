--רשימת החולים שטופלו ביותר מ-2 טיפולים

SELECT 
    patient.patient_id,                                     -- מציג את מזהה החולה
    patient.patient_name,                                   -- מציג את שם החולה
    COUNT(receives_treatment.treatment_id) AS treatment_count -- סופר את מספר הטיפולים של החולה
FROM 
    Patient                                          -- טבלת החולים
JOIN 
    receives_treatment ON patient.patient_id = receives_treatment.patient_id  -- מצטרף לטבלת הטיפולים לפי מזהה החולה
GROUP BY 
    patient.patient_id,                                     -- מקבץ לפי מזהה החולה
    patient.patient_name                                    -- ומבצע גם קיבוץ לפי שם החולה
HAVING 
    COUNT(receives_treatment.treatment_id) > 2               -- מסנן את התוצאות כך שרק חולים עם יותר מ-2 טיפולים יוצגו
ORDER BY 
    treatment_count DESC;                                    -- ממיין את התוצאות לפי מספר טיפולים, מהחולה עם הכי הרבה טיפולים ועד לפחות
