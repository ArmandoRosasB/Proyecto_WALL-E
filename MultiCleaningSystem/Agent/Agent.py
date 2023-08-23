# Paquetes para trabajar con agentes y modelos
from mesa import Agent, Model
import numpy as np
from random import randint

class Scavenger(Agent):
    """ Clase heredada de mesa.agent que representa a un robot """

    mapa = []
    cells = 1
    target = [-1, -1]
    
    visited = set()
    xVisit = []
    prev = []

    steps = 0


    def __init__(self, id: int, model: Model) -> None:
        """ El constructor recibe como parámetros el id del agente y el modelo 
        sobre le cual opera """
        super().__init__(id, model)

        self.value = 'R'
        self.storage = 5

    def step(self) -> None:
        """ Este metodo mueve a los robots a la posición más óptima """

        self.steps += 1
        
        neighbors = self.model.grid.get_neighbors(self.pos, moore = True, include_center = False)  # Regresa un vector
        
        movements = set()
        neighborhood = set()
        robots = set()

        self.visited.add(self.pos)
        
        if self.cells > 0:
            for agent in neighbors:
                if agent.value == 'R': # Si eres robot u obstáculo ya no eres una posición disponible             
                    robots.add(agent.pos)

                if agent.value == 'X':
                    robots.add(agent.pos)

                    if agent.pos not in self.visited:
                        self.visited.add(agent.pos)
                        self.mapa[agent.pos[0]][agent.pos[1]] = 'X'
                        self.cells -= 1


                else: # Si no eres robot, eres un vecino candidato
                    neighborhood.add(agent.pos)

            movements = neighborhood.difference(robots) # Las posiciones que solo tengan basura o sean la papelera 
            back = True
            for move in movements:
                if move not in self.visited:
                    back = False
                    if move in self.xVisit:
                        self.xVisit.remove(move)

                    self.xVisit.append(move)
        
            if len(movements) == 0 or back:
                self.model.grid.move_agent(self, self.prev.pop())
                return

            self.prev.append(self.pos)
            self.model.grid.move_agent(self, self.xVisit.pop())
            self.cells -= 1


            aux = [agent.detritus for agent in self.model.grid.iter_cell_list_contents(self.pos) if agent.value == 'T']

            if len(aux) > 0:
                self.mapa[self.pos[0]][self.pos[1]] = aux[0]


        else:
            print(self.steps)
            for row in self.mapa:
                for col in row:
                    print(col, end= " ")
                print()

        
        
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


