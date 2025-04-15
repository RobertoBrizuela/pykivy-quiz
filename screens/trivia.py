from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder

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
    current_category = None
    correct_answer = None

    def set_category(self, category):
        self.current_category = category
        self.load_question()

    def load_question(self):
        # Se obtienen los datos del modelo (la función lo define en el siguiente módulo)
        from models.trivia_model import get_trivia_question
        q_data = get_trivia_question(self.current_category)
        if q_data:
            self.question_text = q_data.get("question", "Pregunta no disponible")
            options = q_data.get("options", [])
            self.correct_answer = q_data.get("answer")
            if len(options) >= 4:
                self.option1, self.option2, self.option3, self.option4 = options[:4]
            else:
                # En caso de tener menos opciones, se rellenan vacías
                self.option1 = options[0] if len(options) > 0 else ""
                self.option2 = options[1] if len(options) > 1 else ""
                self.option3 = options[2] if len(options) > 2 else ""
                self.option4 = options[3] if len(options) > 3 else ""
        else:
            self.question_text = "No hay preguntas disponibles para esta categoría."

    def check_answer(self, selected):
        if selected == self.correct_answer:
            self.question_text = "¡Correcto!"
        else:
            self.question_text = f"Incorrecto. La respuesta correcta era: {self.correct_answer}"
