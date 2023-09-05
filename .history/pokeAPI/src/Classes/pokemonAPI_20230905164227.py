import requests
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Classes.pokemon import Pokemon

class PokemonAPI:
    
    def __init__(self) -> None:
        self.data = None
        self.species_data = None

    def get_api_data(self, pokemon : str) -> None:
        data_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}-standard")

        if data_response.status_code != 200:
            data_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")

        species_data_response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}")
        
        if data_response.status_code == 200 and species_data_response.status_code == 200:
            self.data = data_response.json()
            self.species_data = species_data_response.json()


    def elaborate_api_data(self) -> None:

        name = self.data["name"].capitalize().replace("-standard", "")
        
        id = str(self.data["id"])

        photo = self.data["sprites"]["other"]["official-artwork"]["front_default"]
        photo_link = photo.replace("PokeAPI/sprites", "cristianDemarco/PokeAPI_sprites")

        types = []
        
        for type in self.data["types"]:
            type_link = type["type"]["url"]
            data_response = requests.get(type_link).json()
            for element in data_response["names"]:
                if element["language"]["name"] == "it":
                    types.append(element["name"])
                    break

        types = ", ".join(types)

        descriptions = self.species_data["flavor_text_entries"]
        descriptions_set = set(description["flavor_text"] for description in descriptions if description["language"]["name"] == "it")

        description = " ".join(random.choice(descriptions_set))

        return Pokemon(name, id, photo_link, types, description)        
            

    