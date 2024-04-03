import mysql.connector
import pandas as pd
import logging

# Function to execute SQL query and fetch results
def execute_query(query):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="youtube_data_harvesting"
        )

        if conn.is_connected():
            # Create a cursor object to execute queries
            cursor = conn.cursor()

            # Execute the SQL query
            cursor.execute(query)

            # Fetch all rows of the result
            rows = cursor.fetchall()

            # Get column names from cursor description
            columns = [col[0] for col in cursor.description]

            # Create a pandas DataFrame from the fetched rows
            df = pd.DataFrame(rows, columns=columns)

            return df

    except mysql.connector.Error as e:
        print("Error executing query:", e)
        logging.error(f"Error executing query: {e}")

    finally:
        # Close the database connection
        if conn.is_connected():
            cursor.close()
            conn.close()

# # Example usage:
# query = "SELECT * FROM your_table"
# result_df = execute_query(query)
# print(result_df)
