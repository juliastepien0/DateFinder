import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from data_layer.database import Database
from data_layer.models import User, UserProfile, Match, Message

#kv = Builder.load_file("my.kv")

def main():
    """"
    #połączenie
    db = Database('localhost', 'root', 'password', 'DateFinder')

    user_model = User(db)
    user_model.create_user("test@gmail.com", "123")

    profile_model = UserProfile(db)
    user = user_model.get_user_by_email("test@gmail.com")
    print(user)
    profile_model.create_profile(user['user_id'], "John Doe", '18', 'Male', 'hihihi', 'Szczecin')
    db.close()
    """

class DateFinder(App):
    def build(self):
        self.icon = 'main_icon.png'
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.add_widget(Image(source=self.icon))

        #return kv

if __name__ == "__main__":
    #main()
    app = DateFinder()
    app.run()