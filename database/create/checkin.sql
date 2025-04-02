CREATE TABLE checkin (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    customer_id INT NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
    type ENUM('in', 'item', 'room', 'out') NOT NULL,
    item VARCHAR(255),
    details TEXT,
    check_in_at DATETIME NOT NULL
);