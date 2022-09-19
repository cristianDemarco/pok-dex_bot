import requests
from flask import Flask
from flask import Response
from flask import request
from functions import scrap_previous_next_pokemon
from main import search_pokemon_info

TOKEN = '5783232042:AAEVoD_NrIz5oyCfdqttcMb-Qrv5dxFh85Y'
app = Flask(__name__)


def tel_parse_message(message):
    print('message-->', message)
    try:
        try:
            chat_id = message['callback_query']['message']['chat']['id']
            txt = message['callback_query']['data']
            message_id = message['callback_query']['message']['message_id']
            chat_type = message['callback_query']['message']['chat']['type']
        except:
            chat_id = message['message']['chat']['id']
            txt = message['message']['text']
            message_id = message['message']['message_id']
            chat_type = message['message']['chat']['type']

        print('message-id -->', message_id)
        print('chat_id -->', chat_id)
        print('txt -->', txt)
        print('group_type -->', chat_type)

        return chat_id, txt, message_id, chat_type

    except Exception as e:
        print(f'{e} --- tel_parse_message function')


def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(url, json=payload)

    return r


def tel_send_image(chat_id, txt, message_id):
    pokemon = txt.strip().lower()
    try:
        message, image_link, pokemon_url = search_pokemon_info(pokemon)
        previous_next_pokemon = scrap_previous_next_pokemon(pokemon_url)

        url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'

        payload = {
            'chat_id': chat_id,
            'photo': image_link,
            'caption': message,
            'reply_to_message_id': message_id,
            'reply_markup': {
                'inline_keyboard': [[
                    {
                        'text': f'< {previous_next_pokemon[1]} {previous_next_pokemon[2]}',
                        'callback_data': previous_next_pokemon[1].lower()
                    },
                    {
                        'text': f'{previous_next_pokemon[4]} {previous_next_pokemon[5]} >',
                        'callback_data': previous_next_pokemon[4].lower()
                    }],
                    [{
                        'text': 'Visita il sito per maggiori dettagli',
                        'url': f'https://wiki.pokemoncentral.it/{pokemon}'
                    }]]
            }
        }

        r = requests.post(url, json=payload)
        return r
    except Exception as e:
        print(f'{e} --- tel_send_image function')
        tel_send_message(chat_id, f'Mi dispiace, non sono riuscito a trovare {txt} nel pokédex')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, txt, message_id, chat_type = tel_parse_message(msg)
        if txt == '/help':
            tel_send_message(chat_id,
                             "Questo bot ti permette di cercare un pokémon all'interno del pokèdex fornendoti le "
                             "informazioni più importanti.\nDigita '/pokèmon' seguito dal nome del pokémon che stavi "
                             "cercando. Ad esempio, '/pokèmon chimchar'.\nNella chat privata sarà necessario digitare esclusivamente il nome.")
        else:
            if chat_type == 'supergroup':
                if '/pokédex' in txt:
                    txt = txt.replace('/pokédex', ' ').strip()
                    tel_send_image(chat_id, txt, message_id)
            elif chat_type == 'private':
                tel_send_image(chat_id, txt, message_id)

    return Response('ok', status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
