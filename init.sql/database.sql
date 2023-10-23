-- Use the "ecommerce" database
USE ecommerce;

-- Create the "User" table
CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role ENUM('customer', 'admin') NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    avatar VARCHAR(255)
);

-- Insert data into the "User" table
INSERT INTO User (name, role, email, password, avatar)
VALUES ('John Doe', 'admin', 'melchor@gmail.com', '1234', 'default_avatar.jpg');
