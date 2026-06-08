INSERT OR IGNORE INTO admins (username, password_hash)
VALUES (
    'admin',
    'scrypt:32768:8:1$EoWH9UhhnwJQxyse$af98ebb8227eed7887a8d0e0b996b1ea35d7d15f5bb0659e62ff2d436aadcbcaf307aa790d6d45da64667dcfca53c1c842b061dacfa48addbfc9d4e09b08b929'
);

INSERT OR IGNORE INTO students (id, full_name, enrollment_number, email, phone, department, year_level) VALUES
    (1, 'Aarav Mehta', 'ENR2026001', 'aarav.mehta@campus.edu', '9876543210', 'Computer Science', 2),
    (2, 'Diya Sharma', 'ENR2026002', 'diya.sharma@campus.edu', '9876543211', 'Business Administration', 1),
    (3, 'Ishan Rao', 'ENR2026003', 'ishan.rao@campus.edu', '9876543212', 'Electrical Engineering', 3),
    (4, 'Mira Kapoor', 'ENR2026004', 'mira.kapoor@campus.edu', '9876543213', 'Mathematics', 2),
    (5, 'Rohan Verma', 'ENR2026005', 'rohan.verma@campus.edu', '9876543214', 'Computer Science', 4);

INSERT OR IGNORE INTO courses (id, course_code, course_name, department, credit_hours, semester) VALUES
    (1, 'CSC201', 'Data Structures', 'Computer Science', 4, 'Fall'),
    (2, 'BUS101', 'Foundations of Management', 'Business Administration', 3, 'Spring'),
    (3, 'EEE305', 'Digital Systems', 'Electrical Engineering', 4, 'Fall'),
    (4, 'MAT220', 'Linear Algebra', 'Mathematics', 3, 'Summer'),
    (5, 'CSC410', 'Database Systems', 'Computer Science', 4, 'Spring');

INSERT OR IGNORE INTO registrations (student_id, course_id) VALUES
    (1, 1),
    (1, 5),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 1);

