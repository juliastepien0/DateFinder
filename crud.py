from data_layer.database import Database
from data_layer.models import User, UserProfile

def delete_user_and_profiles(user_id):
    profile_model.delete_profile_by_user_id(user_id)
    user_model.delete_user(user_id)
    deleted_user_data = user_model.get_user_by_id(user_id)
    if deleted_user_data:
        print(f"Usunięty użytkownik dalej istnieje: {deleted_user_data}")
    else:
        print(f"Użytkownik o user_id {user_id} został usunięty.")



host = 'localhost'
user = 'root'
password = ''
database = 'DateFinder'

db = Database(host, user, password, database)

user_model = User(db)
profile_model = UserProfile(db)

# Create uzytkownik:
# user_model.create_user('igorbebenek@example.com', 'tuturu')
# user_model.create_user('test2@example.com', 'password456')

# Read id:
# user_data = user_model.get_user_by_id(1)
# if user_data:
#     print("User przez ID:", user_data)
# else:
#     print("Użytkownik o user_id 1 nie został znaleziony.")

# Read email:
# user_data = user_model.get_user_by_email('test2@example.com')
# if user_data:
#     print("User przez Email:", user_data)
# else:
#     print("User o email 'test2@example.com' nie został znaleziony.")

# Create profil:
profile_model.create_profile(5, 'John Doe', 30, 'Male', 'Bio example', 'New York')
profile_model.create_profile(6, 'Jane Smith', 28, 'Female', 'Another bio', 'Los Angeles')

# Read:
# profile_data = profile_model.get_profile_by_id(1)
# if profile_data:
#     print("Profil przez ID:", profile_data)
# else:
#     print("Profil o profile_id 1 nie został znaleziony.")

# Update uzytkownika:
# user_model.update_user(1, email='newemail@example.com', password='newpassword123')
# updated_user_data = user_model.get_user_by_id(1)
# print("Zaktualizowany user:", updated_user_data)

# Update profilu:
# profile_model.update_profile(1, name='John Updated', age=31, bio='Updated bio', location='Chicago')
# updated_profile_data = profile_model.get_profile_by_id(1)
# print("Zaktualizowany profil:", updated_profile_data)

# Delete profilu i uzytkownika:
# delete_user_and_profiles(1)
# delete_user_and_profiles(2)


# read wszystkie profile
all_profiles = profile_model.get_profiles()
print("Wszystkie profile:", all_profiles)

db.close()
