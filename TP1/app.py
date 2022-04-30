import os
import random
import numpy as np
import matplotlib.pyplot as plt

def inicializarPoblacion(poblacion, cromosomas):
  return [[random.randint(0, 1) for i in range(cromosomas)] for i in range(poblacion)]
  #Rellenamos la matriz con el primero for nos posicionamos en el primer comosoma y lo llenamos con 5 genes random entre 0 y 1

def objetive(cromosoma):
  return ((arrayToInt(cromosoma)) ** 2)

def arrayToInt(array):
  string = str(array[0])
  for i in range(1, len(array)):
    string += str(array[i])
  return int(string, 2)
# Agarray un array y en cada gen lo convierte en string concatenandolo en una variable String
# Despues ese cromosoma que estaba en un array ahora lo convertimos en un String con la Funcion int,
# pasandole como parametro que sea de base 2. :) 

def llenarMatriz(decimal,vector):
  i=4
  print("Proceso de convertir",decimal)
  while True:
    if i == 0:
      break
    residuo = int(decimal % 2)
    decimal = int(decimal / 2)
    vector[i]=residuo
    i-=1
  return vector

def arrayOrder(pob):
  aux = []
  listaDec=[]
  for i in range(len(pob)):
    listaDec.append(arrayToInt(pob[i]))
  listaDec = sorted(list(listaDec))
#  print(listaDec)
  for i in range(len(listaDec)):
    decimal = listaDec[i]
      # Aquí almacenamos el resultado
    binario = [[0 for i in range(5)] for i in range(10)]
    binario[i] = llenarMatriz(decimal, binario[i])
    aux.append(binario[i])
  print(aux)
  return aux

def fitness(poblacion):
  obj = []
  fit = []
  suma = 0
  for i in range(len(poblacion)):
    obj.append(objetive(poblacion[i]))
  for i in range(len(poblacion)):
    fit.append(obj[i] / sum(obj))
  grafica(fit)
  return fit
# Declara un array objetivo(obj) donde almacena la funcion objetivo de cada cromosoma (x++2) 
# Hacemos un segundo For donde recorre los 10 cromosomas (leng(poblacion)) 
# dividiendo func objetivo de cada cromosoma / sumatoria de la poblacion(func objetivo c/u)

def grafica(porcentas):
  #DEFINIMOS ETIQUETAS  
  etiquetas = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] #labels
  #PORCENTAJE DE CADA PORCIÓN. (parametro=porcentas)
  #DEFIMIMOS COLORES
  colores = ['#1abc9c', '#f1c40f', '#8e44ad', '#e74c3c', '#34495e', '#3498db', '#FFFF00', '#808000', '#32a852', '#008000'] #LabelColor
  #DIBUJAMOS GRÁFICA.  
  plt.pie(porcentas, labels = etiquetas, colors=colores,
          startangle=120, explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1,0.1, 0.1, 0.1,0.1),
          radius = 1.2, autopct = '%1.2f%%')
  #TITULO
  plt.title('Gráfica Circular')
  #MOSTRAMOS GRÁFICA.
  plt.show()

def ruleta(fitness):
  ruleta = []
  for i in range(len(fitness)):
    ruleta.append(round(fitness[i] * 100, 2))
  return ruleta

def tournament(fitness):
  pob = []
  while True:
    n = random.randint(0, 9)
    n1 = random.randint(0,9)
    if n1 != n:
      if round(fitness[n]*100, 0) > round(fitness[n1]*100, 0):
        pob.append(fitness[n])
      else:
        pob.append(fitness[n1])
    elif n == n1:
      pob.append(fitness[n])
    if len(pob) == 10:
      break
  return pob

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

def crossover(poblacion, cromosomas, probCrossover, probMutacion, elitismo):
  if elitismo:
    long = len(poblacion)-2
  else:
    long = len(poblacion)
  posiciones = []
  i,k = 0,0
  cromosomas = list(set(cromosomas))
  for i in range(len(cromosomas)):
    corte = random.randint(1,4)
    k=0
    if i == 0:
      print("Se van a cortar")
      print(cromosomas)
    print("En la posicion ",corte)
    while corte <= 4:
      poblacion[cromosomas[i]][k] = poblacion[k][corte]
      k += 1
      corte += 1
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

def algoritmoGenetico(tamPoblacion, tamCromosoma, numGeneraciones, probCrossover, probMutacion, elitismo, torneo):
  maximoTotal, minimoTotal, promedioTotal = 0, 0, 0
  poblacion = arrayOrder(inicializarPoblacion(tamPoblacion, tamCromosoma))
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


def menu():
	
	os.system('cls') 
	print ("Selecciona una opción")
	print ("\t1 - Seleccion Ruleta")
	print ("\t2 - Seleccion Ruleta con elitismo")
	print ("\t3 - Seleccion torneo")
	print ("\t0 - salir")

algoritmoGenetico(10, 5, 2, 0.75, 0.05, True, True)


  
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
