-- Your SQL goes here

CREATE TABLE user_emails (
    EmailId INT NOT NULL AUTO_INCREMENT,
    Sender VARCHAR(100) NOT NULL,
    SubjectLine TEXT,
    Body TEXT,
    DateOfArrival VARCHAR(100) NOT NULL,
    PRIMARY KEY(EmailId)
);