-- Script that creates a view need_meeting that list all students
-- that have a score under 80 (strit) and no last_meeting
-- or more that one month
DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS
SELECT name, FROM students
WHERE score < 80 AND 
    (last_meeting IS NULL
        OR
    last_meeting < ADDDATE(CURDATE(), INTERVAL -1 MONTH)
);
