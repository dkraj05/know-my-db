-- Initialize the database with sample tables and data

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INTEGER,
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending'
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    description TEXT
);

-- Insert sample users
INSERT INTO users (name, email, age, city) VALUES
    ('John Doe', 'john.doe@email.com', 28, 'New York'),
    ('Jane Smith', 'jane.smith@email.com', 34, 'Los Angeles'),
    ('Bob Johnson', 'bob.johnson@email.com', 45, 'Chicago'),
    ('Alice Brown', 'alice.brown@email.com', 29, 'Houston'),
    ('Charlie Wilson', 'charlie.wilson@email.com', 38, 'Phoenix'),
    ('Diana Davis', 'diana.davis@email.com', 31, 'Philadelphia'),
    ('Eve Miller', 'eve.miller@email.com', 26, 'San Antonio'),
    ('Frank Garcia', 'frank.garcia@email.com', 42, 'San Diego');

-- Insert sample products
INSERT INTO products (name, category, price, stock_quantity, description) VALUES
    ('Laptop Pro', 'Electronics', 1299.99, 50, 'High-performance laptop for professionals'),
    ('Wireless Headphones', 'Electronics', 199.99, 100, 'Premium noise-canceling headphones'),
    ('Coffee Maker', 'Appliances', 89.99, 75, 'Automatic drip coffee maker'),
    ('Running Shoes', 'Sports', 129.99, 200, 'Comfortable running shoes for athletes'),
    ('Desk Chair', 'Furniture', 249.99, 30, 'Ergonomic office chair'),
    ('Smartphone', 'Electronics', 699.99, 80, 'Latest model smartphone'),
    ('Water Bottle', 'Sports', 24.99, 150, 'Insulated stainless steel water bottle'),
    ('Backpack', 'Accessories', 59.99, 120, 'Durable travel backpack');

-- Insert sample orders
INSERT INTO orders (user_id, product_name, quantity, price, status) VALUES
    (1, 'Laptop Pro', 1, 1299.99, 'completed'),
    (1, 'Wireless Headphones', 1, 199.99, 'completed'),
    (2, 'Coffee Maker', 2, 89.99, 'pending'),
    (3, 'Running Shoes', 1, 129.99, 'shipped'),
    (4, 'Desk Chair', 1, 249.99, 'completed'),
    (2, 'Smartphone', 1, 699.99, 'processing'),
    (5, 'Water Bottle', 3, 24.99, 'completed'),
    (6, 'Backpack', 1, 59.99, 'shipped'),
    (7, 'Wireless Headphones', 2, 199.99, 'pending'),
    (8, 'Laptop Pro', 1, 1299.99, 'processing'),
    (3, 'Water Bottle', 2, 24.99, 'completed'),
    (4, 'Running Shoes', 1, 129.99, 'shipped'); 