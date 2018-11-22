from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
 
 
def connect():
    db_config = read_db_config()
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            print('connection established.')
            return conn
        else:
            print('connection failed.')
 
    except Error as error:
        print(error)


def print_table(cursor,table_name):
    cursor.execute("SELECT * FROM "+table_name) 
    row = cursor.fetchone()
    while row is not None:
        print(row)
        row = cursor.fetchone()



