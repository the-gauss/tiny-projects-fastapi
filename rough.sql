SHOW DATABASES ;
use sakila;
SHOW TABLES ;

SHOW TABLES ;
SELECT *
FROM city;

SELECT *
FROM address;

SELECT *
FROM address INNER JOIN city
ON address.city_id = city.city_id
WHERE city.city_id<300
LIMIT 10;

SELECT *
FROM address INNER JOIN city
USING(city_id)
LIMIT 10;

SHOW COLUMNS FROM city;

INSERT INTO city (city, country_id)
VALUES ('Sikar', 5);

SELECT country_id
FROM country LIMIT 5;

SELECT *
FROM city
WHERE country_id=5;

INSERT INTO city VALUES (1000, 'Sikar', 5, NOW());

UPDATE city SET country_id=50 WHERE city='Sikar';
SELECT *
FROM city
WHERE city='sikar';