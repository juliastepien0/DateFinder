import datetime
from data_layer.database import Database

class User:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, email, password, login):
        if self.get_user_by_email(email):
            raise ValueError("User with this email already exists")
        query = "INSERT INTO Users (email, user_password, login) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (email, password, login))

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

    def login_user(self, identifier, password):
        query = "SELECT * FROM Users WHERE (email = %s OR login = %s) AND user_password = %s"
        params = (identifier, identifier, password)
        result = self.db.fetchone(query, params)
        if not result:
            raise ValueError("Invalid email/login or password")
        return result

class UserProfile:
    def __init__(self, db: Database):
        self.db = db

    def create_profile(self, user_id, name, age, gender, bio, location, interests=None):
        query = """INSERT INTO User_profiles (user_id, name, age, gender, bio, location, interests)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        self.db.execute_query(query, (user_id, name, age, gender, bio, location, interests))

    def get_profile_by_user_id(self, user_id):
        query = """SELECT u.*, p.* FROM Users u
                   JOIN User_profiles p ON u.user_id = p.user_id
                   WHERE u.user_id = %s"""
        return self.db.fetchone(query, (user_id,))

    def get_profiles(self):
        query = "SELECT * FROM User_profiles"
        return self.db.fetchall(query)

    def update_profile(self, user_id, name=None, age=None, gender=None, bio=None, location=None, interests=None):
        query = """UPDATE User_profiles SET name = %s, age = %s, gender = %s, bio = %s, location = %s, interests = %s
                   WHERE user_id = %s"""
        self.db.execute_query(query, (name, age, gender, bio, location, interests, user_id))

    def delete_profile(self, profile_id):
        query = "DELETE FROM User_profiles WHERE profile_id = %s"
        self.db.execute_query(query, (profile_id,))

    def delete_profile_by_user_id(self, user_id):
        query = "DELETE FROM User_profiles WHERE user_id = %s"
        self.db.execute_query(query, (user_id,))

    def get_random_user(self, excluded_user_ids):
        excluded_ids_str = ','.join(map(str, excluded_user_ids))
        query = f"""
                SELECT * FROM user_profiles 
                WHERE user_id NOT IN ({excluded_ids_str}) 
                ORDER BY RAND() LIMIT 1"""
        return self.db.fetchone(query)

    def update_premium_status(self, user_id, is_premium):
        query = """UPDATE Users SET is_premium = %s WHERE user_id = %s"""
        self.db.execute_query(query, (is_premium, user_id))

class Photo:
    def __init__(self, db: Database):
        self.db = db

    def add_photo(self, user_id, photo_url):
        query = "INSERT INTO photos (user_id, url) VALUES (%s, %s)"
        self.db.execute_query(query, (user_id, photo_url))

    def get_photos_by_user_id(self, user_id):
        query = "SELECT url FROM photos WHERE user_id = %s"
        return self.db.fetchall(query, (user_id,))

    def delete_photo(self, user_id, photo_url):
        query = "DELETE FROM photos WHERE user_id = %s AND url = %s"
        self.db.execute_query(query, (user_id, photo_url))



class Preference:
    def __init__(self, db: Database):
        self.db = db

    def set_preference(self, user_id, preferred_gender, preferred_age_min, preferred_age_max, distance_max):
        query = "INSERT INTO preferences (user_id, preferred_gender, preferred_age_min, preferred_age_max, distance_max) VALUES (%s, %s, %s, %s, %s)"
        self.db.execute_query(query, (user_id, preferred_gender, preferred_age_min, preferred_age_max, distance_max))

    def get_preference_by_profile_id(self, profile_id):
        query = "SELECT * FROM Preferences WHERE profile_id = %s"
        return self.db.fetchone(query, (profile_id,))

    def get_preference_by_user_id(self, user_id):
        query = "SELECT * FROM Preferences WHERE user_id = %s"
        return self.db.fetchone(query, (user_id,))

    def update_preference(self, user_id, preferred_gender, preferred_age_min, preferred_age_max, distance_max):
        query = """UPDATE Preferences SET preferred_gender = %s, preferred_age_min = %s, preferred_age_max = %s, distance_max = %s
                     WHERE user_id = %s"""
        self.db.execute_query(query, (preferred_gender, preferred_age_min, preferred_age_max, distance_max, user_id))

class Interaction:
    def __init__(self, db: Database):
        self.db = db

    def create_interaction(self, user_id, target_user_id, interaction_type):
        query = """INSERT INTO Interactions (user_id, target_user_id, interaction_type)
                   VALUES (%s, %s, %s)"""
        self.db.execute_query(query, (user_id, target_user_id, interaction_type))

    def check_match(self, from_user_id, to_user_id):
        query = """
        SELECT * FROM interactions 
        WHERE user_id = ? AND target_user_id = ? AND interaction_type = 'liked'
        """
        return self.db.fetchone(query, (to_user_id, from_user_id))

    def get_interactions_for_user(self, user_id):
        query = "SELECT * FROM Interactions WHERE user_id = %s"
        return self.db.fetchall(query, (user_id,))

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

    def create_subscription(self, user_id, start_date=None, end_date="2999-01-01", subscription_status="active"):
        if start_date is None:
            start_date = datetime.date.today()
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
