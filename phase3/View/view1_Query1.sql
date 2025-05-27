SELECT DISTINCT patient_name
FROM Medical_Treatments_View
WHERE EXTRACT(YEAR FROM event_date) = 2023;