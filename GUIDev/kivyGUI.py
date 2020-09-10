import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
import sqlite3
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '250')


conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS database (username TEXT, password TEXT)")


class LoginPage(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    login_title = ObjectProperty(None)
    real_password = ""

    def validate(self):
        cursor.execute("SELECT * FROM database WHERE username=? AND password=?", (self.username.text,
                                                                                  self.password.text))
        if len(cursor.fetchall()) == 0:
            self.login_title.text = "Login Failed!"
            self.login_title.color = 1, 0, 0.1, 1
        else:
            self.login_title.text = "Login Successful!"
            self.login_title.color = 0, 1, 0.1, 1


class RegisterPage(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    register_title = ObjectProperty(None)

    def validate(self):
        cursor.execute("SELECT * FROM database WHERE username=? AND password=?", (self.username.text,
                                                                                  self.password.text))
        if len(cursor.fetchall()) == 1:
            self.register_title.text = "User Already Exists!"
            self.register_title.color = 1, 0, 0.1, 1
        else:
            cursor.execute("INSERT INTO database VALUES (?, ?)", (self.username.text, self.password.text))
            conn.commit()
            self.register_title.text = "User Created!"
            self.register_title.color = 0, 1, 0.1, 1


class WindowManager(ScreenManager):
    pass


class KrxLS(App):
    def build(self):
        return WindowManager()


if __name__ == "__main__":
    KrxLS().run()