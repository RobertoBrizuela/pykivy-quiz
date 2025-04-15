# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.home import HomeScreen
from screens.trivia import TriviaScreen
from kivy.lang import Builder
Builder.load_file("assets/design.kv")

class TriviaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(TriviaScreen(name="trivia"))
        return sm

if __name__ == '__main__':
    TriviaApp().run()
