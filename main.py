from MultiCleaningSystem.Model.Model import Office

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128

MAX_ITERATIONS = 100
width = 0
height = 0
office = []

flag = True
with open('Tests/input1.txt', 'r') as input:
    
    for linea in input:
        if flag:
            width, height = [int(num) for num in linea.split(" ")]
            flag = False
        
        else:
            office.append(linea.split(" "))

model = Office(width, height, office)

for i in range(MAX_ITERATIONS):
    model.step()

all_grid = model.datacollector.get_model_vars_dataframe() # Arreglo de matrices

fig, axis = plt.subplots(figsize= (5, 5))
axis.set_xticks([])
axis.set_yticks([])
patch = plt.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)


def animate(i):
    patch.set_data(all_grid.iloc[i][0])
    
anim = animation.FuncAnimation(fig, animate, frames = MAX_ITERATIONS)

plt.show()