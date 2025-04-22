-- רשימת ציוד שנעשה בו שימוש ביותר מ-5 טיפולים שונים

SELECT 
    medical_equipment.equipment_name,                        -- מציג את שם הציוד הרפואי
    COUNT(DISTINCT uses.treatment_id) AS num_usages           -- סופר את מספר השימושים הייחודיים של הציוד בטיפולים (לפי מזהה הטיפול)
FROM 
    uses                                                     -- טבלת השימושים של הציוד בטיפולים
JOIN 
    Medical_equipment ON uses.equipment_id = medical_equipment.equipment_id  -- מצטרף לטבלת הציוד הרפואי ומחבר את הציוד לשימוש בטיפולים
GROUP BY 
    medical_equipment.equipment_name                        -- מקבץ לפי שם הציוד הרפואי
HAVING 
    COUNT(DISTINCT uses.treatment_id) > 5                    -- מסנן את התוצאות כך שיתווספו רק הציוד שבו השתמשו ביותר מ-5 טיפולים ייחודיים
ORDER BY 
    num_usages DESC;                                         -- ממיין את התוצאות לפי מספר השימושים, מהציוד עם הכי הרבה שימושים ועד פחות
