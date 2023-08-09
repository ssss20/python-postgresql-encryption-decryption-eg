from typing import cast
import psycopg2
import re
from datetime import datetime
import os
from dotenv import load_dotenv
import pytz

load_dotenv()

current_datetime = datetime.now()
namekey=os.getenv("NAME_ENCRYPTION_KEY")
emailkey=os.getenv("EMAIL_ENCRYPTION_KEY")
pwdkey=os.getenv("PWD_ENCRYPTION_KEY")

db_params = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
    }
    # Establish a connection
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()
value = cursor.execute("select created_on from client_credentials where client_id=6")

def validate_name(name):
    # Regular expression pattern to match first name + last name format
    pattern = r"^[A-Za-z]+ [A-Za-z]+$"
    
    
    if re.match(pattern, name):
        return True
    else:
        return False
    
def validate_email(email):
    # Regular expression pattern to match a valid email format
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    if re.match(pattern, email):
        return True
    else:
        return False
def validate_datetime(datetime_string, format="%Y-%m-%d %H:%M:%S"):
    try:
        # Attempt to parse the input string as a datetime
        datetimevalue =datetime.strptime(datetime_string, format)
        if datetimevalue > current_datetime:
            print("Input datetime is greater than or equal to current datetime.")
            return False
        else:
            return True
    except ValueError:
        return False

def update_name_value(column_name, new_value, client_id):

    while True:
        
        if validate_name(new_value):
            print("Valid name format.")
            break
        else:
            print("Invalid name format. Please enter a valid first name + last name.")
        new_value = input("Enter a valid full name (first name last name): ")
    update_query = f"UPDATE client_credentials SET {column_name} = pgp_sym_encrypt(%s,'{namekey}') WHERE client_id = %s"
    cursor.execute(update_query, (new_value, client_id))
    connection.commit()
    
def update_email_value(column_name, new_value, client_id):
    while True:  
        if validate_email(new_value):
            print("Valid email format.")
            break
        else:
            print("Invalid email format. Please enter a valid email address.")
        new_value = input("Enter a valid email address: ")
    update_query = f"UPDATE client_credentials SET {column_name} = pgp_sym_encrypt(%s,'{emailkey}') WHERE client_id = %s"
    cursor.execute(update_query, (new_value, client_id))
    connection.commit()

def update_pass_value(column_name, new_value, client_id):
    update_query = f"UPDATE client_credentials SET {column_name} = pgp_sym_encrypt(%s,'{pwdkey}') WHERE client_id = %s"
    cursor.execute(update_query, (new_value, client_id))
    connection.commit()

def update_datetime_value(column_name, new_value, client_id):
    while True:
        if validate_datetime(new_value):
            print("Valid datetime format.")
            break
        else:
            print("Invalid datetime format. Please enter a valid datetime (YYYY-MM-DD HH:MM:SS).")
        new_value = input("Enter a valid datetime (YYYY-MM-DD HH:MM:SS): ")
    update_query = f"UPDATE client_credentials SET {column_name} = %s WHERE client_id = %s"
    cursor.execute(update_query, (new_value, client_id))
    connection.commit()
def selectData(client_id):
    set_query ="SET timezone TO 'GMT';"
    select_query = "select client_id,pgp_sym_decrypt(encrypted_clientname::bytea, '{}'),pgp_sym_decrypt(encrypted_password::bytea, '{}'),pgp_sym_decrypt(encrypted_email::bytea, '{}'),created_on from client_credentials where client_id= {}".format(namekey,pwdkey,emailkey,client_id)   
    try:
        cursor.execute(set_query)
        cursor.execute(select_query)
        data = cursor.fetchall()
        print(type(data))
        for x in data:
            for index,value in enumerate(x):
                if index == 4:
                    python_datetime = datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
                    gmt_timezone = pytz.timezone('GMT')
                    gmt_datetime = python_datetime.replace(tzinfo=pytz.UTC).astimezone(gmt_timezone)
                    print(gmt_datetime)
                else:
                    print(value)
            # if index == 4:
            #     python_datetime = datetime.strptime(data[index], '%Y-%m-%d %H:%M:%S')
            #     data[index] =python_datetime.timestamp()
            #     print(data[index])
            # else:
            #     print(data[index])
        # for x in data: 
        #     print(x)
    except Exception as e:
        print(e)
    
# Example usage:

option=input("Please make a choice 1)Select Data, 2)Update data: ")
if option == "1":
    client_id = int(input("Enter the Client ID: "))
    selectData(client_id)
elif option == "2":
    choice = input("Choose a column to update (encrypted_clientname, encrypted_password, encrypted_email,created_on): ")
    client_id = int(input("Enter the Client ID: "))
    new_value = input("Enter the new value: ")

    if choice == "encrypted_clientname":
        update_name_value("encrypted_clientname", new_value, client_id)
    elif choice == "encrypted_password":
        update_pass_value("encrypted_password", new_value, client_id)
    elif choice == "encrypted_email":
        update_email_value("encrypted_email", new_value, client_id)
    elif choice == "created_on":
        update_datetime_value("created_on", new_value, client_id)
    else:
        print("Invalid choice")
else:
    print("Invalid choice. Please select 1 or 2.")
# Close the cursor and connection
cursor.close()
connection.close()
