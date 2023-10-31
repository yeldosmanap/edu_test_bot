CREATE TABLE IF NOT EXISTS questions (
    question_id INT PRIMARY KEY,
    subject_name VARCHAR(255),
    question_text TEXT,
    answer_text TEXT,
    level_id INT,
    explanation_text TEXT,
    FOREIGN KEY (level_id) REFERENCES levels(level_id)
);

CREATE TABLE IF NOT EXISTS levels (
    level_id INT PRIMARY KEY,
    level_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) PRIMARY KEY,
    date_signed_in DATE
);

CREATE TABLE IF NOT EXISTS user_questions (
    question_id INT,
    username VARCHAR(255),
    level_id INT,
    FOREIGN KEY (question_id) REFERENCES questions(question_id),
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (level_id) REFERENCES levels(level_id)
);