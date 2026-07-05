DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    region TEXT NOT NULL,
    segment TEXT NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_price REAL NOT NULL,
    stock_quantity INTEGER NOT NULL,
    reorder_level INTEGER NOT NULL,
    supplier TEXT NOT NULL
);

CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    sale_date TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    total_amount REAL NOT NULL,
    sales_channel TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    program TEXT NOT NULL,
    year_level INTEGER NOT NULL,
    gpa REAL NOT NULL,
    enrollment_status TEXT NOT NULL
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_code TEXT NOT NULL UNIQUE,
    course_name TEXT NOT NULL,
    credits INTEGER NOT NULL
);

CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    term TEXT NOT NULL,
    grade REAL NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE support_tickets (
    ticket_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    issue_type TEXT NOT NULL,
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    resolution_time_hours REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO customers (customer_id, full_name, email, region, segment) VALUES
(1, 'Ava Johnson', 'ava.johnson@example.com', 'North America', 'Enterprise'),
(2, 'Noah Smith', 'noah.smith@example.com', 'Europe', 'Small Business'),
(3, 'Mia Garcia', 'mia.garcia@example.com', 'Latin America', 'Consumer'),
(4, 'Liam Brown', 'liam.brown@example.com', 'North America', 'Enterprise'),
(5, 'Emma Wilson', 'emma.wilson@example.com', 'Asia Pacific', 'Small Business'),
(6, 'Olivia Martinez', 'olivia.martinez@example.com', 'Latin America', 'Consumer'),
(7, 'James Lee', 'james.lee@example.com', 'Asia Pacific', 'Enterprise'),
(8, 'Sophia Davis', 'sophia.davis@example.com', 'Europe', 'Consumer');

INSERT INTO products (product_id, sku, name, category, unit_price, stock_quantity, reorder_level, supplier) VALUES
(1, 'LAP-1400', 'Business Laptop 14', 'Computers', 980.00, 18, 10, 'Northwind Hardware'),
(2, 'MON-2700', '27 Inch Monitor', 'Displays', 260.00, 8, 12, 'BrightView Supply'),
(3, 'KEY-MECH', 'Mechanical Keyboard', 'Accessories', 89.90, 32, 15, 'KeyWorks'),
(4, 'MOU-WL20', 'Wireless Mouse', 'Accessories', 34.50, 11, 20, 'KeyWorks'),
(5, 'SRV-MINI', 'Mini Database Server', 'Servers', 2450.00, 4, 5, 'Northwind Hardware'),
(6, 'SSD-1TB', '1TB Solid State Drive', 'Storage', 115.00, 26, 10, 'DataCore'),
(7, 'RTR-AX', 'WiFi 6 Router', 'Networking', 175.00, 7, 8, 'NetLink'),
(8, 'CAM-HD', 'HD Conference Camera', 'Video', 129.00, 14, 6, 'BrightView Supply');

INSERT INTO sales (sale_id, customer_id, product_id, sale_date, quantity, total_amount, sales_channel) VALUES
(1, 1, 1, '2026-01-12', 3, 2940.00, 'Online'),
(2, 2, 3, '2026-01-15', 10, 899.00, 'Partner'),
(3, 3, 4, '2026-02-03', 5, 172.50, 'Online'),
(4, 4, 5, '2026-02-10', 2, 4900.00, 'Direct Sales'),
(5, 5, 2, '2026-03-02', 6, 1560.00, 'Online'),
(6, 6, 6, '2026-03-18', 8, 920.00, 'Partner'),
(7, 7, 5, '2026-04-07', 1, 2450.00, 'Direct Sales'),
(8, 8, 8, '2026-04-22', 4, 516.00, 'Online'),
(9, 1, 6, '2026-05-05', 12, 1380.00, 'Online'),
(10, 4, 1, '2026-05-20', 2, 1960.00, 'Direct Sales'),
(11, 7, 7, '2026-06-02', 5, 875.00, 'Partner'),
(12, 5, 3, '2026-06-11', 7, 629.30, 'Online');

INSERT INTO students (student_id, full_name, program, year_level, gpa, enrollment_status) VALUES
(1, 'Daniel Carter', 'Computer Science', 2, 3.72, 'Active'),
(2, 'Emily Nguyen', 'Information Systems', 3, 3.55, 'Active'),
(3, 'Mateo Rivera', 'Computer Science', 4, 3.91, 'Active'),
(4, 'Grace Kim', 'Data Analytics', 1, 3.44, 'Active'),
(5, 'Isabella Rossi', 'Information Systems', 2, 3.20, 'Inactive'),
(6, 'Ethan Walker', 'Cybersecurity', 3, 3.68, 'Active'),
(7, 'Camila Torres', 'Computer Science', 1, 3.35, 'Active'),
(8, 'William Chen', 'Data Analytics', 4, 3.88, 'Active');

INSERT INTO courses (course_id, course_code, course_name, credits) VALUES
(1, 'CS101', 'Programming Fundamentals', 4),
(2, 'DB210', 'Database Systems', 4),
(3, 'AI330', 'Applied Artificial Intelligence', 3),
(4, 'SEC240', 'Network Security', 3),
(5, 'DA220', 'Data Visualization', 3);

INSERT INTO enrollments (enrollment_id, student_id, course_id, term, grade) VALUES
(1, 1, 2, '2026-I', 17.5),
(2, 1, 3, '2026-I', 18.2),
(3, 2, 2, '2026-I', 16.4),
(4, 3, 3, '2026-I', 19.1),
(5, 4, 5, '2026-I', 15.8),
(6, 6, 4, '2026-I', 17.0),
(7, 7, 1, '2026-I', 16.9),
(8, 8, 5, '2026-I', 18.7);

INSERT INTO support_tickets (ticket_id, customer_id, created_at, issue_type, status, priority, resolution_time_hours) VALUES
(1, 1, '2026-06-01 09:15:00', 'Database connection', 'Open', 'High', NULL),
(2, 2, '2026-06-03 14:40:00', 'Invoice question', 'Closed', 'Low', 4.5),
(3, 4, '2026-06-04 11:05:00', 'Server performance', 'In Progress', 'High', NULL),
(4, 5, '2026-06-07 16:30:00', 'Login problem', 'Closed', 'Medium', 2.0),
(5, 7, '2026-06-10 10:20:00', 'Data export', 'Open', 'Medium', NULL),
(6, 8, '2026-06-12 08:45:00', 'Product warranty', 'Open', 'Low', NULL);
