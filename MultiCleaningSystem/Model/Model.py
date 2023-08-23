from MultiCleaningSystem.Agent.Agent import Scavenger, Trash, Wall, Target

# Paquetes para el manejo de valores numéricos
import numpy as np
import pandas as pd

# Paquetes para trabajar con modelos
from mesa import Model

# Paquete para poder alojar a varios agentes en un mismo cuadrante
from mesa.space import MultiGrid

# Paquete para activar todos los robots al mismo tiempo
from mesa.time import SimultaneousActivation

# Paquete para obtener informacion del ambiente
from mesa.datacollection import DataCollector

colores = []

def get_grid(model):
    """
    La funcion get_grid recibe como parametro el modelo 
    y regresa el mapa del modelo con determinados valores
    en forma de matriz
    """
    grid = np.zeros( (model.grid.width, model.grid.height) )

    for (content, (x, y)) in model.grid.coord_iter():

        for c in colores:
            grid[c[0]][c[1]] = 4 # Robot
        if len(content) == 1:  
            if content[0].value == 'X':
                grid[x][y] = 11 # Obstáculo
            elif content[0].value == 'P' and [x, y] not in colores:
                grid[x][y] = 0 # Papelera
            elif [x, y] not in colores:
                grid[x][y] = 2 # Solo basura
            
            continue
        
        colores.append([x, y])
        grid[x][y] = 4000 # Robot

    
    return grid

class Office(Model):
    """ Clase heredada de mesa.model que representa la oficina """
    
    def __init__(self, width:float, height:float, office) -> None:
        """ El constructor recibe como parámetros el ancho y alto de la oficina,
        así como una matriz representando lo que contiene la oficina """
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)

        Scavenger.mapa = [[-1 for column in range (height)] for row in range (width)]
        Scavenger.cells = width * height

        id = 0
        for (content, (x, y)) in self.grid.coord_iter():
            agent = None

            if office[x][y] == 'X':
                agent = Wall(id, self)

            elif office[x][y] == 'P':
                agent = Target(id, self)
                Scavenger.target = [x, y]
                Scavenger.mapa[x][y] = 'P'

            elif office[x][y] == 'S':
                agent = Trash(id, self, 0)
                self.grid.place_agent(agent, (x, y))
                Scavenger.mapa[x][y] = 0

                id += 1
                
                offset = 0
                partition = [width // 5 for i in range(5)]

                for i in range(width % 5):
                    partition[i] += 1

                for i in range(5): # AGENTES: 5
                    agent = Scavenger(id, self,  offset, offset + partition[i] - 1)
                    # agent.cells = (offset + partition[i] - 1) * height
                   # agent = Scavenger(id, self, 1, 3)
                    offset += partition[i]

                    self.grid.place_agent(agent, (x, y))
                    self.schedule.add(agent)

                    id += 1
                
                continue

            else: # Trash
                agent = Trash(id, self, int(office[x][y]))
            
            self.grid.place_agent(agent, (x, y))
            id += 1

        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})
    
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()