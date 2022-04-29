from calendar import c
import random
import numpy as np
import matplotlib.pyplot as plt

def inicializarPoblacion(poblacion, cromosomas):
  return [[random.randint(0, 1) for i in range(cromosomas)] for i in range(poblacion)]

def arrayToInt(array):
  string = str(array[0])
  for i in range(1, len(array)):
    string += str(array[i])
  return int(string, 2)

def objetivo(cromosoma):
  return ((arrayToInt(cromosoma)) ** 2)

def fitness(poblacion):
  obj = []
  fitness = []
  for i in range(len(poblacion)):
    obj.append(objetivo(poblacion[i]))
  for i in range(len(poblacion)):
    fitness.append(obj[i] / sum(obj))
  return fitness

def grafica(porcentajes):
  #DEFINIMOS ETIQUETAS  
  etiquetas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'] #labels
  #PORCENTAJE DE CADA PORCIÓN. (parametro=porcentajes)

  #DEFIMIMOS COLORES
  colores = ['#1abc9c', '#f1c40f', '#8e44ad', '#e74c3c', '#34495e', '#3498db', '#FFFF00', '#808000', '#32a852', '#008000'] #LabelColor

  #DIBUJAMOS GRÁFICA.  
  plt.pie(porcentajes, labels = etiquetas, colors=colores, startangle=90, explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1,0.1, 0.1, 0.1,0.1), radius = 1.2, autopct = '%1.2f%%')

  #TITULO
  plt.title('Gráfica Circular')

  #MOSTRAMOS GRÁFICA.
  plt.show()

def ruleta(fitness):
  ruleta = []
  for i in range(len(fitness)):
    ruleta.append(round(fitness[i] * 100, 2))
  return ruleta


def seleccion(ruleta):
  cromosomas = []
  for i in range(len(ruleta)):
    n = random.randint(0, 99)
    prob = 0
    for i in range(0, len(ruleta)):
      prob += round(ruleta[i])
      if prob >= n:
        cromosomas.append(i)
        break
  return cromosomas

def crossover(poblacion, cromosomas, probCrossover, probMutacion):
  for i in range(0, len(poblacion), 2):
    hayCrossover = random.uniform(0, 1)
    if(hayCrossover < probCrossover):
      aux = poblacion[cromosomas[i]][4]
      poblacion[cromosomas[i]][4] = poblacion[cromosomas[i+1]][4]
      poblacion[cromosomas[i+1]][4] = aux
      poblacion = mutacion(poblacion, cromosomas[i], cromosomas[i+1], probMutacion)
    return poblacion

def mutacion(poblacion, cromosoma1, cromosoma2, probMutacion):
  hayMutacion = random.uniform(0, 1)
  if(hayMutacion < probMutacion):
    aux = poblacion[cromosoma1]
    poblacion[cromosoma1] = poblacion[cromosoma2]
    poblacion[cromosoma2] = aux
    aux = poblacion[cromosoma1][1]
    poblacion[cromosoma1][1] = poblacion[cromosoma2][1]
    poblacion[cromosoma2][1] = aux
    return poblacion
  return poblacion

def maximoCromosoma(poblacion):
  maximo = [0]
  for i in range(len(poblacion)):
    if(arrayToInt(poblacion[i]) > arrayToInt(maximo)):
      maximo = poblacion[i]
  return maximo

def minimoCromosoma(poblacion):
  minimo = [1, 1, 1, 1, 1]
  for i in range(len(poblacion)):
    if(arrayToInt(poblacion[i]) < arrayToInt(minimo)):
      minimo = poblacion[i]
  return minimo

def promedioCromosomas(poblacion):
  promedio = 0
  for i in range(len(poblacion)):
    promedio += arrayToInt(poblacion[i])
  return promedio / len(poblacion)

def algoritmoGenetico(fitness, tamPoblacion, tamCromosoma, numGeneraciones, probCrossover, probMutacion):
  maximoTotal, minimoTotal, promedioTotal = 0, 0, 0
  for i in range(numGeneraciones):
    poblacion = inicializarPoblacion(tamPoblacion, tamCromosoma)
    maximo, minimo, promedio = 0, 0, 0
    poblacion = crossover(poblacion, seleccion(ruleta(fitness(poblacion))), probCrossover, probMutacion)
    maximo = maximoCromosoma(poblacion)
    minimo = minimoCromosoma(poblacion)
    promedio = promedioCromosomas(poblacion)
    print('Generacion: ', i)
    print('Poblacion: ', poblacion)
    print('Maximo: ', maximo, arrayToInt(maximo))
    print('Minimo: ', minimo, arrayToInt(minimo))
    print('Promedio: ', promedio)
    maximoTotal = maximoCromosoma(poblacion)
    minimoTotal = minimoCromosoma(poblacion)
    promedioTotal = promedioCromosomas(poblacion)
  print('Maximo Total: ', maximoTotal, arrayToInt(maximoTotal))
  print('Minimo Total: ', minimoTotal, arrayToInt(minimoTotal))
  print('Promedio Total: ', promedioTotal)
  

algoritmoGenetico(fitness, 10, 5, 200, 0.75, 0.05)
# algoritmoGenetico(fitness, 10, 5, 100, 0.75, 0.05)
# algoritmoGenetico(fitness, 10, 5, 200, 0.75, 0.05)

# pob = inicializarPoblacion(10, 5)
# print("Poblacion inicial: ", pob)
# print("Cromosomas -> fitness")
# for i in range(len(pob)):
#   print(arrayToInt(pob[i]), "    ->    ", objetivo(pob[i]))
# print("Fitness: ", fitness(pob))
# print("Ruleta: ", ruleta(fitness(pob)))
# seleccionados = seleccion(ruleta(fitness(pob)))
# print("Seleccion: ", seleccionados)
# print("Crossover: ", crossover(pob, seleccionados, 0.75, 0.05))
# print(grafica(fitness(pob)))