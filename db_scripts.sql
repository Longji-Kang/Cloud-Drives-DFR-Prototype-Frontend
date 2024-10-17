CREATE TABLE users(
    username VARCHAR(16) PRIMARY KEY,
    pass CHAR(64),
    salt CHAR(10)
)