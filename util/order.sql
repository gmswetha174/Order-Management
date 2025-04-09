CREATE DATABASE IF NOT EXISTS OrderManagementSystem;
USE OrderManagementSystem;

CREATE TABLE IF NOT EXISTS User (
    userId INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role ENUM('Admin', 'User') NOT NULL
);

CREATE TABLE IF NOT EXISTS Product (
    productId INT PRIMARY KEY AUTO_INCREMENT,
    productName VARCHAR(100) NOT NULL,
    description TEXT,
    price DOUBLE NOT NULL,
    quantityInStock INT NOT NULL,
    type ENUM('Electronics', 'Clothing') NOT NULL
);

CREATE TABLE IF NOT EXISTS Electronics (
    productId INT PRIMARY KEY,
    brand VARCHAR(100),
    warrantyPeriod INT,
    FOREIGN KEY (productId) REFERENCES Product(productId) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Clothing (
    productId INT PRIMARY KEY,
    size VARCHAR(20),
    color VARCHAR(30),
    FOREIGN KEY (productId) REFERENCES Product(productId) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Orders (
    orderId INT PRIMARY KEY AUTO_INCREMENT,
    userId INT NOT NULL,
    orderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES User(userId) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Order_Product (
    orderId INT,
    productId INT,
    quantity INT NOT NULL,
    PRIMARY KEY (orderId, productId),
    FOREIGN KEY (orderId) REFERENCES Orders(orderId) ON DELETE CASCADE,
    FOREIGN KEY (productId) REFERENCES Product(productId) ON DELETE CASCADE
);

INSERT INTO User (username, password, role) VALUES ('admin1', 'adminpass', 'Admin');
INSERT INTO User (username, password, role) VALUES ('user1', 'userpass', 'User');
INSERT INTO User (username, password, role) VALUES ('admin2', 'securepass', 'Admin');
INSERT INTO User (username, password, role) VALUES ('user2', 'mypassword', 'User');
INSERT INTO User (username, password, role) VALUES ('user3', 'abc123', 'User');
INSERT INTO User (username, password, role) VALUES ('admin3', 'pass1234', 'Admin');
INSERT INTO User (username, password, role) VALUES ('user4', 'pass456', 'User');
INSERT INTO User (username, password, role) VALUES ('user5', 'user789', 'User');
INSERT INTO User (username, password, role) VALUES ('admin4', 'superpass', 'Admin');
INSERT INTO User (username, password, role) VALUES ('user6', 'testpass', 'User');

INSERT INTO Product (productName, description, price, quantityInStock, type) VALUES ('Smartphone', 'Android smartphone', 25000, 50, 'Electronics');
INSERT INTO Product (productName, description, price, quantityInStock, type) VALUES ('Laptop', 'Gaming laptop', 70000, 30, 'Electronics');
INSERT INTO Product (productName, description, price, quantityInStock, type) VALUES ('Headphones', 'Noise-cancelling headphones', 5000, 100, 'Electronics');
INSERT INTO Product (productName, description, price, quantityInStock, type) VALUES ('LED TV', '42 inch Smart LED TV', 35000, 20, 'Electronics');
INSERT INTO Product (productName, description, price, quantityInStock, type) VALUES ('Jeans', 'Blue denim jeans', 1500, 80, 'Clothing');
INSERT INTO Product (productName, description, price, quantityInStock, type) VALUES ('T-shirt', 'Cotton round-neck T-shirt', 600, 200, 'Clothing');
INSERT INTO Product (productName, description, price, quantityInStock, type) VALUES ('Jacket', 'Leather jacket', 3000, 60, 'Clothing');
INSERT INTO Product (productName, description, price, quantityInStock, type) VALUES ('Sneakers', 'Running sneakers', 2500, 40, 'Clothing');
INSERT INTO Product (productName, description, price, quantityInStock, type) VALUES ('Tablet', 'Android tablet', 15000, 25, 'Electronics');
INSERT INTO Product (productName, description, price, quantityInStock, type) VALUES ('Smartwatch', 'Fitness smartwatch', 7000, 35, 'Electronics');

INSERT INTO Electronics (productId, brand, warrantyPeriod) VALUES (1, 'Samsung', 12);
INSERT INTO Electronics (productId, brand, warrantyPeriod) VALUES (2, 'Dell', 24);
INSERT INTO Electronics (productId, brand, warrantyPeriod) VALUES (3, 'Sony', 18);
INSERT INTO Electronics (productId, brand, warrantyPeriod) VALUES (4, 'LG', 12);
INSERT INTO Electronics (productId, brand, warrantyPeriod) VALUES (9, 'Lenovo', 12);
INSERT INTO Electronics (productId, brand, warrantyPeriod) VALUES (10, 'Boat', 6);

INSERT INTO Clothing (productId, size, color) VALUES (5, 'M', 'Blue');
INSERT INTO Clothing (productId, size, color) VALUES (6, 'L', 'White');
INSERT INTO Clothing (productId, size, color) VALUES (7, 'XL', 'Black');
INSERT INTO Clothing (productId, size, color) VALUES (8, '9', 'Grey');

INSERT INTO Orders (userId) VALUES (2);
INSERT INTO Orders (userId) VALUES (4);
INSERT INTO Orders (userId) VALUES (5);
INSERT INTO Orders (userId) VALUES (7);
INSERT INTO Orders (userId) VALUES (10);
INSERT INTO Orders (userId) VALUES (2);
INSERT INTO Orders (userId) VALUES (4);
INSERT INTO Orders (userId) VALUES (5);
INSERT INTO Orders (userId) VALUES (7);
INSERT INTO Orders (userId) VALUES (10);

INSERT INTO Order_Product (orderId, productId, quantity) VALUES (1, 1, 1);
INSERT INTO Order_Product (orderId, productId, quantity) VALUES (1, 5, 2);
INSERT INTO Order_Product (orderId, productId, quantity) VALUES (2, 2, 1);
INSERT INTO Order_Product (orderId, productId, quantity) VALUES (2, 6, 1);
INSERT INTO Order_Product (orderId, productId, quantity) VALUES (3, 3, 3);
INSERT INTO Order_Product (orderId, productId, quantity) VALUES (4, 7, 1);
INSERT INTO Order_Product (orderId, productId, quantity) VALUES (5, 9, 1);
INSERT INTO Order_Product (orderId, productId, quantity) VALUES (6, 4, 1);
INSERT INTO Order_Product (orderId, productId, quantity) VALUES (7, 10, 2);
INSERT INTO Order_Product (orderId, productId, quantity) VALUES (8, 8, 1);
