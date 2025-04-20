-- Tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(10) DEFAULT 'client' CHECK (role IN ('admin', 'client'))
);

-- Tabla de productos
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2),
    stock INT DEFAULT 0,
    image_url VARCHAR(255)
);

-- Tabla de carrito
CREATE TABLE cart (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    product_id INT REFERENCES products(id),
    quantity INT
);

-- Tabla de órdenes
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    total NUMERIC(10, 2),
    status VARCHAR(10) DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- poblar base 

INSERT INTO products (id, name, description, price, stock, image_url) VALUES
(1, 'Laptop', 'Laptop empresarial con procesador i7, 16GB RAM, 512GB SSD', 1200.00, 153, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(2, 'iPhone 13 Pro', 'Smartphone Apple con pantalla Super Retina XDR, 128GB', 999.99, 8, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(3, 'Samsung Galaxy S22', 'Smartphone Android con cámara de 108MP, 256GB', 849.50, 12, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(4, 'Monitor Dell 27\"', 'Monitor QHD de 27 pulgadas con tasa de refresco de 144Hz', 349.99, 20, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(5, 'Teclado Mecánico RGB', 'Teclado gaming mecánico con retroiluminación RGB', 89.99, 30, 'https://example.com/images/teclado-rgb.jpg'),
(6, 'Mouse Inalámbrico Logitech', 'Mouse ergonómico con conexión Bluetooth y 2 años de batería', 59.99, 25, 'https://example.com/images/mouse-logitech.jpg'),
(7, 'Auriculares Sony WH-1000XM4', 'Auriculares inalámbricos con cancelación de ruido, calidad de sonido excepcional', 349.99, 12, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(8, 'Disco Duro Externo 1TB', 'Disco duro portátil USB 3.0, compatible con PC y Mac', 69.99, 18, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(9, 'Tablet Samsung Galaxy Tab S7', 'Tablet con S Pen incluido, pantalla de 11\", 128GB', 499.99, 7, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(10, 'Impresora Multifunción HP', 'Impresora láser con escáner y copiadora, WiFi', 199.99, 5, 'https://example.com/images/impresora-hp.jpg'),
(11, 'Smartwatch Apple Watch Series 7', 'Reloj inteligente con monitor de actividad y ECG', 399.99, 9, 'https://example.com/images/apple-watch.jpg'),
(12, 'Router WiFi 6', 'Router de última generación con soporte para WiFi 6', 129.99, 14, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(13, 'Altavoz Bluetooth JBL', 'Altavoz portátil resistente al agua con 20h de autonomía', 119.99, 22, 'https://example.com/images/altavoz-jbl.jpg'),
(14, 'Cargador Inalámbrico Rápido 15W', 'Base de carga inalámbrica rápida 15W compatible con dispositivos Qi', 34.99, 40, 'https://example.com/images/cargador-inalambrico.jpg'),
(15, 'Webcam HD 1080p', 'Cámara web con micrófono integrado y enfoque automático', 49.99, 17, 'https://example.com/images/webcam-hd.jpg'),
(101, 'Cargador Inalámbrico 15W', 'Cargador inalámbrico rápido 15W, compatible con dispositivos Qi', 34.99, 50, 'https://example.com/images/cargador-inalambrico.jpg'),
(102, 'Auriculares Sony WH-1000XM4', 'Auriculares inalámbricos con cancelación de ruido, sonido premium', 349.99, 20, 'https://example.com/images/auriculares-sony.jpg'),
(103, 'Funda Silicona iPhone 13', 'Funda de silicona protectora para iPhone 13, color negro', 19.99, 150, 'https://example.com/images/funda-iphone-13.jpg'),
(104, 'Protector de Pantalla Samsung Galaxy S22', 'Protector de pantalla de cristal templado para Samsung Galaxy S22', 12.99, 100, 'https://example.com/images/protector-s22.jpg'),
(105, 'Auriculares Bluetooth Samsung Galaxy Buds Pro', 'Auriculares inalámbricos con cancelación de ruido', 199.99, 50, 'https://example.com/images/galaxy-buds-pro.jpg'),
(106, 'Cargador Rápido iPhone 20W', 'Cargador rápido de 20W compatible con iPhone 12 y superiores', 24.99, 80, 'https://example.com/images/cargador-iphone-20w.jpg'),
(107, 'Funda TPU Samsung Galaxy S21', 'Funda protectora de TPU para Samsung Galaxy S21, resistente a caídas', 15.99, 200, 'https://example.com/images/funda-galaxy-s21.jpg'),
(108, 'Power Bank 10000mAh', 'Batería externa portátil de 10000mAh, carga rápida', 29.99, 100, 'https://example.com/images/power-bank-10000.jpg'),
(109, 'Soporte Ajustable para Celular', 'Soporte ajustable para celular, ideal para videollamadas y ver películas', 14.99, 150, 'https://example.com/images/soporte-celular.jpg'),
(110, 'Cable de Carga USB-C a Lightning', 'Cable de carga USB-C a Lightning, 1 metro, compatible con iPhone', 9.99, 300, 'https://example.com/images/cable-iphone-usbc.jpg'),
(1100, 'Cargador Inalámbrico 20W', 'Cargador inalámbrico rápido 20W para dispositivos móviles', 39.99, 150, 'https://example.com/images/cargador-inalambrico-20w.jpg'),
(1101, 'dqw', 'qwq', 23.00, 2, 'http://localhost:5000/admin/products/add'),
(1102, 'dqw', 'qwq', 23.00, 2, 'http://localhost:5000/admin/products/add');