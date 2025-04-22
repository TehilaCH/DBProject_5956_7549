--מציגה את ממוצע מספר החולים בכל שנה:

SELECT 
    EXTRACT(YEAR FROM Medical_event.event_date) AS year,   -- מוציא את שנת האירוע
    AVG(Medical_event.number_of_injured) AS avg_patients    -- מחשב את ממוצע מספר הפצועים בכל שנה
FROM 
    Medical_event                                         -- טבלת האירועים הרפואיים
GROUP BY 
    EXTRACT(YEAR FROM Medical_event.event_date)            -- מקבץ לפי שנת האירוע
ORDER BY 
    year DESC;                                            -- ממיין לפי שנה, מהשנה החדשה לישנה
