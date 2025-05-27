
SELECT 
    operation_name, 
    startdate, 
    location
FROM Commander_Operations_View
WHERE EXTRACT(YEAR FROM startdate)=2024;
