\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Sellers FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Transactions FROM 'Transactions.csv' WITH DELIMITER ',' NULL '' CSV
                 
\COPY Carts FROM 'Carts.csv' WITH DELIMITER ',' NULL '' CSV

\COPY ForSaleItems FROM 'ForSaleItems.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Ratings FROM 'Ratings.csv' WITH DELIMITER ',' NULL '' CSV
