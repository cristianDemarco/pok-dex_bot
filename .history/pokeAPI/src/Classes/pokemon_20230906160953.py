from typing import List

class Pokemon:
    
    def __init__(self, name : str = "Undefined", id : str = "Undefined", generation : str = "Undefined", is_legendary : bool = False, photo : str = "Undefined", types : List = [], description : str = "Undefined", variety : int = 0) -> None:
        self.name = name
        self.id = id
        self.generation = generation
        self.is_legendary = is_legendary
        self.is_mythical =  is_mythical
        self.photo = photo
        self.types = types
        self.description = description
        self.variety = variety
            

    