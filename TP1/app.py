import random
import numpy as np
import matplotlib.pyplot as plt
import os

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
  return sorted(ruleta)

def tournament(fitness):
  pob = []
  while True:
    n = random.randint(0, 9)
    n1 = random.randint(0, 9)
    if n1 != n:
      if fitness[n] > fitness[n1]:
        pob.append(fitness[n])
      else:
        pob.append(fitness[n1])
    if len(pob) == 10:
      break
  return pob

def seleccion(ruleta, elitismo):
  if elitismo:
    long = len(ruleta) - 2
    totalProb = int(99 - ruleta[-1] - ruleta[-2])
  else:
    long = len(ruleta)
    totalProb = 99
  cromosomas = []
  for i in range(long):
    n = random.randint(0, totalProb)
    prob = 0
    for i in range(0, len(ruleta)):
      prob += round(ruleta[i])
      if prob >= n:
        cromosomas.append(i)
        break
  return cromosomas

def crossover(poblacion, cromosomas, probCrossover, probMutacion):
  for i in range(0, len(cromosomas), 2):
    hayCrossover = random.uniform(0, 1)
    corte = random.randint(1, 3)
    if(hayCrossover < probCrossover):
      print(hayCrossover, corte)
      cromosoma1 = poblacion.index(cromosomas[i])
      cromosoma2 = poblacion.index(cromosomas[i + 1])
      print(poblacion[cromosoma1], poblacion[cromosoma2])
      poblacion[cromosoma1] = np.append(poblacion[cromosoma1][:corte], poblacion[cromosoma2][corte:])
      poblacion[cromosoma2] = np.append(poblacion[cromosoma2][:corte], poblacion[cromosoma1][corte:])
      print(poblacion[cromosoma1], poblacion[cromosoma2])
  return poblacion

pob = inicializarPoblacion(10, 5)
cromosomas = [pob[2], pob[5]]
print(pob, cromosomas)
print(ruleta(fitness(pob)))
selec = seleccion(ruleta(fitness(pob)), True)
print(selec)
(crossover(pob, selec, 0.75, 0.05))

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

def algoritmoGenetico(tamPoblacion, tamCromosoma, numGeneraciones, probCrossover, probMutacion, elitismo, torneo):
  maximoTotal, minimoTotal, promedioTotal = 0, 0, 0
  poblacion = inicializarPoblacion(tamPoblacion, tamCromosoma)
  for i in range(numGeneraciones):
    maximo, minimo, promedio = 0, 0, 0
    if torneo:
      poblacion = crossover(poblacion, seleccion(tournament(fitness(poblacion))), probCrossover, probMutacion, elitismo)
    else:
      poblacion = crossover(poblacion, seleccion(ruleta(fitness(poblacion))), probCrossover, probMutacion, elitismo)
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
  
#algoritmoGenetico(fitness, 10, 5, 200, 0.75, 0.05)
# algoritmoGenetico(fitness, 10, 5, 100, 0.75, 0.05)
# algoritmoGenetico(fitness, 10, 5, 200, 0.75, 0.05)

def pedirOpcion():
  correcto=False
  num=0
  while(not correcto):
    try:
      num = int(input("Introduce un numero entero: "))
      correcto=True
    except ValueError:
      print('Error, introduce un numero entero')
  return num
 
# salir = False
# opcion = 0
 
# while not salir:
#   os.system('cls') 
#   print ("1. Ruleta")
#   print ("2. Ruleta con elitismo")
#   print ("3. Torneo")
#   print ("4. Torneo con elitismo")
#   print ("0. Salir")

#   print ("Elige una opcion")

#   opcion = pedirOpcion()

#   if opcion == 1:
#     algoritmoGenetico(10, 5, 200, 0.75, 0.05, False, False)
#   elif opcion == 2:
#     algoritmoGenetico(10, 5, 200, 0.75, 0.05, True, False)
#   elif opcion == 3:
#     algoritmoGenetico(10, 5, 200, 0.75, 0.05, False, True)
#   elif opcion == 4:
#     algoritmoGenetico(10, 5, 200, 0.75, 0.05, True, True)
#   elif opcion == 0:
#     salir = True
#   else:
#     print ("Introduce un numero entre 1 y 4")

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
