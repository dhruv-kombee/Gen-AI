INSERT INTO students (full_name, enrollment_number, email, phone, department, year)
VALUES
    ('Aarav Mehta', 'CSE2024001', 'aarav.mehta@college.edu', '+91 9876543210', 'Computer Science', 2),
    ('Diya Sharma', 'ECE2024007', 'diya.sharma@college.edu', '+91 9876543211', 'Electronics', 1),
    ('Rohan Iyer', 'MBA2024012', 'rohan.iyer@college.edu', '+91 9876543212', 'Business Administration', 3),
    ('Nisha Patel', 'MTH2024019', 'nisha.patel@college.edu', '+91 9876543213', 'Mathematics', 2),
    ('Kabir Singh', 'MEC2024022', 'kabir.singh@college.edu', '+91 9876543214', 'Mechanical Engineering', 4);

INSERT INTO courses (course_code, title, department, credits, capacity)
VALUES
    ('CSE101', 'Programming Fundamentals', 'Computer Science', 4, 60),
    ('CSE220', 'Database Management Systems', 'Computer Science', 3, 45),
    ('ECE110', 'Digital Electronics', 'Electronics', 4, 50),
    ('MAT210', 'Applied Statistics', 'Mathematics', 3, 40),
    ('MGT301', 'Strategic Management', 'Business Administration', 3, 35),
    ('MEC330', 'Thermal Engineering', 'Mechanical Engineering', 4, 30);

INSERT INTO registrations (student_id, course_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 3),
    (3, 5),
    (4, 4),
    (5, 6),
    (2, 4);
