DROP TABLE client;
CREATE TABLE client(
	id_client INT,
	first_name VARCHAR(45),
	last_name VARCHAR(45),
	adreess VARCHAR(60),
	country VARCHAR(45),
	email VARCHAR(45),
	cellphone VARCHAR(20),
	telephone VARCHAR(20),
	job_title VARCHAR(45),
	gender VARCHAR(10),
	college VARCHAR(200)
) PARTITION BY LIST (LOWER(gender));

CREATE TABLE particion_client_male PARTITION OF
client
FOR VALUES IN ('male');

CREATE TABLE particion_client_female PARTITION OF
client
FOR VALUES IN ('female');

ALTER TABLE particion_client_male
ADD CONSTRAINT particion_male_check
CHECK (gender ILIKE 'male');

ALTER TABLE particion_client_female
ADD CONSTRAINT particion_female_check
CHECK (gender ILIKE 'female');

SELECT COUNT(*) FROM client;
SELECT * FROM particion_client_male