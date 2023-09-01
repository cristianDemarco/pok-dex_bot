import bs4
from bs4 import BeautifulSoup
import requests


def create_url(pokemon):
    url = f"https://www.pokemon.com/it/pokedex/{pokemon}"

    return url


def scrap_pokemon_name(soup):
    name = soup.find("div", class_="pokedex-pokemon-pagination-title")
    number = name.span.extract().text.strip()
    name = name.text.strip()

    name = f"{name} {number}"

    return name


def scrap_pokemon_image(soup):
    image = soup.find("img", class_="active")
    image = image["src"]

    return image


def scrap_pokemon_description(soup):
    description_v1 = soup.find("p", class_="version-x active").text.strip()
    description_v2 = soup.find("p", class_="version-y").text.strip()

    pokemon_description = f"Descrizione: \n{description_v1}\n{description_v2}"

    return pokemon_description


def scrap_pokemon_types(soup):
    types = []
    type = soup.find("div", class_="dtm-type")
    type = type.find_all("li")
    for element in type:
        types.append(element.text.strip())

    return types


def scrap_pokemon_weaknesses(soup):
    weaknesses = []
    weakness = soup.find("div", class_="dtm-weaknesses")
    weakness = weakness.find_all("li")
    for element in weakness:
        weaknesses.append(element.text.strip())

    return weaknesses


def scrap_pokemon_stats(soup):
    pokemon_attributes = {}

    pokemon_stats = soup.find("div", class_="pokemon-ability-info color-bg color-lightblue match active")
    pokemon_stats = pokemon_stats.find_all("li")
    for element in pokemon_stats:
        key = element.find("span", class_="attribute-title")
        value = element.find("span", class_="attribute-value")
        if type(key) == bs4.element.Tag and type(value) == bs4.element.Tag:
            if key.text.strip() == "Sesso":
                value = value.find_all("i")
                sexes = []
                if not value:
                    sex = "Sconosciuto"
                else:
                    for s in value:
                        s = str(s)
                        if s == '<i class="icon icon_male_symbol"></i>':
                            sex = "Maschio"
                            sexes.append(sex)
                        elif s == '<i class="icon icon_female_symbol"></i>':
                            sex = "Femmina"
                sexes.append(sex)
                sexes = (', '.join(sexes))
                pokemon_attributes[key.text.strip()] = sexes
            else:
                key = key.text.strip()
                value = value.text.strip()
                pokemon_attributes[key] = value
    return pokemon_attributes


def print_pokemon_stats(pokemon_stats):
    pokemon_stats_str = ""
    for key, value in pokemon_stats.items():
        pokemon_stats_str += key + ': ' + value + "\n"

    return pokemon_stats_str


def scrap_previous_next_pokemon(pokemon_url):
    previous_next_pokemon = []
    page = requests.get(pokemon_url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find("div", class_="pokedex-pokemon-pagination")
    a = div.find_all("a")
    for element in a:
        link_url = element["href"]
        name = element.find("span", class_="pokemon-name hidden-mobile").text.strip()
        number = element.find("span", class_="pokemon-number").text.strip()

        previous_next_pokemon.append(link_url)
        previous_next_pokemon.append(name)
        previous_next_pokemon.append(number)

    return previous_next_pokemon
