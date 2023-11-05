CREATE TABLE IF NOT EXISTS levels (
                                      level_id SERIAL PRIMARY KEY,
                                      level_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users (
                                     username VARCHAR(255) PRIMARY KEY,
                                     date_signed_in DATE
);

CREATE TABLE IF NOT EXISTS questions (
    question_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(255),
    question_text TEXT,
    answer_text TEXT,
    level_id INT,
    explanation_text TEXT,
    FOREIGN KEY (level_id) REFERENCES levels(level_id)
);

CREATE TABLE IF NOT EXISTS user_questions (
    question_id INT,
    subject_name VARCHAR(255),
    username VARCHAR(255),
    level_id INT,
    FOREIGN KEY (question_id) REFERENCES questions(question_id),
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (level_id) REFERENCES levels(level_id)
);

SELECT q.question_id, q.subject_name, q.question_text, q.answer_text, q.level_id, q.explanation_text
FROM questions q
JOIN levels l ON q.level_id = l.level_id
WHERE q.subject_name = 'Mathematics' -- Replace with the desired subject
AND q.question_id NOT IN (
    SELECT uq.question_id
    FROM user_questions uq
    JOIN users u ON uq.username = u.username
    WHERE u.username = 'eldos_manap' -- Replace with the specific username
);


insert into levels(level_id, level_name) values (1, 'Easy');
insert into levels(level_id, level_name) values (2, 'Medium');
insert into levels(level_id, level_name) values (3, 'Hard');

-- Computer Science Questions
INSERT INTO questions (subject_name, question_text, answer_text, level_id, explanation_text) VALUES
('Computer Science', 'What does "HTTP" stand for in web addresses?', 'HyperText Transfer Protocol', 1, 'HTTP stands for HyperText Transfer Protocol.'),
('Computer Science', 'What is the binary representation of the decimal number 10?', '1010', 1, 'The binary representation of 10 is 1010.'),
('Computer Science', 'What programming language is known for its simplicity and readability, often used for beginners?', 'Python', 1, 'Python is known for its simplicity and readability, making it a popular choice for beginners.'),
('Computer Science', 'In object-oriented programming, what is encapsulation?', 'A process of wrapping data and code together as a single unit', 2, 'Encapsulation is a process of wrapping data and code together as a single unit in object-oriented programming.'),
('Computer Science', 'What does the acronym "SQL" stand for in the context of databases?', 'Structured Query Language', 2, 'SQL stands for Structured Query Language in the context of databases.'),
('Computer Science', 'What is a linked list in data structures?', 'A linear collection of elements where each element points to the next', 2, 'A linked list is a linear collection of elements where each element points to the next in data structures.'),
('Computer Science', 'What is the time complexity of a binary search algorithm in Big O notation?', 'O(log n)', 3, 'The time complexity of a binary search algorithm is O(log n) in Big O notation.'),
('Computer Science', 'What is the purpose of a Virtual Private Network (VPN) in computer networking?', 'To establish a secure connection over an untrusted network', 3, 'The purpose of a VPN in computer networking is to establish a secure connection over an untrusted network.'),
('Computer Science', 'What is the difference between TCP (Transmission Control Protocol) and UDP (User Datagram Protocol)?', 'TCP is connection-oriented and ensures reliable delivery, while UDP is connectionless and may lose data packets', 3, 'TCP is connection-oriented and ensures reliable delivery, while UDP is connectionless and may lose data packets.'),
('Computer Science', 'What is the purpose of the "git merge" command in version control systems?', 'To combine changes from different branches into the current branch', 3, 'The purpose of the "git merge" command in version control systems is to combine changes from different branches into the current branch.');

-- Mathematics Questions
INSERT INTO questions (subject_name, question_text, answer_text, level_id, explanation_text)
VALUES
('Mathematics', 'What is the result of 5 + 3?', '8', 1, 'The result of 5 + 3 is 8.'),
('Mathematics', 'If a rectangle has a length of 6 units and a width of 4 units, what is its area?', '24 square units', 1, 'The area of the rectangle is calculated by multiplying its length and width. In this case, it is 6 * 4 = 24 square units.'),
('Mathematics', 'Solve for x: 2x + 3 = 11.', '4', 1, 'To solve for x, first subtract 3 from both sides to isolate 2x. This gives you 2x = 8. Then, divide both sides by 2 to get x = 4.'),
('Mathematics', 'What is the value of π (pi) to two decimal places?', '3.14', 2, 'The value of π (pi) to two decimal places is approximately 3.14.'),
('Mathematics', 'Solve the quadratic equation: x^2 - 5x + 6 = 0.', 'x = 2 or x = 3', 2, 'The solutions to the quadratic equation x^2 - 5x + 6 = 0 are x = 2 and x = 3.'),
('Mathematics', 'If a circle has a radius of 8 units, what is its circumference?', '16π units or approximately 50.27 units', 2, 'The circumference of a circle can be calculated using the formula C = 2πr, where r is the radius. In this case, C = 2π(8) = 16π units or approximately 50.27 units.'),
('Mathematics', 'Find the derivative of the function f(x) = 3x^2 + 2x - 1.', 'f(x) = 6x + 2', 3, 'The derivative of the function f(x) = 3x^2 + 2x - 1 is f(x) = 6x + 2.'),
('Mathematics', 'What is the value of the factorial of 5 (5!)?', '120', 3, 'The factorial of 5 (5!) is 120.'),
('Mathematics', 'Solve the system of linear equations: 2x + y = 8, 3x - 2y = 1.', 'x = 3, y = 2', 3, 'The solutions to the system of linear equations are x = 3 and y = 2.');

INSERT INTO questions(subject_name, question_text, answer_text, level_id, explanation_text) VALUES
    ('Mathematics', 'What is the result of 5 + 3? (Please provide your answer as a numerical value)', '8', 1, 'The result of 5 + 3 is 8.'),
    ('Mathematics', 'If a rectangle has a length of 6 units and a width of 4 units, what is its area? (Please provide your answer in square units)', '24 square units', 1, 'The area of the rectangle is calculated by multiplying its length and width. In this case, it is 6 * 4 = 24 square units.'),
    ('Mathematics', 'Solve for x: 2x + 3 = 11. (Please provide your answer as a numerical value of x)', '4', 1, 'To solve for x, first subtract 3 from both sides to isolate 2x. This gives you 2x = 8. Then, divide both sides by 2 to get x = 4.'),
    ('Mathematics', 'What is the value of π (pi) to two decimal places? (Please provide your answer as a numerical value)', '3.14', 2, 'The value of π (pi) to two decimal places is approximately 3.14.'),
    ('Mathematics', 'Solve the quadratic equation: x^2 - 5x + 6 = 0. (Please provide your answers as numerical values of x, separated by commas if there are multiple solutions)', 'x1=2, x2=3', 2, 'The solutions to the quadratic equation x^2 - 5x + 6 = 0 are x = 2 and x = 3.'),
    ('Mathematics', 'If a circle has a radius of 8 units, what is its circumference? (Please provide your answer in units of length)', '16π units or approximately 50.27 units', 2, 'The circumference of a circle can be calculated using the formula C = 2πr, where r is the radius. In this case, C = 2π(8) = 16π units or approximately 50.27 units.'),
    ('Mathematics', 'Find the derivative of the function f(x) = 3x^2 + 2x - 1. (Please provide the derivative of the function)', 'f(x) = 6x + 2', 3, 'The derivative of the function f(x) = 3x^2 + 2x - 1 is f(x) = 6x + 2.'),
    ('Mathematics', 'What is the value of the factorial of 5 (5!)? (Please provide the numerical value of the factorial)', '120', 3, 'The factorial of 5 (5!) is 120.'),
    ('Mathematics', 'Solve the system of linear equations: 2x + y = 8, 3x - 2y = 1. (Please provide the values of x and y, separated by a comma)', 'x=3, y=2', 3, 'The solutions to the system of linear equations are x = 3 and y = 2.');


INSERT INTO questions(subject_name, question_text, answer_text, level_id, explanation_text) VALUES
    ('Computer Science', 'What is the output of the following Python code?\n\n```python\nprint(2 + 3)\n``` (Please provide the numerical value of the output)', '5', 1, 'The Python code prints the result of the addition operation 2 + 3, which is 5.'),
    ('Computer Science', 'What is the time complexity of a linear search algorithm? (Please provide the Big O notation)', 'O(n)', 1, 'The time complexity of a linear search algorithm is O(n), where n is the number of elements in the list being searched.'),
    ('Computer Science', 'Explain the concept of Object-Oriented Programming (OOP) in one sentence. (Please provide a concise definition)', 'Object-Oriented Programming is a programming paradigm that organizes code into objects, which are instances of classes, and allows for the encapsulation, inheritance, and polymorphism of data and behavior.', 2, 'Object-Oriented Programming (OOP) is a fundamental programming paradigm that allows for the organization and structuring of code in a modular and reusable manner.'),
    ('Computer Science', 'What is the difference between a stack and a queue in data structures? (Please provide a brief explanation)', 'A stack is a Last-In, First-Out (LIFO) data structure where elements are added and removed from the same end, while a queue is a First-In, First-Out (FIFO) data structure where elements are added at the rear and removed from the front.', 2, 'Stacks and queues are fundamental data structures used in computer science to organize and manage data in various algorithms and applications.'),
    ('Computer Science', 'Explain the purpose of a constructor in object-oriented programming. (Please provide a concise explanation)', 'A constructor is a special method in a class that is automatically called when an object of the class is created, and it is used to initialize the objects attributes and perform any necessary setup.', 3, 'Constructors are essential in object-oriented programming as they ensure that objects are properly initialized and ready for use in a program.');
