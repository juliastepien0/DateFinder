from data_layer.database import Database

class User:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, email, password):
        query = "INSERT INTO Users (email, user_password) VALUES (%s, %s)"
        self.db.execute_query(query, (email, password))

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM Users WHERE user_id = %s"
        return self.db.fetchone(query, (user_id,))

    def get_user_by_email(self, email):
        query = "SELECT * FROM Users WHERE email = %s"
        return self.db.fetchone(query, (email,))

    def update_user(self, user_id, email=None, password=None):
        query = "UPDATE Users SET email = %s, user_password = %s WHERE user_id = %s"
        self.db.execute_query(query, (email, password, user_id))

    def delete_user(self, user_id):
        query = "DELETE FROM Users WHERE user_id = %s"
        self.db.execute_query(query, (user_id,))

    #logowanie
    def login_user(self, email, password):
        query = "SELECT * FROM Users WHERE email = %s AND user_password = %s"
        return self.db.fetchone(query, (email, password))

class UserProfile:
    def __init__(self, db: Database):
        self.db = db

    def create_profile(self, user_id, name, age, gender, bio, location):
        query = """INSERT INTO User_profiles (user_id, user_name, age, gender, bio, location)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        self.db.execute_query(query, (user_id, name, age, gender, bio, location))

    def get_profile_by_id(self, profile_id):
        query = "SELECT * FROM User_profiles WHERE profile_id = %s"
        return self.db.fetchone(query, (profile_id,))

    def get_profiles(self):
        query = "SELECT * FROM User_profiles"
        return self.db.fetchall(query)

    def update_profile(self, profile_id, name=None, age=None, gender=None, bio=None, location=None):
        query = """UPDATE User_profiles SET user_name = %s, age = %s, gender = %s, bio = %s, location = %s 
                   WHERE profile_id = %s"""
        self.db.execute_query(query, (name, age, gender, bio, location, profile_id))

    def delete_profile(self, profile_id):
        query = "DELETE FROM Profiles WHERE profile_id = %s"
        self.db.execute_query(query, (profile_id,))

    def delete_profile_by_user_id(self, user_id):
        query = "DELETE FROM User_profiles WHERE user_id = %s"
        self.db.execute_query(query, (user_id,))

class Photo:
    def __init__(self, db: Database):
        self.db = db

    def add_photo(self, profile_id, url):
        query = "INSERT INTO Photos (profile_id, url) VALUES (%s, %s)"
        self.db.execute_query(query, (profile_id, url))

    def get_photos_by_profile_id(self, profile_id):
        query = "SELECT * FROM Photos WHERE profile_id = %s"
        return self.db.fetchall(query, (profile_id,))

class Preference:
    def __init__(self, db: Database):
        self.db = db

    def set_preference(self, user_id, preferred_gender, preferred_age_min, preferred_age_max, distance_max):
        query = """INSERT INTO Preferences (user_id, preferred_gender, preferred_age_min, preferred_age_max, distance_max)
                   VALUES (%s, %s, %s, %s, %s)"""
        self.db.execute_query(query, (user_id, preferred_gender, preferred_age_min, preferred_age_max, distance_max))

    def get_preference_by_user_id(self, user_id):
        query = "SELECT * FROM Preferences WHERE user_id = %s"
        return self.db.fetchone(query, (user_id,))

class Interaction:
    def __init__(self, db: Database):
        self.db = db

    def create_interaction(self, user_id, target_user_id, interaction_type):
        query = """INSERT INTO Interactions (user_id, target_user_id, interaction_type)
                   VALUES (%s, %s, %s)"""
        self.db.execute_query(query, (user_id, target_user_id, interaction_type))

    def get_interactions_for_user(self, user_id):
        query = "SELECT * FROM Interactions WHERE user_id = %s OR target_user_id = %s"
        return self.db.fetchall(query, (user_id, user_id))

class Match:
    def __init__(self, db: Database):
        self.db = db

    def create_match(self, user_id_1, user_id_2):
        query = "INSERT INTO Matches (user_id_1, user_id_2) VALUES (%s, %s)"
        self.db.execute_query(query, (user_id_1, user_id_2))

    def get_matches_for_user(self, user_id):
        query = "SELECT * FROM Matches WHERE user_id_1 = %s OR user_id_2 = %s"
        return self.db.fetchall(query, (user_id, user_id))

class Message:
    def __init__(self, db: Database):
        self.db = db

    def create_message(self, match_id, sender_id, receiver_id, content):
        query = """INSERT INTO Messages (match_id, sender_id, receiver_id, content)
                   VALUES (%s, %s, %s, %s)"""
        self.db.execute_query(query, (match_id, sender_id, receiver_id, content))

    def get_messages_for_match(self, match_id):
        query = "SELECT * FROM Messages WHERE match_id = %s"
        return self.db.fetchall(query, (match_id,))

class Subscription:
    def __init__(self, db: Database):
        self.db = db

    def create_subscription(self, user_id, start_date=None, end_date="2999-01-01", subscription_status="inactive"):
        query = """INSERT INTO Subscriptions (user_id, start_date, end_date, subscription_status)
                   VALUES (%s, %s, %s, %s)"""
        self.db.execute_query(query, (user_id, start_date, end_date, subscription_status))

    def get_subscription_by_user_id(self, user_id):
        query = "SELECT * FROM Subscriptions WHERE user_id = %s"
        return self.db.fetchone(query, (user_id,))

    def update_subscription(self, subscription_id, start_date=None, end_date=None, subscription_status=None):
        query = """UPDATE Subscriptions SET start_date = %s, end_date = %s, subscription_status = %s 
                   WHERE subscription_id = %s"""
        self.db.execute_query(query, (start_date, end_date, subscription_status, subscription_id))

class CardInfo:
    def __init__(self, db: Database):
        self.db = db

    def add_card_info(self, subscription_id, expiration_date, safety_code):
        query = """INSERT INTO Card_info (subscription_id, expiration_date, safety_code)
                   VALUES (%s, %s, %s)"""
        self.db.execute_query(query, (subscription_id, expiration_date, safety_code))

    def get_card_info_by_subscription_id(self, subscription_id):
        query = "SELECT * FROM Card_info WHERE subscription_id = %s"
        return self.db.fetchone(query, (subscription_id,))
