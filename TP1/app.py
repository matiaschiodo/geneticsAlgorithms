import random
import numpy as np

def inicializarPoblacion(poblacion, cromosomas):
  return [random.randint(0, 1) for i in range(cromosomas) for i in range(poblacion)]

def objetive(cromosoma):
  return (arrayToInt(cromosoma) ** 2)

def fitness(poblacion):
  array = []
  for i in range(len(poblacion)):
    array.insert(-1, objetive(poblacion[i]))
  return array

def arrayToInt(array):
  string = str(array[0])
  for i in range(1, len(array)):
    string += str(array[i])
  return int(string, 2)

def seleccion():
  pass

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
for i in range(len(pob)):
  print(objetive(pob[i]))
print(fitness(pob))
# print(objetive(inicializarPoblacion(1, 5)))