# Paquetes para trabajar con agentes
from mesa import Agent, Model

class Scavenger(Agent):
    """ Clase heredada de mesa.agent que representa a un robot """
    
    def __init__(self, id: int, model: Model) -> None:
        """ El constructor recibe como parámetros el id del agente y el modelo 
        sobre le cual opera """
        super().__init__(id, model)

        self.value = 'R'
        self.storage = 5

    def step(self):
        """ Este metodo mueve a los robots a la posición más óptima """
        neighbors = self.model.grid.get_neighbors(self.pos, moore = True, include_center = False)  # Regresa un vector

        movements = []
        for agent in neighbors:
            if agent.value == 'T':
                movements.append(agent.pos)

        if len(movements) != 0: # Buscar mejor posibilidad
            self.pos = movements[0]
    
class Trash(Agent):
    """ Clase heredada de mesa.agent que representa una pila de basura """

    def __init__(self, id: int, model: Model) -> None:
        """ El constructor recibe como parámetros el id del agente y el modelo 
        sobre le cual opera """
        super().__init__(id, model)

        self.value = 'T'
        self.detritus = 0

class Wall (Agent):
    """ Clase heredada de mesa.agent que representa una pared u obstaculo"""

    def __init__(self, id: int, model: Model) -> None:
        """ El constructor recibe como parámetros el id del agente y el modelo 
        sobre le cual opera """
        super().__init__(id, model)
        
        self.value = 'X'
