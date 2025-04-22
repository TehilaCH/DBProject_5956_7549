--כמות השימושים בציוד רפואי לפי חודש במהלך שנת 2023, ממוינת לפי חודש וסדר שימושים יורד

SELECT 
    Medical_equipment.equipment_id,                          -- ת"ז של הציוד
    Medical_equipment.equipment_name,                        -- שם הציוד
    EXTRACT(MONTH FROM Treatment.date) AS usage_month,       -- החודש שבו השתמשו בציוד
    COUNT(*) AS usage_count                                  -- כמות הפעמים שהשתמשו בציוד באותו חודש
FROM uses
JOIN Treatment 
    ON uses.treatment_id = Treatment.treatment_id
JOIN Medical_equipment 
    ON uses.equipment_id = Medical_equipment.equipment_id
WHERE EXTRACT(YEAR FROM Treatment.date) = 2023
GROUP BY 
    Medical_equipment.equipment_id,
    Medical_equipment.equipment_name,
    EXTRACT(MONTH FROM Treatment.date)
ORDER BY 
    usage_month,                -- קודם כל סידור לפי חודש (1, 2, 3 וכו’)
    usage_count DESC;           -- בתוך כל חודש – סידור מהכי הרבה שימושים לפחות