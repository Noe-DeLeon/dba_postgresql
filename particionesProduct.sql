DROP TABLE product;
CREATE TABLE product(
	id INT,
	product_name VARCHAR(50),
	price DECIMAL(7,2)
) PARTITION BY RANGE (price);

CREATE TABLE particion_product_1 PARTITION OF
product
FOR VALUES FROM (1.00) TO (3000.99);

CREATE TABLE particion_product_2 PARTITION OF
product
FOR VALUES FROM (3001) TO (6000.99);

CREATE TABLE particion_product_3 PARTITION OF
product
FOR VALUES FROM (6001) TO (10000);

ALTER TABLE particion_product_1
ADD CONSTRAINT particion_1_check
CHECK (price >= 1.00 AND price <= 3000.99);

ALTER TABLE particion_product_2
ADD CONSTRAINT particion_2_check
CHECK (price >= 3001 AND price <= 6000.99);

ALTER TABLE particion_product_3
ADD CONSTRAINT particion_3_check
CHECK (price >= 6001 AND price <= 10000);

SELECT COUNT(*) FROM product;
SELECT * FROM particion_product_3;