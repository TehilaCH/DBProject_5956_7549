SELECT 
    commander_name, 
    COUNT(*) AS number_of_operations
FROM Commander_Operations_View
GROUP BY commander_name
ORDER BY number_of_operations DESC;