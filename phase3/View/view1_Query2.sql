SELECT paramedic_name, COUNT(*) AS total_treatments
FROM Medical_Treatments_View
GROUP BY paramedic_name
ORDER BY total_treatments DESC;
