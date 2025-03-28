CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    model_year INTEGER,
    grade INTEGER,
    review TEXT,
    user_id INTEGER REFERENCES users
);