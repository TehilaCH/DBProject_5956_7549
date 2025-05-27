CREATE VIEW Commander_Operations_View AS
SELECT
    o.operationid AS operation_id,
    o.operationname AS operation_name,
    s.soldier_name AS commander_name,
    o.startdate,
    o.location
FROM operation o
JOIN commander c 
    ON o.id = c.soldier_id AND o.role_type = c.role_type
JOIN soldier s 
    ON c.soldier_id = s.soldier_id AND c.role_type = s.role_type AND s.role_type = 'commander';

