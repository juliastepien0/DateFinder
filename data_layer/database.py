import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host = host,
                user = user,
                password = password,
                database = database
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
        except Error as e:
            print("Error occurred: ", e)

    def fetchall(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as e:
            print("Error occurred: ", e)

    def fetchone(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Error as e:
            print("Error occurred: ", e)

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")

