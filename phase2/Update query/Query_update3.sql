--עדכון סוג פצוע עבור חולה שעבר יותר מ-3 טיפולים

UPDATE Patient
-- מגדירים את סוג הפצוע כ-2 (למשל: בינוני)
SET patient_type = 2  
-- תנאי: רק לחולים שמופיעים בתת-שאילתה הבאה
WHERE patient_id IN (
    -- בחירת מזהי חולים מתוך טבלת הקשר receives_treatment
    SELECT rt.patient_id
    FROM receives_treatment rt
    -- מצטרפים לטבלת הטיפולים כדי לוודא התאמה תקינה בין טיפולים לחולים
    JOIN Treatment t ON rt.treatment_id = t.treatment_id
    -- מקבצים לפי מזהה חולה – כדי שנוכל לבדוק כמה טיפולים שונים כל חולה קיבל
    GROUP BY rt.patient_id
    -- מסננים רק את החולים שקיבלו יותר מ-3 טיפולים שונים
    HAVING COUNT(DISTINCT rt.treatment_id) > 3  
);