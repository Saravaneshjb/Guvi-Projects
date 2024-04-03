import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from mysql.connector import FieldType
import pandas as pd
import logging

class Dataload:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'database': 'youtube_data_harvesting'
        }

    def create_connection(self):
        """ Create a connection to MySQL database """
        try:
            conn = mysql.connector.connect(**self.db_config)
            if conn.is_connected():
                print('Connected to MySQL database')
                logging.info('Connected to MySQL database')
                return conn
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            logging.error(f"Error connecting to MySQL database: {e}")
            return None

    def close_connection(self, conn):
        """ Close connection to MySQL database """
        if conn.is_connected():
            conn.close()
            print('Connection to MySQL database closed')
            logging.info('Connection to MySQL database closed')

    def execute_query(self, conn, query):
        """ Execute SQL query """
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            print("Query executed successfully")
            logging.info("Query executed successfully")
        except Error as e:
            print(f"Error executing query: {e}")
            logging.error(f"Error executing query: {e}")

    def load_df(self, df_data,df_name):
        try:
            conn = self.create_connection()
            if conn:
                # Convert DataFrame to list of tuples
                data = [tuple(row) for row in df_data.values]
                # print(data)
                # Define the INSERT INTO query
                query = f"INSERT INTO {df_name} ({', '.join(df_data.columns)}) VALUES ({', '.join(['%s'] * len(df_data.columns))})"
                print('The insert query being executed is : ',query)
                logging.info(f'The insert query being executed is : {query}')
                # Execute the query
                cursor = conn.cursor()
                cursor.executemany(query, data)
                conn.commit()
                print("Data loaded successfully")
                logging.info("Data loaded successfully")
        finally:
            self.close_connection(conn)



# if __name__ == "__main__":
#     # Sample DataFrame
#     df = pd.DataFrame({
#         'column1': [1, 2, 3],
#         'column2': ['A', 'B', 'C']
#     })
#     dl = Dataload()
#     dl.channel_load(df)
