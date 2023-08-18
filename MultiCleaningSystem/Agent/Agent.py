# Paquetes para trabajar con agentes
from mesa import Agent, Model
from mesa.model import Model

class Scavenger(Agent):
    def __init__(self, id: int, model: Model) -> None:
        super().__init__(id, model)

        self.value = 'R'
        self.storage = 5
    
class Trash(Agent):
    def __init__(self, id: int, model: Model) -> None:
        super().__init__(id, model)

        self.value = 'T'
        self.detritus = 0

class Wall (Agent):
    def __init__(self, id: int, model: Model) -> None:
        super().__init__(id, model)
        
        self.value = 'X'
