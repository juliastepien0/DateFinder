from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import data_layer.database as database
import data_layer.models as models

class WindowManager(ScreenManager):
    pass

class WelcomeWindow(Screen):
    pass

class LoginWindow(Screen):
    def validate(self):
        email = self.ids.email.text
        password = self.ids.pwd.text

        if email and password:
            user = models.User(MDApp.get_running_app().db)
            user_data = user.login_user(email, password)
            if user_data:
                print(f"User {email} logged in successfully with password: {password}")
                MDApp.get_running_app().root.current = 'logdata'
            else:
                print("Invalid email or password")
        else:
            print("Please fill in all fields")

class SignupWindow(Screen):
    def signupbtn(self):
        email = self.ids.email.text
        password = self.ids.pwd.text
        name = self.ids.name2.text

        if email and password and name:
            user = models.User(MDApp.get_running_app().db)  # Poprawne odwołanie do instancji aplikacji
            user.create_user(email, password)
            print(f"User {email} registered successfully with password: {password}")
            MDApp.get_running_app().root.current = 'login'
        else:
            print("Please fill in all fields")

class LogDataWindow(Screen):
    pass

class DateFinder(MDApp):
    def build(self):
        self.icon = 'main_icon.png'
        self.db = database.Database('localhost', 'root', '...', 'DateFinder')
        Builder.load_file('WelcomeRegisterAndLoginScreen.kv')
        sm = WindowManager()

        sm.add_widget(WelcomeWindow(name='welcome'))
        sm.add_widget(LoginWindow(name='login'))
        sm.add_widget(SignupWindow(name='signup'))
        sm.add_widget(LogDataWindow(name='logdata'))

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"

        return sm

if __name__ == "__main__":
    DateFinder().run()
