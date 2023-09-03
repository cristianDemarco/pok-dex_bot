from typing import List

class Pokemon:
    
    def __init__(self, name : str = "Undefined", id : str = "Undefined", photo : str = "Undefined", types : List = [], description : str = "Undefined") -> None:
        self.name = name
        self.id = id
        self.photo = photo
        self.types = types
        self.description = description
            

    