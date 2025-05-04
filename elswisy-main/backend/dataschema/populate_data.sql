-- Insert sample categories
INSERT INTO categories (name, description) VALUES
('Clothes', 'Fashionable clothing items for all occasions'),
('Bags', 'Stylish bags and accessories'),
('Footwear', 'Comfortable and trendy footwear'),
('Accessories', 'Fashion accessories and jewelry'),
('Electronics', 'Modern electronic devices and gadgets');

-- Insert sample products
INSERT INTO products (name, description, price, stock, category_id, image_path) VALUES
-- Clothes
('Classic White T-Shirt', 'Comfortable cotton t-shirt perfect for everyday wear', 19.99, 50, 1, 'clothes/white_tshirt.jpg'),
('Blue Denim Jeans', 'Classic fit blue jeans with comfortable stretch', 59.99, 30, 1, 'clothes/blue_jeans.jpg'),

-- Bags
('Urban Backpack', 'Spacious backpack with laptop compartment', 45.99, 25, 2, 'bags/urban_backpack.jpg'),
('Leather Tote Bag', 'Elegant leather tote perfect for work', 79.99, 15, 2, 'bags/leather_tote.jpg'),

-- Footwear
('Running Sneakers', 'Lightweight and comfortable running shoes', 89.99, 40, 3, 'footwear/running_sneakers.jpg'),
('Classic Leather Boots', 'Durable leather boots for all occasions', 129.99, 20, 3, 'footwear/leather_boots.jpg'),

-- Accessories
('Silver Watch', 'Elegant silver watch with leather strap', 149.99, 15, 4, 'accessories/silver_watch.jpg'),
('Leather Belt', 'Classic brown leather belt', 34.99, 35, 4, 'accessories/leather_belt.jpg'),

-- Electronics
('Wireless Earbuds', 'High-quality wireless earbuds with noise cancellation', 129.99, 30, 5, 'electronics/wireless_earbuds.jpg'),
('Smart Watch', 'Feature-rich smartwatch with health tracking', 199.99, 20, 5, 'electronics/smart_watch.jpg');

-- Insert a sample user
INSERT INTO users (username, password, email, name) VALUES
('testuser', 'password123', 'test@example.com', 'Test User'); 