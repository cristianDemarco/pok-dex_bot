import requests

class Pokemon:
    
    def _init_ (self) -> None:
        self.data = None
        self.species_data = None
        self.name = None
        self.id = None
        self.types = []
        self.description = None


    def get_api_data(self, pokemon : str) -> None:
        data_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        species_data_response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}")
        
        if data_response.status_code == 200 and species_data_response.status_code == 200:
            self.data = data_response.json()
            self.species_data = species_data_response.json()

    def elaborate_api_data(self):
        
        self.name = self.data["name"]
        self.id = self.data["id"]
        
        types_data = self.data["types"]

        for element in types_data:
            self.types.append(element["type"]["name"])

        descriptions = self.species_data["flavor_text_entries"]

        for element in descriptions:
            if element["language"]["name"] == "it":
                self.description = element["flavor_text"]

                break
                
    def get_photo(self):
        photo_link = self.data["sprites"]["other"]["official-artwork"]["front_default"]
        return photo_link.replace("PokeAPI/sprites", "cristianDemarco/PokeAPI_sprites")
            

    