--מחיקת בתי חולים שלא נקלטו אליהם פצועים

DELETE FROM Hospital                             -- מוחק רשומות מהטבלה Hospital (בתי חולים)
WHERE hospital_id NOT IN (                       -- רק אם מזהה בית החולים לא מופיע אצל אף פצוע
    SELECT DISTINCT hospital_id                  -- כל בתי החולים שקלטו לפחות פצוע אחד
    FROM Patient
    WHERE hospital_id IS NOT NULL                -- מתעלם מערכים ריקים (כדי לא להשוות ל-NULL)
);