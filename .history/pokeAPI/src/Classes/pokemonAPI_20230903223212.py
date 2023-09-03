import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pokemon import Pokemon

class PokemonAPI:
    
    def __init__(self) -> None:
        self.data = None
        self.species_data = None

    def get_api_data(self, pokemon : str) -> None:
        data_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        species_data_response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}")
        
        if data_response.status_code == 200 and species_data_response.status_code == 200:
            self.data = data_response.json()
            self.species_data = species_data_response.json()

    def elaborate_api_data(self) -> None:
        
        name = self.data["name"].capitalize()
        id = self.data["id"]

        photo_link = self.data["sprites"]["other"]["official-artwork"]["front_default"]
        photo = photo_link.replace("PokeAPI/sprites", "cristianDemarco/PokeAPI_sprites")

        types = []
        
        for element in self.data["types"]:
            self.types.append(element["type"]["name"])

        descriptions = self.species_data["flavor_text_entries"]

        for element in descriptions:
            if element["language"]["name"] == "it":
                description = element["flavor_text"]
                break

        return Pokemon(name, id, photo, types, description)
                
    def get_photo(self):
        
            

    