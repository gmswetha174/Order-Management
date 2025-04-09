import mysql.connector
from mysql.connector import Error
from utils.db_property_util import DBPropertyUtil

class DBConnUtil:
    @staticmethod
    def get_connection(property_file='db.properties'):
        try:
            # Get connection properties
            connection_properties = DBPropertyUtil.get_connection_string(property_file)
            
            # Establish connection
            connection = mysql.connector.connect(
                host=connection_properties['host'],
                port=connection_properties['port'],
                database=connection_properties['database'],
                user=connection_properties['user'],
                password=connection_properties['password']
            )
            
            if connection.is_connected():
                print("Successfully connected to the database")
                return connection
                
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            raise
        
    @staticmethod
    def close_connection(connection):
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")