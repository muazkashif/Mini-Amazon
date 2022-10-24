\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Sellers FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV


\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY Transactions FROM 'Transactions.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.transactions_id_seq',
--                          (SELECT MAX(id)+1 FROM Transactions),
--                          false);
                    
\COPY Carts FROM 'Carts.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.carts_id_seq',
--                          (SELECT MAX(id)+1 FROM Carts),
--                          false);

\COPY ForSaleItems FROM 'ForSaleItems.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.forsaleitems_id_seq',
--                          (SELECT MAX(id)+1 FROM ForSaleItems),
--                          false);

\COPY SellerRatings FROM 'SellerRatings.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.sellerratings_id_seq',
--                          (SELECT MAX(id)+1 FROM SellerRatings),
--                          false);

\COPY ProductRatings FROM 'ProductRatings.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.productratings_id_seq',
--                          (SELECT MAX(id)+1 FROM ProductRatings),
--                          false);

\COPY Ratings FROM 'Ratings.csv' WITH DELIMITER ',' NULL '' CSV
