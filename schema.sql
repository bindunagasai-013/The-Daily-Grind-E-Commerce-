DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    price REAL
);

INSERT INTO products (name, description, price) VALUES
("Espresso Beans", "Strong dark roast", 16.99),
("Cold Brew Blend", "Smooth low acidity", 15.99),
("French Press", "Brewer equipment", 29.99);
