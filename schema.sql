CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    join_date TEXT,
    about_me TEXT,
    image BLOB
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    model_year INTEGER,
    grade INTEGER,
    review TEXT,
    user_id INTEGER REFERENCES users,
    image BLOB
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    post_id INTEGER REFERENCES posts,
    comment TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE post_classes (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    title TEXT,
    value TEXT
);

CREATE INDEX idx_post_value ON post_classes (value);
CREATE INDEX idx_post_title ON posts (title);
CREATE INDEX idx_post_model_year ON posts (model_year);
CREATE INDEX idx_post_grade ON posts (grade);
CREATE INDEX idx_post_review ON posts (review);