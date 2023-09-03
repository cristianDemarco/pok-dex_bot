import requests

class Pokemon:
    
    def _init_ (self) -> None:
        self.data = None
        self.species_data = None

    def get_api_data(self, pokemon : str) -> None:
        data_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        species_data_response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}")
        
        if data_response.status_code == 200 and species_data_response.status_code == 200:
            self.data = data_response.json()
            self.species_data = species_data_response.json()

    def elaborate_api_data(self):
        
        name = self.data["name"]
        id = self.data["id"]
        
        types = []
        types_data = self.data["types"]

        for element in types_data:
            types.append(element["type"]["name"])

        description = None
        descriptions = self.species_data["flavor_text_entries"]

        for element in descriptions:
            if element["language"]["name"] == "it":
                description = element["flavor_text"]

                break
            
        return f"{name}, {id}, {types}, \n{description}"
    
    def get_photo(self):
        return self.data["sprites"]["front_default"]
            

    