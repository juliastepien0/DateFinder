import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                print("Successfully connected to the database")
                self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print("Error while connecting to MySQL: ", e)

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            while self.cursor.nextset():
                pass
        except Error as e:
            print("Error occurred: ", e)
            print("Query: ", query)
            print("Params: ", params)

    def fetchall(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            # Ensure all results are read
            while self.cursor.nextset():
                pass
            return results
        except Error as e:
            print("Error occurred: ", e)

    def fetchone(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            while self.cursor.nextset():
                pass
            return result
        except Error as e:
            print("Error occurred: ", e)

    def close(self):
        if self.connection.is_connected():
            while self.cursor.nextset():
                pass
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")
