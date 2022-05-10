import os
import random
import numpy as np
import matplotlib.pyplot as plt

def inicializarPoblacion(poblacion, cromosomas):
  # Inicializamos la población de cromosomas como un array de binarios.
  # Ej: [[1, 0, 0, 1, 0], [1, 0, 0, 1, 0], [1, 0, 0, 1, 0]]
  return sorted([[random.randint(0, 1) for i in range(cromosomas)] for i in range(poblacion)])

# Funcion para convertir un array de binarios a un entero.
def arrayToInt(array):
  string = str(array[0])
  for i in range(1, len(array)):
    string += str(array[i])
  return int(string, 2)

# Función para calcular el objetivo.
def objetivo(cromosoma):
  return ((arrayToInt(cromosoma)) ** 2)

# Función para calcular el fitness de cada cromosoma.
def fitness(poblacion):
  obj = []
  fitness = []
  for i in range(len(poblacion)):
    obj.append(objetivo(poblacion[i]))
  for i in range(len(poblacion)):
    fitness.append(obj[i] / sum(obj))
  return fitness

# Función para graficar la probabilidad de la ruleta.
def graficaRuleta(porcentajes, numgen, op):
  #DEFINIMOS ETIQUETAS  
  etiquetas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'] #labels
  #PORCENTAJE DE CADA PORCIÓN. (parametro = porcentajes)
  #DEFIMIMOS COLORES
  colores = ['#1abc9c', '#f1c40f', '#8e44ad', '#e74c3c', '#34495e', '#3498db', '#FFFF00', '#808000', '#32a852', '#008000'] #LabelColor
  #DIBUJAMOS GRÁFICA.  
  plt.pie(porcentajes, labels = etiquetas, colors=colores, startangle=90, explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1,0.1, 0.1, 0.1,0.1), radius = 1.2, autopct = '%1.2f%%')
  #TITULO
  plt.title('Gráfica Circular')
  #MOSTRAMOS GRÁFICA.
  if op == 1:
    ruta = "Ruleta"
    try:
      os.stat(ruta)
    except:
      os.mkdir(ruta)
      
  elif op == 2:
    ruta = 'Ruleta_elitismo'
    try:
      os.stat(ruta)
    except:
      os.mkdir(ruta)
      
  elif op == 3:
    ruta= "Torneo"
    try:
      os.stat(ruta)
    except:
      os.mkdir(ruta)
      
  elif op == 4:
      ruta = "Torneo_elitimos"
      try:
        os.stat(ruta)
      except:
        os.mkdir(ruta)
  img = "grafica.jpg"
  x=np.linspace(0,5,100)
  plt.savefig(ruta+"/"+str(numgen)+"-"+img, bbox_inches='tight')
  plt.clf()
  return porcentajes

def graficaBastones(numgen, maximo, minimo, promedio):
  ## Declaramos valores para el eje x
  eje_x = ["maximo", "minimo", "promedio"]
  ## Declaramos valores para el eje y
  eje_y = [maximo,minimo,promedio]
  ## Creamos Gráfica
  plt.bar(eje_x, eje_y)
  ## Legenda en el eje y
  plt.ylabel('')
  ## Legenda en el eje x
  plt.xlabel('Información')
  ## Título de Gráfica
  plt.title('Generacion '+str(numgen))
  plt.show()

# Función para declarar el método de ruleta
def ruleta(fitness):
  ruleta = []
  for i in range(len(fitness)):
    ruleta.append(fitness[i] * 100)
  return sorted(ruleta)

# Función para declarar el método de torneo
def tournament(poblacion, fitness):
  pob = []
  while True:
    n = random.randint(0, 9)
    n1 = random.randint(0, 9)
    if n1 != n:
      if fitness[n] > fitness[n1]:
        pob.append(poblacion[n])
      else:
        pob.append(poblacion[n1])
    if len(pob) == 10:
      break
  return pob

# Función para seleccionar cromosomas para el crossover.
def seleccion(ruleta, elitismo, metodo):
  if metodo == 1: # Metodo de ruleta
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
        prob += ruleta[i]
        if prob >= n:
          cromosomas.append(i)
          break
  else: # Metodo de torneo
    cromosomas = []
    if elitismo:
      long = 7
    else:
      long = 9
    for i in range(10):
      n = random.randint(0, long)
      cromosomas.append(n)
  return cromosomas

