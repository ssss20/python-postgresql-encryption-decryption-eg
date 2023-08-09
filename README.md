# python-postgresql-encryption-decryption-eg

Prerequisites:
**POSTGRESQL:**
- Install postgresql-latest version compatible with your Windows version.
- Go to start open pgAdmin4 which is installed with the postgresql.
- Click on Server, it will prompt you to enter your password. Enter the password used for thr superuser postgres while installation.

**Code Editor:**
- Install VS code editor compatible with your Windows version.
- Install extensions Python, Pylance and pgsql in VS code.

**Steps to follow:**
- Open pgAdmin4 login to Server with SUPERUSER postgres and password used during installation.
- Open SQL window and run the create_DB.sql
- Run the SQL files in sql folder in below order in the SQL window:
  1) create_table.sql
  2) loadData.sql
  3) addencryptedcols.sql(the key mentioned is not an actual key, you can replace it with your symmetric encryption key)
  Eg: SET encrypted_clientname = pgp_sym_encrypt(clientname, 'AES_key_name'),-- AES_key_name to be replaced by your encryption key.
  4) dropcols.sql

- Now open VS code editor and follow the below steps:
  1) Clone the Github project to local using GitBash.
  2) git clone https://github.com/ssss20/python-postgresql-encryption-decryption-eg/
  3) Create .env file at the root of project and add below parameters
     POSTGRES_USER='username'
     POSTGRES_PASSWORD='pwd'
     POSTGRES_DB='dbname'
     POSTGRES_HOST='localhost'
     POSTGRES_PORT='port'
     NAME_ENCRYPTION_KEY='your_key_name'
     EMAIL_ENCRYPTION_KEY='your_key_name'
     PWD_ENCRYPTION_KEY='your_key_name'
  4) Replace all the above values with your defined values.
  5) Run createpostgresconn.py in Python terminal.
 
  **Execution Details:**

  - Please make a choice 1)Select Data, 2)Update data: 
  - Option to be entered=1 or 2
  - Option 1: Displays the data of the client_id that was given as input by user.
  - Option 2: Updates the column name selected for the input client_id.

    
    



  
