import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEXTS = {
    "IT":{
        "POKEDEX_RETURN_MESSAGE" : f"""
<name> N°<id>
Tipo: <types>
Descrizione: <description>"""
    }
}

def translate(message, language: str = 'IT', data: dict = {}):
    translation = TEXTS[language][message]
    print(data)
    for key in data:
        print(data[key], type(data[key]))
        translation = translation.replace(f'<{key}>', data[key])
    return translation