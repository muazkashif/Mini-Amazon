\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Sellers FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);


\COPY Transactions FROM 'Transactions.csv' WITH DELIMITER ',' NULL '' CSV
                 
\COPY Carts FROM 'Carts.csv' WITH DELIMITER ',' NULL '' CSV

\COPY ForSaleItems FROM 'ForSaleItems.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Ratings FROM 'Ratings.csv' WITH DELIMITER ',' NULL '' CSV
