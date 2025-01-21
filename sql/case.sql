select FirstName , 
CASE 
WHEN salary > 70000 THEN 'High salary'
WHEN salary < 50000 THEN 'Low salary'
ELSE
'Noramal Salary'
END as "SalaryRemark"
FROM employees;