# Importamos el modelo y los agentes
from MultiCleaningSystem.Model.Model import Office
from MultiCleaningSystem.Ugraph.Ugraph import dijkstra, BreadthFirstSearch

# Importamos matplotlib y seaborn para poder visualizar los resultados
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128

width = 0
height = 0
office = []

flag = True
with open('Tests/input5.txt', 'r') as input:
    
    for linea in input:
        if flag:
            width, height = [int(num) for num in linea.split(" ")]
            flag = False
        
        else:
            office.append(linea.split(" "))

model = Office(width, height, office) # Inicializamos el modelo

while not model.done:
    model.step()
    for row in model.mapa:
        for column in row:
            print(column, end=" ")
        print()
    print()
    print()

print("Algoritmo terminado en ", model.steps, " steps")
# Visualizacion
all_grid = model.datacollector.get_model_vars_dataframe() # Arreglo de matrices

fig, axis = plt.subplots(figsize= (width, height))
axis.set_xticks([])
axis.set_yticks([])
patch = plt.imshow(all_grid.iloc[0][0], cmap=sns.color_palette("Paired", as_cmap=True))

def animate(i):
    patch.set_data(all_grid.iloc[i][0])
    
anim = animation.FuncAnimation(fig, animate, frames = model.steps)

plt.show()
