CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    school VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    -- Add other user-related fields as needed
);

CREATE TABLE cork_boards (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    description TEXT,
    starred BOOLEAN DEFAULT false,
    username VARCHAR(50),
    content_type VARCHAR(50),
    content_url VARCHAR(255),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username)
);


CREATE TABLE recently_viewed (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    board_title VARCHAR(255) NOT NULL,
    view_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (board_title) REFERENCES cork_boards(title)
);
