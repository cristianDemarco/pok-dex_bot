import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEXTS = {
    "IT":{
        "POKEDEX_RETURN_MESSAGE" : f"""
            <name> N°<id>\n
            Tipo: <types>"\n
            Descrizione: {pokemon.description}
        """
    }
}

def translate(message, language: str = 'IT', data: dict = None):
    translation = TEXTS[language][message]
    if data:
        for key in data:
            translation.replace(f'<{key}>', data[key])