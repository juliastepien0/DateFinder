from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
import data_layer.database as database
import data_layer.models as models

class WindowManager(ScreenManager):
    pass

class WelcomeWindow(Screen):
    pass

class LoginWindow(Screen):
    def validate(self):
        identifier = self.ids.identifier.text
        password = self.ids.pwd.text

        if identifier and password:
            user = models.User(MDApp.get_running_app().db)
            user_data = user.login_user(identifier, password)
            if user_data:
                print(f"User {identifier} logged in successfully with password: {password}")
                MDApp.get_running_app().current_user_id = user_data['user_id']
                profile = models.UserProfile(MDApp.get_running_app().db)
                profile_data = profile.get_profile_by_user_id(user_data['user_id'])
                if profile_data:
                    MDApp.get_running_app().root.current = 'logdata'
                else:
                    if MDApp.get_running_app().is_new_user:
                        MDApp.get_running_app().root.current = 'create_profile'
                        MDApp.get_running_app().is_new_user = False
                    else:
                        MDApp.get_running_app().root.current = 'logdata'
            else:
                print("Invalid email/login or password")
        else:
            print("Please fill in all fields")

class SignupWindow(Screen):
    def signupbtn(self):
        email = self.ids.email.text
        password = self.ids.pwd.text
        login = self.ids.login.text

        if email and password and login:
            user = models.User(MDApp.get_running_app().db)
            if user.get_user_by_email(email):
                print("User with this email already exists")
            else:
                user.create_user(email, password, login)
                print(f"User {email} registered successfully with password: {password}")
                MDApp.get_running_app().is_new_user = True
                MDApp.get_running_app().root.current = 'login'
        else:
            print("Please fill in all fields")

class LogDataWindow(Screen):
    def on_enter(self):
        user_id = MDApp.get_running_app().current_user_id
        profile = models.UserProfile(MDApp.get_running_app().db)
        photo = models.Photo(MDApp.get_running_app().db)

        profile_data = profile.get_profile_by_user_id(user_id)
        profile_photos = photo.get_photos_by_user_id(user_id)

        if profile_data:
            self.ids.info.text = f"Profile created for: {profile_data['user_name']}"
            if profile_photos:
                self.ids.profile_picture.source = profile_photos[0]['url']  # Assuming one profile picture for simplicity
            else:
                self.ids.profile_picture.source = ""  # or set a default image
        else:
            print("Profile not found")
