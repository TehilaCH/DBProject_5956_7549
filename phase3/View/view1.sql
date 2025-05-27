CREATE VIEW Medical_Treatments_View AS
SELECT
    t.treatment_id,
    t.treatment_type,
    t.treatment_duration,
    t.date,
    ps.soldier_name AS paramedic_name,
    pt_soldier.soldier_name AS patient_name,
    pt.birthday,
    me.event_date,
    h.hospital_name
FROM Treatment t
JOIN soldier ps ON t.paramedic_id = ps.soldier_id AND t.role_type = ps.role_type AND ps.role_type = 'paramedic'
JOIN receives_treatment rt ON t.treatment_id = rt.treatment_id
JOIN patient pt ON rt.soldier_id = pt.soldier_id AND rt.role_type = pt.role_type
JOIN soldier pt_soldier ON pt.soldier_id = pt_soldier.soldier_id AND pt.role_type = pt_soldier.role_type AND pt_soldier.role_type = 'patient'
JOIN Medical_event me ON pt.event_id = me.event_id
LEFT JOIN Hospital h ON pt.hospital_id = h.hospital_id;