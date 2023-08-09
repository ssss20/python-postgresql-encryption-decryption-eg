ALTER TABLE client_credentials
ADD COLUMN encrypted_clientname TEXT,
ADD COLUMN encrypted_password TEXT,
ADD COLUMN encrypted_email TEXT;

UPDATE client_credentials
SET encrypted_clientname = pgp_sym_encrypt(clientname, 'AES_key_name'),
encrypted_password = pgp_sym_encrypt(password,'AES_key_pass'),
encrypted_email = pgp_sym_encrypt(email, 'AES_key_email')

