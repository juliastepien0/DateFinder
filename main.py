import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from data_layer.database import Database
from data_layer.models import User, UserProfile

class DateFinder(App):
    def build(self):
        self.icon = 'main_icon.png'
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.add_widget(Image(source=self.icon))

        # Tworzenie i konfiguracja połączenia z bazą danych
        self.db = Database('localhost', 'root', '', 'DateFinder')
        self.user_model = User(self.db)
        self.profile_model = UserProfile(self.db)

        # Przykładowe operacje na bazie danych
        self.user_model.create_user("test@gmail.com", "123")
        user = self.user_model.get_user_by_email("test@gmail.com")
        print(user)
        self.profile_model.create_profile(user['user_id'], "John Doe", 18, "Male", "hihihi", "Szczecin")

        # Dodawanie przycisku, aby pokazać, że Kivy działa
        self.button = Button(
            text="Click Me",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE',
            background_normal=""
        )
        self.button.bind(on_press=self.button_pressed)
        self.window.add_widget(self.button)

        return self.window

    def button_pressed(self, instance):
        user = self.user_model.get_user_by_email("test@gmail.com")
        print("Button clicked! User data:", user)

    def on_stop(self):
        # Zamknięcie połączenia z bazą danych przy zamykaniu aplikacji
        self.db.close()

if __name__ == "__main__":
    app = DateFinder()
    app.run()
