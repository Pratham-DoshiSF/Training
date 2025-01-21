SELECT Firstname
FROM employees e
WHERE EXISTS (
    SELECT 1
    FROM employeeprojects ep
    WHERE ep.Employeeid = e.Employeeid
    AND ep.HoursWorked < 70
);
