-- =============================================================
-- mcp-postgres — Database Init Script
-- Database: mcp-demo
-- =============================================================

-- Create database (run separately if it doesn't exist)
-- CREATE DATABASE "mcp-demo";

-- ─────────────────────────────────────────
-- SCHEMA
-- ─────────────────────────────────────────

CREATE TABLE IF NOT EXISTS products (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price    NUMERIC(10, 2) NOT NULL,
    stock    INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    id            SERIAL PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    product_id    INT NOT NULL REFERENCES products(id),
    quantity      INT NOT NULL,
    total_price   NUMERIC(10, 2) NOT NULL,
    status        VARCHAR(50) CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled')),
    ordered_at    TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────
-- MOCK DATA — PRODUCTS
-- ─────────────────────────────────────────

INSERT INTO products (name, category, price, stock) VALUES
('Wireless Mouse',        'Electronics',   29.99,  120),
('Mechanical Keyboard',   'Electronics',   89.99,   45),
('USB-C Hub',             'Electronics',   49.99,   80),
('Laptop Stand',          'Accessories',   39.99,   60),
('Webcam HD 1080p',       'Electronics',   79.99,   30),
('Desk Lamp LED',         'Accessories',   24.99,  200),
('Noise Cancelling Headphones', 'Electronics', 149.99, 18),
('Mousepad XL',           'Accessories',   19.99,  150),
('Monitor 27"',           'Electronics',  399.99,   12),
('Cable Management Kit',  'Accessories',   14.99,   90),
('Ergonomic Chair',       'Furniture',    299.99,    8),
('Standing Desk',         'Furniture',    499.99,    5),
('Bookshelf',             'Furniture',    129.99,   22),
('Desk Organizer',        'Accessories',   34.99,   75),
('HDMI Cable 2m',         'Electronics',   12.99,  300);

-- ─────────────────────────────────────────
-- MOCK DATA — ORDERS
-- ─────────────────────────────────────────

INSERT INTO orders (customer_name, product_id, quantity, total_price, status, ordered_at) VALUES
('Alice Johnson',   1,  2,   59.98, 'delivered',  '2025-01-05 09:15:00'),
('Bob Smith',       7,  1,  149.99, 'delivered',  '2025-01-08 14:30:00'),
('Carol White',     9,  1,  399.99, 'shipped',    '2025-01-12 10:00:00'),
('David Lee',       3,  3,  149.97, 'delivered',  '2025-01-15 11:20:00'),
('Emma Brown',      2,  1,   89.99, 'pending',    '2025-01-18 16:45:00'),
('Frank Wilson',    5,  2,  159.98, 'delivered',  '2025-01-20 08:30:00'),
('Grace Kim',      11,  1,  299.99, 'shipped',    '2025-01-22 13:00:00'),
('Henry Chen',      4,  2,   79.98, 'delivered',  '2025-01-25 09:45:00'),
('Alice Johnson',   6,  3,   74.97, 'delivered',  '2025-01-28 15:10:00'),
('Bob Smith',      12,  1,  499.99, 'pending',    '2025-02-01 10:30:00'),
('Carol White',     8,  4,   79.96, 'delivered',  '2025-02-03 14:00:00'),
('David Lee',      14,  2,   69.98, 'cancelled',  '2025-02-05 11:15:00'),
('Emma Brown',      1,  1,   29.99, 'delivered',  '2025-02-07 09:00:00'),
('Frank Wilson',   15,  5,   64.95, 'shipped',    '2025-02-09 16:30:00'),
('Grace Kim',      10,  3,   44.97, 'pending',    '2025-02-10 12:00:00'),
('Henry Chen',      7,  1,  149.99, 'cancelled',  '2025-02-11 08:45:00'),
('Alice Johnson',   9,  1,  399.99, 'pending',    '2025-02-12 10:15:00'),
('Bob Smith',       3,  2,   99.98, 'shipped',    '2025-02-13 14:30:00'),
('Carol White',    13,  1,  129.99, 'delivered',  '2025-02-14 09:30:00'),
('David Lee',       5,  1,   79.99, 'delivered',  '2025-02-15 11:00:00');