class CreateProfileWindow(Screen):
    gender = StringProperty('')
    preferred_gender = StringProperty('')

    def set_gender(self, gender):
        self.gender = gender

    def set_preferred_gender(self, gender):
        self.preferred_gender = gender

    def create_profile(self):
        user_id = MDApp.get_running_app().current_user_id
        name = self.ids.name.text
        age = self.ids.age.text
        gender = self.gender
        bio = self.ids.bio.text
        location = self.ids.location.text
        profile_picture_url = self.ids.profile_picture_url.text
        interests = self.ids.interests.text
        preferred_gender = self.preferred_gender
        preferred_age_min = self.ids.preferred_age_min.text
        preferred_age_max = self.ids.preferred_age_max.text
        distance_max = self.ids.distance_max.text

        if not age.isdigit() or int(age) < 18:
            print("You must be at least 18 years old to create a profile")
            return

        if not preferred_age_min.isdigit() or int(preferred_age_min) < 18:
            print("Please enter a valid minimum preferred age of at least 18")
            return

        if not preferred_age_max.isdigit() or int(preferred_age_max) < int(preferred_age_min):
            print("Please enter a valid maximum preferred age greater than minimum preferred age")
            return

        if not distance_max.isdigit() or int(distance_max) <= 0:
            print("Please enter a valid maximum distance greater than 0")
            return

        if name and age and gender and bio and location:
            profile = models.UserProfile(MDApp.get_running_app().db)
            profile.create_profile(user_id, name, int(age), gender, bio, location, interests)

            photo = models.Photo(MDApp.get_running_app().db)
            if profile_picture_url:
                photo.add_photo(user_id, profile_picture_url)

            preference = models.Preference(MDApp.get_running_app().db)
            preference.set_preference(user_id, preferred_gender, int(preferred_age_min), int(preferred_age_max),
                                      int(distance_max))
            print(f"Profile for user {user_id} created successfully")
            logdata_window = MDApp.get_running_app().root.get_screen('logdata')
            logdata_window.ids.info.text = "Profile has been created"
            MDApp.get_running_app().root.current = 'logdata'
        else:
            print("Please fill in all fields")

    def file_chooser_open(self):
        content = FileChooserPopup(select=self.file_chooser_select, dismiss=self.dismiss_popup)
        self._popup = Popup(title="Choose Profile Picture", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def file_chooser_select(self, selection):
        if selection:
            self.ids.profile_picture_url.text = selection[0]
        self._popup.dismiss()

    def dismiss_popup(self):
        self._popup.dismiss()

class EditProfileWindow(Screen):
    gender = StringProperty('')
    preferred_gender = StringProperty('')

    def set_gender(self, gender):
        self.gender = gender

    def set_preferred_gender(self, gender):
        self.preferred_gender = gender

    def on_enter(self):
        self.load_profile()

    def load_profile(self):
        user_id = MDApp.get_running_app().current_user_id
        profile = models.UserProfile(MDApp.get_running_app().db)
        photo = models.Photo(MDApp.get_running_app().db)
        profile_data = profile.get_profile_by_user_id(user_id)
        if profile_data:
            self.ids.name.text = profile_data['name']
            self.ids.age.text = str(profile_data['age'])
            self.gender = profile_data['gender']
            self.ids.bio.text = profile_data['bio']
            self.ids.location.text = profile_data['location']
            self.ids.interests.text = profile_data['interests']
            photos = photo.get_photos_by_user_id(user_id)
            if photos:
                self.ids.profile_picture_url.text = photos[0]['photo_url']  # Assuming one profile picture for simplicity
        else:
            print("Profile not found")

    def update_profile(self):
        user_id = MDApp.get_running_app().current_user_id
        name = self.ids.name.text
        age = self.ids.age.text
        gender = self.gender
        bio = self.ids.bio.text
        location = self.ids.location.text
        profile_picture_url = self.ids.profile_picture_url.text
        interests = self.ids.interests.text
        preferred_gender = self.preferred_gender
        preferred_age_min = self.ids.preferred_age_min.text
        preferred_age_max = self.ids.preferred_age_max.text
        distance_max = self.ids.distance_max.text

        if not age.isdigit() or int(age) < 18:
            print("You must be at least 18 years old to create a profile")
            return

        if not preferred_age_min.isdigit() or int(preferred_age_min) < 18:
            print("Please enter a valid minimum preferred age of at least 18")
            return

        if not preferred_age_max.isdigit() or int(preferred_age_max) < int(preferred_age_min):
            print("Please enter a valid maximum preferred age greater than minimum preferred age")
            return

        if not distance_max.isdigit() or int(distance_max) <= 0:
            print("Please enter a valid maximum distance greater than 0")
            return

        if name and age and gender and bio and location:
            profile = models.UserProfile(MDApp.get_running_app().db)
            photo = models.Photo(MDApp.get_running_app().db)
            try:
                profile.update_profile(user_id, name, age, gender, bio, location, interests)
                existing_photos = photo.get_photos_by_user_id(user_id)
                if profile_picture_url:
                    if not any(p['photo_url'] == profile_picture_url for p in existing_photos):
                        photo.add_photo(user_id, profile_picture_url)
                print(f"Profile updated for: {name}")
                MDApp.get_running_app().root.current = 'logdata'
            except ValueError as e:
                print(e)
        else:
            print("Please fill in all fields")

class HomeScreen(Screen):
    random_user_picture = StringProperty('')
    random_user_id= NumericProperty()

    def on_enter(self):
        self.load_random_user()

    def load_random_user(self):
        user_id = MDApp.get_running_app().current_user_id
        profile = models.UserProfile(MDApp.get_running_app().db)
        photo = models.Photo(MDApp.get_running_app().db)
        interactions = models.Interaction(MDApp.get_running_app().db)
        excluded_user_ids = [user_id] + interactions.get_interactions_for_user(user_id)
        random_user = profile.get_random_user(excluded_user_ids)

        if random_user is None:
            # Handle case when no new user is available
            self.random_user_picture = 'no_more_users.png'

        else:
            self.random_user_id = random_user['user_id']
            url = photo.get_photos_by_user_id(random_user['user_id'])
            self.random_user_picture = photo.get_photos_by_user_id(random_user['user_id'])[0]['url']

    def swipe_left(self):
        if self.random_user_id is None:
            self.load_random_user()
        else:
            self.add_interaction('not liked')
            self.load_random_user()

    def swipe_right(self):
        if self.random_user_id is None:
            self.load_random_user()
        else:
            self.add_interaction('liked')
            if self.check_match():
                self.add_match()
            self.load_random_user()

    def add_interaction(self, action):
        user_id = MDApp.get_running_app().current_user_id
        interaction = models.Interaction(MDApp.get_running_app().db)
        interaction.create_interaction(user_id, self.random_user_id, action)

    def check_match(self):
        user_id = MDApp.get_running_app().current_user_id
        interaction = models.Interaction(MDApp.get_running_app().db)
        return interaction.check_match(user_id, self.random_user_id)

    def add_match(self):
        user_id = MDApp.get_running_app().current_user_id
        match = models.Match(MDApp.get_running_app().db)
        match.create_match(user_id, self.random_user_id)

class FileChooserPopup(BoxLayout):
    select = ObjectProperty(None)
    dismiss = ObjectProperty(None)

class DateFinder(MDApp):
    is_new_user = False

    def build(self):
        self.icon = 'main_icon.png'
        self.db = database.Database('localhost', 'root', 'julia', 'DateFinder')
        Builder.load_file('WelcomeRegisterAndLoginScreen.kv')
        Builder.load_file('CreateProfileScreen.kv')
        sm = WindowManager()

        sm.add_widget(WelcomeWindow(name='welcome'))
        sm.add_widget(LoginWindow(name='login'))
        sm.add_widget(SignupWindow(name='signup'))
        sm.add_widget(LogDataWindow(name='logdata'))
        sm.add_widget(CreateProfileWindow(name='create_profile'))
        sm.add_widget(HomeScreen(name='home'))

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"

        return sm

if __name__ == "__main__":
    DateFinder().run()
