import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEXTS = {
    "IT":{
        "POKEDEX_RETURN_MESSAGE" : f"""
<name> N°<id>
Tipo: <types>\n
Descrizione: <description>
"""
    }
}

def translate(message, language: str = 'IT', data: dict = {}):
    translation = TEXTS[language][message]
    for key in data:
        translation = translation.replace(f'<{key}>', data[key])
    return translation