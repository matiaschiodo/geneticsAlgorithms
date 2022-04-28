from calendar import c
import random
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import randint
from numpy.random import rand

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


def crossover(poblacion, cromosomas):
  for i in range(0, len(poblacion), 2):
    aux = poblacion[cromosomas[i]][4]
    poblacion[cromosomas[i]][4] = poblacion[cromosomas[i+1]][4]
    poblacion[cromosomas[i+1]][4] = aux
  return poblacion



'''def seleccion_padres(cromosomas):
  p1 = random.choice(cromosomas)
  p2 = random.choice(cromosomas)
  return [p1, p2]


def crossover(p1, p2):
  h1, h2 = p1.copy(), p2.copy()
  if rand() < prob_cross:
  corte = random.randint(1, len(pob)-1)
  h1 = p1[:corte] + p2[corte:]
  h2 = p2[:corte] + p1[corte:]
  return [h1,h2]'''


def mutacion():
 # if rand() < prob_mut:
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
print("Poblacion inicial: ", pob)
print("Cromosomas -> fitness")
for i in range(len(pob)):
  print(arrayToInt(pob[i]), "    ->    ", objetivo(pob[i]))
print("Fitness: ", fitness(pob))
print("Ruleta: ", ruleta(fitness(pob)))
seleccionados = seleccion(ruleta(fitness(pob)))
print("Seleccion: ", seleccionados)
print("Crossover: ", crossover(pob, seleccionados))
# print(grafica(fitness(pob)))

'''pob = inicializarPoblacion(10, 5)
print("Poblacion inicial: ", pob)
print("Nro Decimal -> Objetivo")
for i in range(len(pob)):
  print(arrayToInt(pob[i]), "            ", objetivo(pob[i]))
print("Fitness: ", fitness(pob))
print("Ruleta: ", ruleta(fitness(pob)))
seleccionados = seleccion(ruleta(fitness(pob)))
print("Seleccion: ", seleccionados)
#falta tirar un num random para ver si se hace crossover o mutacion
for i in range (0,5):
  p1 = random.choice(seleccionados)
  p2 = random.choice(seleccionados)
  print("Padres", p1,p2)
  print("Crossover: ", crossover(p1, p2))
# print(grafica(fitness(pob)))
'''
