from bs4 import BeautifulSoup
import requests

from functions import create_url, scrap_pokemon_name, scrap_pokemon_description, \
    scrap_pokemon_stats, scrap_pokemon_image, print_pokemon_stats, scrap_pokemon_types, scrap_pokemon_weaknesses


def search_pokemon_info(pokemon):
    url = create_url(pokemon)

    try:
        page = requests.get(url)
    except Exception as e:
        print(e)

    soup = BeautifulSoup(page.content, "html.parser")

    pokemon_name = scrap_pokemon_name(soup)
    pokemon_image = scrap_pokemon_image(soup)
    pokemon_types = scrap_pokemon_types(soup)
    pokemon_weaknesses = scrap_pokemon_weaknesses(soup)
    pokemon_description = scrap_pokemon_description(soup)
    pokemon_stats = scrap_pokemon_stats(soup)
    pokemon_stats_str = print_pokemon_stats(pokemon_stats)

    output = f"\n{pokemon_name}" \
             f"\nTipo: {(', '.join(pokemon_types))}" \
             f"\nDebolezze: {(', '.join(pokemon_weaknesses))}" \
             f"\n\n{pokemon_description}" \
             f"\n\n{pokemon_stats_str} "

    return output, pokemon_image, url
