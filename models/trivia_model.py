# models/trivia_model.py
import random

# Ejemplo de preguntas organizadas por categorías
TRIVIA_DATA = {
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

def get_trivia_question(category):
    data = TRIVIA_DATA.get(category, [])
    if not data:
        return None
    return random.choice(data)
