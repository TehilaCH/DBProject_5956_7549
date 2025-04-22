--מחיקת ציוד רפואי שלא נעשה בו שימוש באף טיפול:

DELETE FROM Medical_equipment                          -- מוחק רשומות מטבלת הציוד הרפואי
WHERE equipment_id NOT IN (                            -- רק אם מזהה הציוד לא נמצא ברשימת הציוד שבשימוש
    SELECT DISTINCT equipment_id                       -- בוחר את כל מזהי הציוד הייחודיים
    FROM uses                                          -- מתוך הטבלה שמתעדת שימושים בציוד רפואי בטיפולים
);