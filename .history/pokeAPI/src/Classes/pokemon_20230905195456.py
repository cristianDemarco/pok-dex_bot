from typing import List

class Pokemon:
    
    def __init__(self, name : str = "Undefined", id : str = "Undefined", generation : str = "Undefined", is_legendary : bool = False, photo : str = "Undefined", types : List = [], description : str = "Undefined") -> None:
        self.name = name
        self.id = id
        self.generation = generation
        self.is_legendary = is_legendary
        self.photo = photo
        self.types = types
        self.description = description
        self.variety = variety
            

    