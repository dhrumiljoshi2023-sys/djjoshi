-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    salary INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Insert sample data
-- INSERT INTO employees (name, salary) VALUES 
--     ('John Doe', 50000),
--     ('Jane Smith', 60000),
--     ('Bob Johnson', 55000);

