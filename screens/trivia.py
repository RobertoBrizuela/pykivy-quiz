from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

Builder.load_string('''
<TriviaScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        Label:
            id: question_label
            text: root.question_text
            font_size: 28
        BoxLayout:
            orientation: 'vertical'
            spacing: 5
            Button:
                text: root.option1
                on_release: root.check_answer(root.option1)
            Button:
                text: root.option2
                on_release: root.check_answer(root.option2)
            Button:
                text: root.option3
                on_release: root.check_answer(root.option3)
            Button:
                text: root.option4
                on_release: root.check_answer(root.option4)
        Button:
            text: "Siguiente Trivia"
            size_hint_y: None
            height: '50dp'
            on_release: root.load_question()
''')

class TriviaScreen(Screen):
    question_text = StringProperty("Cargando pregunta...")
    option1 = StringProperty("")
    option2 = StringProperty("")
    option3 = StringProperty("")
    option4 = StringProperty("")
    
    # Propiedades para la lógica de preguntas
    current_category = None
    correct_answer = None

    # Propiedades de puntuación
    correct_answers = NumericProperty(0)
    wrong_answers = NumericProperty(0)
    score_text = StringProperty("Correctas: 0 | Incorrectas: 0")
    
    # vidas
    lives = NumericProperty(3)
    lives_status = ListProperty([])

    def set_category(self, category):
        self.current_category = category
        self.correct_answers = 0  # Reinicia marcador
        self.wrong_answers = 0
        self.lives = 3
        self.update_score()
        self.update_lives()
        self.load_question()

    def load_question(self):
        from models.trivia_model import get_trivia_question
        q_data = get_trivia_question(self.current_category)
        if q_data:
            self.question_text = q_data.get("question", "Pregunta no disponible")
            options = q_data.get("options", [])
            self.correct_answer = q_data.get("answer")
            if len(options) >= 4:
                self.option1, self.option2, self.option3, self.option4 = options[:4]
            else:
                self.option1 = options[0] if len(options) > 0 else ""
                self.option2 = options[1] if len(options) > 1 else ""
                self.option3 = options[2] if len(options) > 2 else ""
                self.option4 = options[3] if len(options) > 3 else ""
        else:
            self.question_text = "No hay preguntas disponibles para esta categoría."

    def check_answer(self, selected):
        
        if self.lives <= 0:
            self.show_game_over_popup()
            return
        
        if selected == self.correct_answer:
            self.question_text = "¡Correcto!"
            self.correct_answers += 1
        else:
            self.question_text = f"Incorrecto. La respuesta correcta era: {self.correct_answer}"
            self.wrong_answers += 1
            self.lives -= 1
            self.update_lives()

        self.update_score()

        # Aquí es posible agregar un temporizador para pasar a la siguiente pregunta
        # o un botón para continuar manualmente

    def update_score(self):
        self.score_text = f"Correct: {self.correct_answers} | Wrong: {self.wrong_answers}"
        
    
    def update_lives(self):
        self.lives_status = [
            "assets/heart.png" if i < self.lives else "assets/noheart.png"
            for i in range(3)
        ]
        
    def show_game_over_popup(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        game_over_label = Label(text="¡Juego terminado!\nSin vidas restantes.", font_size='20sp')
        restart_btn = Button(text="Reiniciar", size_hint_y=None, height='40dp')

        layout.add_widget(game_over_label)
        layout.add_widget(restart_btn)

        popup = Popup(title="Game Over",
                    content=layout,
                    size_hint=(0.7, 0.4),
                    auto_dismiss=False)

        restart_btn.bind(on_release=lambda *args: self.restart_game(popup))
        popup.open()



    def restart_game(self, popup):
        # Cierra el popup
        popup.dismiss()
        # Reinicia todo el estado
        self.correct_answers = 0
        self.wrong_answers = 0
        self.lives = 3
        self.update_score()
        self.update_lives()
        # Vuelve a cargar la pantalla de inicio
        self.manager.current = "home"