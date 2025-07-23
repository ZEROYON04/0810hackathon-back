-- テーブルの作成
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- 初期データの挿入
INSERT INTO products (name, price) VALUES ('Apple', 1.00) ON CONFLICT (id) DO NOTHING;
INSERT INTO products (name, price) VALUES ('Banana', 0.50) ON CONFLICT (id) DO NOTHING;
INSERT INTO products (name, price) VALUES ('Orange', 0.75) ON CONFLICT (id) DO NOTHING;

-- 新しいユーザーの作成（オプション）
-- CREATE USER app_user WITH PASSWORD 'app_password';
-- GRANT ALL PRIVILEGES ON DATABASE mydatabase TO app_user;