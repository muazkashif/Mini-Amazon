-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    balance DECIMAL(12,2) NOT NULL,
    date DATE NOT NULL
);

CREATE TABLE Sellers (
    id INT NOT NULL REFERENCES Users(id),
    PRIMARY KEY (id)
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(255) NOT NULL,
    descriptions VARCHAR(8000) UNIQUE NOT NULL,
    images VARCHAR(255) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    rating DECIMAL(3,2),
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE ForSaleItems (
    pid INT NOT NULL REFERENCES Products(id),
    sid INT NOT NULL REFERENCES Sellers(id),
    quantity INT NOT NULL,
    PRIMARY KEY (pid, sid)
);

CREATE TABLE Carts (
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    sid INT NOT NULL REFERENCES Sellers(id),
    quantity INT NOT NULL,
    PRIMARY KEY (uid, sid, pid)
);

CREATE TABLE Transactions (
    uid INT NOT NULL REFERENCES Users(id),
    sid INT NOT NULL REFERENCES Sellers(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL,
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    order_status VARCHAR(255) NOT NULL,
    PRIMARY KEY (uid, sid, pid, time_purchased)
);

CREATE TABLE Ratings (
    uid INT NOT NULL REFERENCES Users(id),
    sid INT NOT NULL REFERENCES Sellers(id),
    pid INT NOT NULL REFERENCES Products(id),
    rating DECIMAL(3,2) NOT NULL,
    review VARCHAR(8000) NOT NULL,
    time_reviewed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    PRIMARY KEY (uid, sid, pid)
);