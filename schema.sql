CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    review_date DATE,
    rating_overall FLOAT,
    rating_taste FLOAT,
    rating_env FLOAT,
    rating_service FLOAT,
    rating_value FLOAT,
    content TEXT,
    review_year INTEGER DEFAULT 2025,
    source VARCHAR(50) DEFAULT 'screenshot',
    image_path TEXT,
    source_filename TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(username, content)
);
