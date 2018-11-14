from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
 
 
def connect():
    """ Connect to MySQL database """
 
    db_config = read_db_config()
 
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

        if conn.is_connected():
            print('connection established.')
            print_table(cursor,'classroom')
        else:
            print('connection failed.')
 
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()
        print('Connection closed.')


def print_table(cursor,table_name):
    cursor.execute("SELECT * FROM "+table_name) 
    row = cursor.fetchone()
    while row is not None:
        print(row)
        row = cursor.fetchone()



connect()
