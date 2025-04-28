# models/trivia_model.py
import random

# Ejemplo de preguntas organizadas por categorías
datastore = {
    "cultura_general": [
        {
            "question": "¿Quién escribió 'Don Quijote de la Mancha'?",
            "options": ["Miguel de Cervantes", "William Shakespeare", "Gabriel García Márquez", "Pablo Neruda"],
            "answer": "Miguel de Cervantes"
        },
        {
            "question": "¿Cuál es la capital de Francia?",
            "options": ["Londres", "Madrid", "París", "Berlín"],
            "answer": "París"
        }
    ],
    "ciencia": [
        {
            "question": "¿Qué partícula subatómica tiene carga negativa?",
            "options": ["Protón", "Neutrón", "Electrón", "Positrón"],
            "answer": "Electrón"
        },
        {
            "question": "¿Qué planeta es conocido como el planeta rojo?",
            "options": ["Venus", "Marte", "Júpiter", "Saturno"],
            "answer": "Marte"
        }
    ],
    "deportes": [
        {
            "question": "¿Cuántos jugadores conforman un equipo de fútbol en el campo?",
            "options": ["9", "10", "11", "12"],
            "answer": "11"
        },
        {
            "question": "¿En qué deporte se utiliza la pala?",
            "options": ["Tenis", "Pádel", "Bádminton", "Squash"],
            "answer": "Pádel"
        }
    ]
}

class TriviaModel:
    
    # Clase para manejar el flujo de preguntas por categoría.
    # Mantiene un pool de preguntas interno y admite reinicio.
    
    def __init__(self, category: str):
        self.category = category
        self._original_pool = datastore.get(category, [])
        self.reset()

    def get_next_question(self) -> dict or None:
        
        # Devuelve la siguiente pregunta (con opciones y respuesta)
        # o None si no quedan preguntas.
        
        if not self._pool:
            return None
        return self._pool.pop()

    def reset(self) -> None:
        
        # Reinicia el pool de preguntas a su estado original y baraja.
        
        self._pool = self._original_pool.copy()
        random.shuffle(self._pool)
