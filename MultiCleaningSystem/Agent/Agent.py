# Paquetes para trabajar con agentes y modelos
from mesa import Agent, Model
import numpy as np
from random import randint
class Scavenger(Agent):
    """ Clase heredada de mesa.agent que representa a un robot """
    
    def __init__(self, id: int, model: Model) -> None:
        """ El constructor recibe como parámetros el id del agente y el modelo 
        sobre le cual opera """
        super().__init__(id, model)

        self.value = 'R'
        self.storage = 5

    def step(self) -> None:
        """ Este metodo mueve a los robots a la posición más óptima """
        neighbors = self.model.grid.get_neighbors(self.pos, moore = True, include_center = False)  # Regresa un vector
        
        movements = set()
        neighborhood = set()
        robots = set()

        for agent in neighbors:
            if agent.value == 'R' or agent.value == 'X': # Si eres robot u obstáculo ya no eres una posición disponible                
                robots.add(agent.pos)
            else: # Si no eres robot, eres un vecino candidato
                neighborhood.add(agent.pos)

        movements = neighborhood.difference(robots) # Las posiciones que solo tengan basura o sean la papelera 

        if len(movements) != 0: # POR IMPLEMENTAR: Buscar el movimiento más óptimo
            self.model.grid.move_agent(self, movements.pop())
        
class Trash(Agent):
    """ Clase heredada de mesa.agent que representa una pila de basura """

    def __init__(self, id: int, model: Model, detritus:int) -> None:
        """ El constructor recibe como parámetros el id del agente, el modelo 
        sobre le cual opera y la basura que contiene esa casilla """
        super().__init__(id, model)

        self.value = 'T'
        self.detritus = detritus

class Wall (Agent):
    """ Clase heredada de mesa.agent que representa una pared u obstáculo"""

    def __init__(self, id: int, model: Model) -> None:
        """ El constructor recibe como parámetros el id del agente y el modelo 
        sobre le cual opera """
        super().__init__(id, model)
        
        self.value = 'X'

class Target (Agent):
    """ Clase heredada de mesa.agent que representa la papelera"""
    def __init__(self, id: int, model: Model) -> None:
        """ El constructor recibe como parámetros el id del agente y el modelo 
        sobre le cual opera """

        super().__init__(id, model)
        self.value = 'P'
