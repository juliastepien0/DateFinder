from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
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
        profile_data = profile.get_profile_by_user_id(user_id)
        if profile_data:
            print(f"Profile data: {profile_data}")
            self.ids.info.text = f"Profile created for: {profile_data['name']}"
            self.ids.profile_picture.source = profile_data['profile_picture_url']
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
            profile.create_profile(user_id, name, int(age), gender, bio, location, profile_picture_url, interests)
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

class FileChooserPopup(BoxLayout):
    select = ObjectProperty(None)
    dismiss = ObjectProperty(None)

class DateFinder(MDApp):
    is_new_user = False

    def build(self):
        self.icon = 'main_icon.png'
        self.db = database.Database('localhost', 'root', '', 'DateFinder')
        Builder.load_file('WelcomeRegisterAndLoginScreen.kv')
        Builder.load_file('CreateProfileScreen.kv')
        sm = WindowManager()

        sm.add_widget(WelcomeWindow(name='welcome'))
        sm.add_widget(LoginWindow(name='login'))
        sm.add_widget(SignupWindow(name='signup'))
        sm.add_widget(LogDataWindow(name='logdata'))
        sm.add_widget(CreateProfileWindow(name='create_profile'))

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"

        return sm

if __name__ == "__main__":
    DateFinder().run()
