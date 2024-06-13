-- Create table users
-- Script should fail if table already exists

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255)
);
