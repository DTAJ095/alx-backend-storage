-- Create table users
-- Script should fail if table already exists
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTOINCREMENT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    country ENUM ('US', 'CO', 'TN') DEFAULT 'US' NOT NULL
);