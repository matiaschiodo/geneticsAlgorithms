import copy
import os
import time

def clearScreen():
	# Limpia la terminal.
	os.system('cls' if os.name == 'nt' else 'clear')

def numberToList(number, minListSize):
	# Convierte un numero decimal en una lista de bits.
	bitList = []
	if number is 1:
		bitList.append(1)
	else:
		actual = number
		while True:
			bitList.append(actual % 2)
			actual = actual // 2
			if actual == 1:
				bitList.append(1)
				break
	while len(bitList) < minListSize:
		bitList.append(0)
	bitList.reverse()
	return bitList

def printResults(bag):
	# Imprimir en pantalla el resultado encontrado.
	print("Valor máximo posible: ", bag.getTotalValue())
	print("Volumen total: ", bag.getTotalVolume())
	print("Elementos encontrados: ")
	for element in bag.getSortedContentByValue():
		print("Valor: {} | Volumen: {}".format(element.value, element.volume))

class Bag(object):
	# size (int): capacidad de volumen máxima.
	# content (list): lista de elementos contenidos.
	def __init__(self, size, content=None):
		# Constructor de la clase.
		self.size = size
		if content is None:
			self.content = []
		else:
			self.content = content

	def addElement(self, element):
		# Agregar elemento a la mochila.
		self.content.append(element)

	def popLastElement(self):
		self.content.pop()

	def getSortedContentByValue(self):
		# Devolver contenido de la mochila ordenado por valor.
		sortedContent = copy.deepcopy(self.content)
		sortedContent.sort(key = lambda Element: Element.value)
		sortedContent.reverse()
		return sortedContent

	def getTotalValue(self):
		# Obtener suma de todos los valores de los elementos en la mochila.
		totalValue = 0
		for element in self.content:
			totalValue += element.value
		return totalValue

	def getTotalVolume(self):
		# Obtener suma de todos los volumenes de los elementos de la mochila.
		totalVolume = 0
		for element in self.content:
			totalVolume += element.volume
		return totalVolume

	def isOverloaded(self):
		# Obtener si el contenido sobrepaso la capacidad máxima.
		return (self.getTotalVolume() > self.size)

class Element(object):
	# volume (int): volumen del elemento en cm^2.
	# value (int): valor del elemento.
	def __init__(self, volume, value):
		# Constructor de la clase.
		self.volume = volume
		self.value = value
		self.ratio = value / volume

def busquedaExhaustiva(elementList, maxSize):
	# Crear primera mochila vacia y marcarla como resultado óptimo.
	# Se usará como punto de partida para comparar futuros resultados.
	maxBag = Bag(maxSize)

	for i in range(1, 2 ** len(elementList)):

		# Crear nueva mochila.
		bag = Bag(maxSize)

		# Crear un patrón de bits, relativo a la iteración actual.
		bitPattern = numberToList(i, len(elementList))

		# Dependiendo del patrón, agregar los elementos seleccionados a la mochila.
		for n in range(len(elementList)):
			if bitPattern[n] == 1:
				bag.addElement(elementList[n])

		# Comparar mochila actual con el máximo encontrado.
		if (not bag.isOverloaded()) and (bag.getTotalValue() > maxBag.getTotalValue()):
			maxBag = bag

	return maxBag

def busquedaGreedy(elementList, maxSize):

	# Crear nueva mochila.
	bag = Bag(maxSize)

	# Ordenar lista de elementos relativo a la relacion valor / volumen.
	elementList.sort(key = lambda Element: Element.ratio)
	elementList.reverse()

	# Ejecutar busqueda greedy.
	for element in elementList:
		bag.addElement(element)
		if bag.isOverloaded():
			bag.popLastElement()

	return bag

### PROGRAMA

clearScreen()

# Iniciar parámetros de búsqueda.
maxSize = 4200
elements = [
	Element(150, 20), 
	Element(325, 40),
	Element(600, 50),
	Element(805, 36),
	Element(430, 25),
	Element(1200, 64),
	Element(770, 54),
	Element(60, 18),
	Element(930, 46),
	Element(353, 28)
]

start_time = time.time()

# bag = busquedaExhaustiva(elements, maxSize)
bag = busquedaGreedy(elements, maxSize)
printResults(bag)

print("--- %s seconds ---" % (time.time() - start_time))

input("Presione una tecla para finalizar...")
