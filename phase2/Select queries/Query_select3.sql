--מספר הטיפולים שביצע כל פרמדיק בכל חודש ושנה.

SELECT 
    Paramedic.paramedic_name,                                       -- מציג את שם הפרמדיק
    EXTRACT(MONTH FROM Treatment.date) AS month,                    -- מחלץ את מספר החודש מתוך תאריך הטיפול
    EXTRACT(YEAR FROM Treatment.date) AS year,                      -- מחלץ את שנת הטיפול מתוך תאריך הטיפול
    COUNT(*) AS number_of_treatments                                -- סופר את מספר הטיפולים שביצע הפרמדיק בחודש ובשנה אלו
FROM 
    Treatment                                                       -- טבלת הטיפולים
JOIN 
    Paramedic ON Treatment.paramedic_id = Paramedic.paramedic_id    -- מצטרף לפרמדיק שביצע את הטיפול
GROUP BY 
    Paramedic.paramedic_name,                                       -- מקבץ לפי שם הפרמדיק
    EXTRACT(MONTH FROM Treatment.date),                             -- מקבץ לפי חודש מתוך תאריך הטיפול
    EXTRACT(YEAR FROM Treatment.date)                               -- מקבץ לפי שנה מתוך תאריך הטיפול
ORDER BY 
    year DESC,                                                      -- ממיין מהשנה המאוחרת לישנה
    month DESC;                                                     -- ובתוך אותה שנה מהמועד האחרון לראשון
