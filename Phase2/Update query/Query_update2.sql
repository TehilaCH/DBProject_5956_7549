--עדכון כמות הציוד הרפואי לפי ציוד שנעשה בו שימוש ביותר מ-2 טיפולים

UPDATE Medical_equipment
-- עדכון כמות הציוד ב-5 יחידות נוספות
SET quantity_ = quantity_ + 5
-- עדכון הציוד הרפואי רק עבור ציוד שהשתמשו בו ביותר מ-5 טיפולים שונים
WHERE equipment_id IN (
    -- בחר את מזהי הציוד מתוך טבלת uses
    SELECT u.equipment_id
    FROM uses u
    -- הצטרף לטבלת Treatment לפי מזהה הטיפול
    JOIN Treatment t ON u.treatment_id = t.treatment_id
    -- קבץ את הציוד לפי מזהה הציוד
    GROUP BY u.equipment_id
    -- סנן את הציוד בו השתמשו ביותר מ-2 טיפולים שונים
    HAVING COUNT(DISTINCT u.treatment_id) > 2
);