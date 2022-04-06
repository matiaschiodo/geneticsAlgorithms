import random

def inicializarPoblacion(poblacion, cromosomas):
  return [[random.randint(0, 1) for i in range(cromosomas)] for i in range(poblacion)]

def fitness(x):
  return x**2

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

print(inicializarPoblacion(10, 5))