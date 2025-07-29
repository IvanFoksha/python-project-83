CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL,
    last_checked TIMESTAMP,
    status_code INTEGER
);


CREATE TABLE checks (
    id SERIAL PRIMARY KEY,
    url_id INTEGER NOT NULL,
    status_code INTEGER,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    created_at  TIMESTAMP NOT NULL,
    FOREIGN KEY (url_id) REFERENCES urls(id) ON DELETE CASCADE
);