# Función para el cruce.
def crossover(poblacion, cromosomas, probCrossover, probMutacion):
  for i in range(0, len(cromosomas), 2):
    hayCrossover = random.uniform(0, 1)
    corte = random.randint(1, 3)
    if(hayCrossover < probCrossover):
      c1 = poblacion[cromosomas[i]]
      c2 = poblacion[cromosomas[i + 1]]
      poblacion[cromosomas[i]] = np.append(c1[:corte], c2[corte:])
      poblacion[cromosomas[i + 1]] = np.append(c2[:corte], c1[corte:])
      mutacion(poblacion, cromosomas[i], cromosomas[i + 1], probMutacion)
  return poblacion

# Función para la mutación.
def mutacion(poblacion, cromosoma1, cromosoma2, probMutacion):
  hayMutacion = random.uniform(0, 1)
  corte = 1
  if(hayMutacion < probMutacion):
    c1 = poblacion[cromosoma1]
    c2 = poblacion[cromosoma2]
    poblacion[cromosoma1] = np.append(c1[:corte], c2[corte:])
    poblacion[cromosoma2] = np.append(c2[:corte], c1[corte:])
    return poblacion
  return poblacion

# Función para calcular el mayor cromosoma de la población.
def maximoCromosoma(poblacion):
  maximo = [0]
  for i in range(len(poblacion)):
    if(arrayToInt(poblacion[i]) > arrayToInt(maximo)):
      maximo = poblacion[i]
  return maximo

# Función para calcular el menor cromosoma de la población.
def minimoCromosoma(poblacion):
  minimo = [1, 1, 1, 1, 1]
  for i in range(len(poblacion)):
    if(arrayToInt(poblacion[i]) < arrayToInt(minimo)):
      minimo = poblacion[i]
  return minimo

# Función para calcular el promedio de los cromosomas de la población.
def promedioCromosomas(poblacion):
  promedio = 0
  for i in range(len(poblacion)):
    promedio += arrayToInt(poblacion[i])
  return promedio / len(poblacion)

# Función para ejecutar el algoritmo genético en base a los parametros ingresados.
def algoritmoGenetico(tamPoblacion, tamCromosoma, numGeneraciones, probCrossover, probMutacion, elitismo, torneo, op):
  maximoTotal, minimoTotal, promedioTotal = 0, 0, 0
  poblacion = inicializarPoblacion(tamPoblacion, tamCromosoma)
  for i in range(numGeneraciones):
    maximo, minimo, promedio = 0, 0, 0
    if torneo:
      poblacion = crossover(poblacion, seleccion(tournament(poblacion, fitness(poblacion)), elitismo, 2), probCrossover, probMutacion)
    else:
      poblacion = crossover(poblacion, seleccion(graficaRuleta(ruleta(fitness(poblacion)),i, op), elitismo, 1), probCrossover, probMutacion)
    maximo = maximoCromosoma(poblacion)
    minimo = minimoCromosoma(poblacion)
    promedio = promedioCromosomas(poblacion)
    print('Generacion: ', i)
    print('Poblacion: ', poblacion)
    print('Maximo: ', maximo, arrayToInt(maximo))
    print('Minimo: ', minimo, arrayToInt(minimo))
    print('Promedio: ', promedio)
    graficaBastones(i, arrayToInt(maximo), arrayToInt(minimo), promedio)
    maximoTotal = maximoCromosoma(poblacion)
    minimoTotal = minimoCromosoma(poblacion)
    promedioTotal = promedioCromosomas(poblacion)
  print('Maximo Total: ', maximoTotal, arrayToInt(maximoTotal))
  print('Minimo Total: ', minimoTotal, arrayToInt(minimoTotal))
  print('Promedio Total: ', promedioTotal)

def pedirOpcion(minimo, maximo):
  num = -1
  while num < minimo or num > maximo:
    num = int(input('Ingrese un numero entre ' + str(minimo) + ' y ' + str(maximo) + ': '))
  return num

salir = False
opcion = 0

while not salir:
  print("Ingrese el numero de generaciones que desea realizar.")

  numGeneraciones = pedirOpcion(1, 2000)

  print ("1. Ruleta")
  print ("2. Ruleta con elitismo")
  print ("3. Torneo")
  print ("4. Torneo con elitismo")
  print ("0. Salir")

  opcion = pedirOpcion(0, 4)

  if opcion == 1:
    algoritmoGenetico(10, 5, numGeneraciones, 0.75, 0.05, False, False, opcion)
  elif opcion == 2:
    algoritmoGenetico(10, 5, numGeneraciones, 0.75, 0.05, True, False, opcion)
  elif opcion == 3:
    algoritmoGenetico(10, 5, numGeneraciones, 0.75, 0.05, False, True, opcion)
  elif opcion == 4:
    algoritmoGenetico(10, 5, numGeneraciones, 0.75, 0.05, True, True, opcion)
  elif opcion == 0:
    salir = True
