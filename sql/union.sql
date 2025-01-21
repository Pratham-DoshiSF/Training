SELECT DepartmentID AS ID FROM Employees
UNION
SELECT ManagerID AS ID FROM Departments;
