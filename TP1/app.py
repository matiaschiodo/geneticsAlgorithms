import random
import numpy as np
import matplotlib.pyplot as plt

def inicializarPoblacion(poblacion, cromosomas):
  return [[random.randint(0, 1) for i in range(cromosomas)] for i in range(poblacion)]

def objective(cromosoma):
  return ((arrayToInt(cromosoma)) ** 2)

def fitness(poblacion):
  obj = []
  fit = []
  suma = 0
  for i in range(len(poblacion)):
    obj.append(objective(poblacion[i]))
  for i in range(len(poblacion)):
    fit.append(obj[i] / sum(obj))
  grafica(fit)
  return fit

def grafica(porcentas):
#DEFINIMOS ETIQUETAS  
  etiquetas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'] #labels

  #PORCENTAJE DE CADA PORCIÓN. (parametro=porcentas)

  #DEFIMIMOS COLORES
  colores = ['#1abc9c', '#f1c40f', '#8e44ad', '#e74c3c', '#34495e', '#3498db', '#FFFF00', '#808000', '#32a852', '#008000'] #LabelColor

  #DIBUJAMOS GRÁFICA.  
  plt.pie(porcentas, labels = etiquetas, colors=colores,
          startangle=90, explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1,0.1, 0.1, 0.1,0.1),
          radius = 1.2, autopct = '%1.2f%%')

  #TITULO
  plt.title('Gráfica Circular')

  #MOSTRAMOS GRÁFICA.
  plt.show()
  

def arrayToInt(array):
  string = str(array[0])
  for i in range(1, len(array)):
    string += str(array[i])
  return int(string, 2)

def seleccion():
  pass

def seleccion_ruleta(poblacion):

    fitness = sum([cromosoma.fitness for cromosoma in poblacion])
    cromosoma_probabilidad = [(cromosoma.fitness*100) for cromosoma in poblacion] 
    return np.random.choice(poblacion = cromosoma_probabilidad)

def crossover():
  pass

def mutacion():
  pass

def maximo():
  pass

def minimo():
  pass

def promedio():
  pass

def algoritmoGenetico(fitness, tamPoblacion, tamCromosoma, numGeneraciones, probCrossover, probMutacion):
  poblacion = inicializarPoblacion(tamPoblacion, tamCromosoma)
  for i in range(numGeneraciones):
    poblacion = seleccion(poblacion, fitness)
    poblacion = crossover(poblacion, probCrossover)
    poblacion = mutacion(poblacion, probMutacion)
  return poblacion

# algoritmoGenetico(fitness, 10, 5, 20, 0.75, 0.05)
# algoritmoGenetico(fitness, 10, 5, 100, 0.75, 0.05)
# algoritmoGenetico(fitness, 10, 5, 200, 0.75, 0.05)

pob = inicializarPoblacion(10, 5)
print(pob)
print("\n")
for i in range(len(pob)):
  print(objective(pob[i]))
print("\n")
print(fitness(pob))
# print(objective(inicializarPoblacion(1, 5)))