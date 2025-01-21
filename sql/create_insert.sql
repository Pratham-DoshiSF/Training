-- Create Employees table
CREATE TABLE Employees (
    EmployeeID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DepartmentID INT,
    Salary NUMERIC(10, 2),
    HireDate DATE
);

-- Create Departments table
CREATE TABLE Departments (
    DepartmentID SERIAL PRIMARY KEY,
    DepartmentName VARCHAR(100),
    ManagerID INT
);

-- Create Projects table
CREATE TABLE Projects (
    ProjectID SERIAL PRIMARY KEY,
    ProjectName VARCHAR(100),
    StartDate DATE,
    EndDate DATE
);

-- Create EmployeeProjects table (Many-to-Many relationship)
CREATE TABLE EmployeeProjects (
    EmployeeProjectID SERIAL PRIMARY KEY,
    EmployeeID INT REFERENCES Employees(EmployeeID),
    ProjectID INT REFERENCES Projects(ProjectID),
    HoursWorked INT
);

-- Insert sample data into Departments
INSERT INTO Departments (DepartmentName, ManagerID)
VALUES 
    ('IT', 1),
    ('HR', 2),
    ('Finance', 3);

-- Insert sample data into Employees
INSERT INTO Employees (FirstName, LastName, DepartmentID, Salary, HireDate)
VALUES 
    ('Alice', 'Smith', 1, 60000.00, '2020-01-15'),
    ('Bob', 'Johnson', 2, 50000.00, '2019-03-10'),
    ('Charlie', 'Brown', 3, 70000.00, '2018-07-20'),
    ('Diana', 'Prince', 1, 80000.00, '2021-09-12'),
    ('Eve', 'Davis', 2, 45000.00, '2022-05-01');

-- Insert sample data into Projects
INSERT INTO Projects (ProjectName, StartDate, EndDate)
VALUES 
    ('Website Development', '2023-01-01', '2023-06-30'),
    ('Employee Training', '2023-02-15', '2023-03-15'),
    ('Financial Audit', '2023-03-01', '2023-04-30');

-- Insert sample data into EmployeeProjects
INSERT INTO EmployeeProjects (EmployeeID, ProjectID, HoursWorked)
VALUES 
    (1, 1, 120),
    (2, 2, 50),
    (3, 3, 80),
    (1, 3, 60),
    (4, 1, 150);
