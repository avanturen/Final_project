import json



class Character:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def get_json(self):
        
        return json.dumps(self.__dict__)

def get_character_by_dictionary(dictionary):
    return Character(dictionary['name'], dictionary['x'], dictionary['y'])
