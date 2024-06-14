CREATE TABLE new_flipkart_products (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    price INTEGER,
    mrp INTEGER,
    rating INTEGER,
    url TEXT
);

select * from new_flipkart_products;