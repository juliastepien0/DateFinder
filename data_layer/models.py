from data_layer.database import Database

class User:
    def __int__(self, db:Database):
        self.db = db

    def create_user(self,email,password):
        query = "INSERT INTO Users (email, password) VALUES (%s, %s)"
        self.db.execute_query(query, (email, password))

