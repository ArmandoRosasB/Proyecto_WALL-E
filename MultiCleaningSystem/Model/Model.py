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

def get_grid(model):
    grid = np.zeros( (model.grid.width, model.grid.height) )

    for (content, (x, y)) in model.grid.coord_iter():
        if len(content) == 1:  
            if content[0].value == 'X':
                grid[x][y] = 5 # Obstáculo
            elif content[0].value == 'P':
                grid[x][y] = 2 # Papelera
            else:
                grid[x][y] = 3 # Solo basura
            
            continue
        
        grid[x][y] = 1 # Basura con robot | Robot con robot
    
    return grid

class Office(Model):
    """ Clase heredada de mesa.model que representa la oficina """
    
    def __init__(self, width:float, height:float, office) -> None:
        """ El constructor recibe como parámetros el ancho y alto de la oficina,
        así como una matriz representando lo que contiene la oficina """
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)

        id = 0
        for (content, (x, y)) in self.grid.coord_iter():
            agent = None

            if office[x][y] == 'X':
                agent = Wall(id, self)

            elif office[x][y] == 'P':
                agent = Target(id, self)

            elif office[x][y] == 'S':
                agent = Trash(id, self, 0)

                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)

                id += 1

                for i in range(5):
                    agent = Scavenger(id, self)
                    
                    self.grid.place_agent(agent, (x, y))
                    self.schedule.add(agent)

                    id += 1
                
                continue

            else: # Trash
                agent = Trash(id, self, int(office[x][y]))
            
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)
            id += 1

        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})
    
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()