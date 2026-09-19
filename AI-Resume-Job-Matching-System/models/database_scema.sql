CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150),
    email VARCHAR(150),
    resume_filename VARCHAR(255) NOT NULL,
    resume_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_candidate_email
ON candidates(email);

CREATE INDEX IF NOT EXISTS idx_resume_filename
ON candidates(resume_filename);

CREATE TABLE IF NOT EXISTS matching_results (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id)
        ON DELETE CASCADE,
    job_description TEXT NOT NULL,
    tfidf_score DECIMAL(5,2),
    semantic_score DECIMAL(5,2),
    final_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_final_score
ON matching_results(final_score DESC);






























