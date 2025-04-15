from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string('''
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        Label:
            text: "Selecciona una categoría de Trivia"
            font_size: 32
        Button:
            text: "Cultura General"
            on_release: root.select_category("cultura_general")
        Button:
            text: "Ciencia"
            on_release: root.select_category("ciencia")
        Button:
            text: "Deportes"
            on_release: root.select_category("deportes")
''')

class HomeScreen(Screen):
    def select_category(self, category):
        # Al seleccionar, se guarda la categoría elegida y se cambia a la pantalla de trivia
        self.manager.get_screen('trivia').set_category(category)
        self.manager.current = 'trivia'
