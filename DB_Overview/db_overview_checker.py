import pymysql



host_ip = input("Please enter server IP-address: ")
host_port = int(input("Please enter server Port: "))
host_user = input("Please enter user: ")
host_password = input("Please enter password: ")


# Connection later
def connection():  
    conn=pymysql.connect(
        host=host_ip, 
        port=host_port, user=host_user, 
        password=host_password 
    )
    return conn 


def schema():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT schema_name FROM information_schema.SCHEMATA;")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def table(schema_name):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SHOW tables FROM `{}`;".format(schema_name))
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def columns(schema_name, table_name):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SHOW COLUMNS FROM `{}`.`{}`;".format(schema_name, table_name))
    header = cursor.fetchall()
    conn.commit()
    conn.close()
    return header

# Get a list of available schemas
available_schemas = schema()
print("Available schemas:")
for row in available_schemas:
    print(row[0])

# Prompt the user to select a schema
selected_schema = input("Enter the name of the schema: ")

# Get a list of tables in the selected schema
available_tables = table(selected_schema)
print("Tables in schema '{}':".format(selected_schema))
for row in available_tables:
    print(row[0])

# Prompt the user to select a table
selected_table = input("Enter the name of the table: ")

# Get the columns of the selected table
table_columns = columns(selected_schema, selected_table)
print("Columns in table '{}.{}':".format(selected_schema, selected_table))
for row in table_columns:
    print(row[0])
