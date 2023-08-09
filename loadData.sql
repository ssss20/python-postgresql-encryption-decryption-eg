SET timezone TO 'GMT';
SET datestyle = dmy;	
COPY client_credentials(client_id, clientname, password, email, created_on)
FROM '<DIR_PATH>\client_data.csv'
DELIMITER ','
CSV HEADER;
