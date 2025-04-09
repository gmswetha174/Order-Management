import configparser
import os

class DBPropertyUtil:
    @staticmethod
    def get_connection_string(property_file):
        config = configparser.ConfigParser()
        
        # Get the absolute path to the property file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        property_path = os.path.join(current_dir, "..", property_file)
        
        config.read(property_path)
        
        if 'database' in config:
            db_config = config['database']
            return {
                'host': db_config.get('host', 'localhost'),
                'port': db_config.get('port', '3306'),
                'database': db_config.get('database', 'OrderManagementSystem'),
                'user': db_config.get('username', 'root'),
                'password': db_config.get('password', '')
            }
        else:
            raise Exception("Database configuration not found in property file")