-- מציאת הפרמדיקים עם ניסיון מעל לממוצע של כל הפרמדיקים
SELECT paramedic_name, experience
FROM Paramedic
WHERE experience > (
    SELECT AVG(experience)
    FROM Paramedic
);