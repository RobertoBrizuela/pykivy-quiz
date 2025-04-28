from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock

from models.trivia_model import TriviaModel

Builder.load_string('''
<TriviaScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        # Marcador de puntuación y vidas (omítelo si ya lo tienes en otro KV)
        Label:
            text: root.score_text
            font_size: '18sp'
            size_hint_y: None
            height: '30dp'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: '32dp'
            spacing: 5
            Image:
                source: root.lives_status[0] if len(root.lives_status) > 0 else ''
                size_hint: None, None
                size: '32dp', '32dp'
            Image:
                source: root.lives_status[1] if len(root.lives_status) > 1 else ''
                size_hint: None, None
                size: '32dp', '32dp'
            Image:
                source: root.lives_status[2] if len(root.lives_status) > 2 else ''
                size_hint: None, None
                size: '32dp', '32dp'

        # Pregunta
        Label:
            id: question_label
            text: root.question_text
            font_size: 28
            size_hint_y: None
            height: '60dp'

        # Opciones
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

        # Botón “Siguiente Trivia”
        Button:
            id: next_btn
            text: "Siguiente Trivia"
            size_hint_y: None
            height: '50dp'
            disabled: not root.question_answered
            on_release: root.load_question()
''')

class TriviaScreen(Screen):
    # Texto en pantalla
    question_text    = StringProperty("Cargando pregunta...")
    option1          = StringProperty("")
    option2          = StringProperty("")
    option3          = StringProperty("")
    option4          = StringProperty("")

    # Lógica de preguntas
    model             = None
    current_category  = None
    correct_answer    = None

    # Puntuación
    correct_answers = NumericProperty(0)
    wrong_answers   = NumericProperty(0)
    score_text      = StringProperty("Correctas: 0 | Incorrectas: 0")

    # Vidas
    lives          = NumericProperty(3)
    lives_status   = ListProperty([])

    # Bandera para habilitar “Siguiente Trivia”
    question_answered = BooleanProperty(False)

    def set_category(self, category):
        self.current_category   = category
        self.model              = TriviaModel(category)
        self.correct_answers    = 0
        self.wrong_answers      = 0
        self.lives              = 3
        self.question_answered  = False
        self.update_score()
        self.update_lives()
        self.load_question()

    def load_question(self, *args):
        # Cada vez que cargamos pregunta, bloqueamos “Siguiente”
        self.question_answered = False

        q_data = self.model.get_next_question()
        if q_data is None:
            self.show_category_complete_popup()
            return

        self.populate_question(q_data)

    def populate_question(self, q_data):
        # Asigna los datos de la pregunta a las propiedades
        self.question_text  = q_data.get("question", "Pregunta no disponible")
        options             = q_data.get("options", [])
        self.correct_answer = q_data.get("answer")
        padded              = options + [""] * 4
        self.option1, self.option2, self.option3, self.option4 = padded[:4]

    def check_answer(self, selected):
        # Evita múltiples clics o si ya no hay vidas
        if self.question_answered or self.lives <= 0:
            return

        self.question_answered = True  # Marca que ya se contestó

        if selected == self.correct_answer:
            self.question_text = "¡Correcto!"
            self.correct_answers += 1
        else:
            self.question_text = f"Incorrecto. La respuesta correcta era: {self.correct_answer}"
            self.wrong_answers += 1
            self.lives -= 1
            self.update_lives()

        self.update_score()

        # Si te quedas sin vidas, popup de Game Over
        if self.lives <= 0:
            self.show_game_over_popup()
            return

        # Avance automático tras 2 segundos
        Clock.schedule_once(lambda dt: self.load_question(), 1.5)

    def update_score(self):
        self.score_text = f"Correctas: {self.correct_answers} | Incorrectas: {self.wrong_answers}"

    def update_lives(self):
        # Actualiza lista de rutas de iconos según vidas
        self.lives_status = [
            "assets/heart.png"   if i < self.lives else
            "assets/noheart.png"
            for i in range(3)
        ]

    def show_game_over_popup(self):
        popup = ModalView(size_hint=(0.8, 0.4), background_color=(0, 0, 0, 0.7))
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        label  = Label(text="¡Juego terminado!\nSin vidas restantes.", font_size='20sp', color=(1,1,1,1))
        btn    = Button(text="Volver a Inicio", size_hint_y=None, height='40dp')
        layout.add_widget(label)
        layout.add_widget(btn)
        popup.add_widget(layout)
        btn.bind(on_release=lambda *args: self._on_game_over(popup))
        popup.open()

    def _on_game_over(self, popup):
        popup.dismiss()
        self.manager.current = 'home'

    def show_category_complete_popup(self):
        popup = ModalView(size_hint=(0.8, 0.4), background_color=(0, 0, 0, 0.7))
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        label  = Label(text="¡Terminaste todas las preguntas de esta categoría!", font_size='22sp', color=(1,1,1,1))
        btn    = Button(text="Elegir otra categoría", size_hint_y=None, height='40dp')
        layout.add_widget(label)
        layout.add_widget(btn)
        popup.add_widget(layout)
        btn.bind(on_release=lambda *args: self._on_category_complete(popup))
        popup.open()

    def _on_category_complete(self, popup):
        popup.dismiss()
        self.manager.current = 'home'
