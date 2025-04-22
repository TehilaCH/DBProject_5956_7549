--מוחקת מטופלים שמעולם לא עברו טיפול

DELETE FROM Patient                                -- מוחק רשומות מהטבלה Patient (טבלת המטופלים)
WHERE patient_id NOT IN (                          -- מוחק רק את המטופלים שלא נמצאים ברשימת המטופלים שעברו טיפול
    SELECT DISTINCT patient_id                     -- בוחר את כל מזהי המטופלים שהופיעו בטיפולים
    FROM receives_treatment                        -- מתוך טבלת הקשר בין מטופלים לטיפולים
);