import xlsxwriter
import datetime
import random as rnd
import os

# Parámetros de ejecución
popSize = 10
chromSize = 30
probCrossover = 0.75
probMutacionActual = 0.05
# roulette or tournament
method = "roulette"
# True or False
elitism = False

def clearScreen():
	# Limpia la terminal
	os.system('cls' if os.name == 'nt' else 'clear')

def decision(probability):
	# Toma una decision aleatoria en base a una probabilidad
	return rnd.random() < probability

class Chromosome(object):
	def __init__(self, size, madre=None, padre=None, punto=None):
		# Constructor del cromosoma
		self.gen = []
		if madre == None:
			for i in range(size):
				self.gen.append(rnd.randint(0,1))
			self.calculateValue()
			self.calculateScore()
		elif padre != None:
			for i in range(punto):
				self.gen.append(madre.gen[i])
			for i in range(punto, size):
				self.gen.append(padre.gen[i])
		else:
				for i in range(size):
					self.gen.append(madre.gen[i])
				self.value = madre.value
				self.score = madre.score
	
	def asString(self):
		# Devuelve un string en base al arreglo de genes
		chromStr = ""
		for g in self.gen:
			chromStr += str(g)
		return chromStr
	
	def calculateValue(self):
		# Calcula y guarda el valor entero decimal del cromosoma
		v = 0
		for g in range(len(self.gen)):
			v += self.gen[g] * (2 ** (chromSize - 1 - g))
		self.value = v
	
	def calculateScore(self):
		# Calcula y guarda el puntaje según la función objetivo
		self.score = ((self.value/((2**30) - 1))**2)
	
	def calculateFitness(self, totalScore):
		# Calcula y guarda el valor fitness
		self.fitness = self.score/totalScore
	
	def mutate(self):
		# Muta un gen aleatorio del cromosoma
		punto = rnd.randint(0, chromSize - 1)
		self.gen[punto] = 1 - self.gen[punto]
		self.calculateValue()
		self.calculateScore()

class Population(object):
	def __init__(self, prevPopulation=None, method=None, elitism=False):
		# Constructor de la población
		self.chromosomes = []
		self.totalScore = 0
		# Crear población aleatoriamente
		if prevPopulation == None:
			for i in range(popSize):
				individuo = Chromosome(chromSize)
				self.addChromosome(individuo)
		# Crear población hija en base a la población previa
		else:
			# Aplicar elitismo
			if elitism:
				self.addChromosome(Chromosome(chromSize, prevPopulation.chromosomes[-2]))
				self.addChromosome(Chromosome(chromSize, prevPopulation.chromosomes[-1]))
				size = int(popSize / 2) - 1
			else:
				size = int(popSize / 2)
			for i in range(size):
				# Método de selección
				if method == "roulette":
					padre = prevPopulation.selectWeightedChromosome()
					madre = prevPopulation.selectWeightedChromosome()
				elif method == "tournament":
					padre = prevPopulation.tournament()
					madre = prevPopulation.tournament()
				# Aplicar crossover
				if decision(probCrossover) & (padre != madre):
					punto = rnd.randint(1, chromSize - 1)
					hijo1 = Chromosome(chromSize, madre, padre, punto)
					hijo2 = Chromosome(chromSize, madre, padre, punto)
					isNew = True
				else:
					hijo1 = padre
					hijo2 = madre
					isNew = False
				# Aplicar mutación
				if decision(probMutacionActual):
					hijo1.mutate()
				elif isNew:
					hijo1.calculateValue()
					hijo1.calculateScore()
				if decision(probMutacionActual):
					hijo2.mutate()
				elif isNew:
					hijo2.calculateValue()
					hijo2.calculateScore()
				# Agregar cromosomas hijos
				self.addChromosome(hijo1)
				self.addChromosome(hijo2)
	
	def addChromosome(self, c):
		# Agrega un cromosoma a la población
		self.chromosomes.append(c)
	
	def calculateTotalScore(self):
		# Calcula y guarda la suma de los puntajes de todos los cromosomas
		for c in self.chromosomes:
			self.totalScore += c.score
	
	def sortByFitness(self):
		# Calcula los valores fitness de cada cromosoma y ordena de menor a mayor
		for c in self.chromosomes:
			c.calculateFitness(self.totalScore)
		self.chromosomes.sort(key = lambda Chromosome: Chromosome.value)
	
	def selectWeightedChromosome(self):
		# Devuelve un cromosoma, teniendo mayor probabilidad dependiendo de su valor fitness
		# Obtener lista de los valores fitness de los cromosomas
		w = []
		for c in self.chromosomes:
			w.append(c.fitness)
		# Devolver cromosoma aleatorio
		return rnd.choices(
			population = self.chromosomes,
			weights = w
		)[0]

	def selectChromosome(self):
		# Devuelve un cromosoma aleatorio
		return self.chromosomes[rnd.randint(0, popSize - 1)]

	def tournament(self):
		# Devuelve el mejor cromosoma
		padre = self.selectChromosome()
		madre = self.selectChromosome()
		return padre if padre.score > madre.score else madre
	
	def printStats(self):
		# Imprime en pantalla estadisticas de la población
		minimo = self.chromosomes[0].score
		maximo = self.chromosomes[-1].score # Indice -1 devuelve el último item
		promedio = self.totalScore / len(self.chromosomes)
		print("Máximo: ", maximo, "Mínimo: ", minimo, "Promedio: ", promedio)
	
	def printChrom(self):
		# Imprime en pantalla la lista de cromosomas
		for c in self.chromosomes:
			print(c.asString(), " f:", c.fitness)
	
	def exportDataToSpreadsheet(self, populationCounter):
		# Exporta los datos de la población a un archivo xlsx
		# Calcular valores estadísticos de la población
		global rowCounter
		global rowCounter_graph
		sumFitness = 0
		for c in self.chromosomes:
			sumFitness += c.fitness
		minScore = self.chromosomes[0].score
		minFitness = self.chromosomes[0].fitness
		maxScore = self.chromosomes[-1].score # Indice -1 devuelve el último item
		maxFitness = self.chromosomes[-1].fitness
		promScore = self.totalScore / len(self.chromosomes)
		promFitness = sumFitness / len(self.chromosomes)
		# Agregar encabezado y formato a la tabla
		dataSheet.merge_range(rowCounter, columnAlign, rowCounter,
			columnAlign+3, "Población {}".format(populationCounter+1), titleFormat)
		rowCounter += 1
		dataSheet.write_row(rowCounter, columnAlign,
			["Cromosoma", "Valor entero", "Objetivo", "Fitness"], boldFormat)
		rowCounter += 1
		# Agrega datos a la tabla
		for c in self.chromosomes:
			dataSheet.write(rowCounter, columnAlign, c.asString(), chromFormat)
			dataSheet.write(rowCounter, columnAlign+1, c.value)
			dataSheet.write(rowCounter, columnAlign+2, c.score, numberFormat)
			dataSheet.write(rowCounter, columnAlign+3, c.fitness, numberFormat)
			rowCounter += 1
		dataSheet.write(rowCounter, columnAlign, "Suma", boldFormat)
		dataSheet.write(rowCounter, columnAlign+2, self.totalScore, numberFormat)
		dataSheet.write(rowCounter, columnAlign+3, sumFitness, numberFormat)
		rowCounter += 1
		dataSheet.write(rowCounter, columnAlign, "Máximo", boldFormat)
		dataSheet.write(rowCounter, columnAlign+2, maxScore, numberFormat)
		dataSheet.write(rowCounter, columnAlign+3, maxFitness, numberFormat)
		rowCounter += 1
		dataSheet.write(rowCounter, columnAlign, "Mínimo", boldFormat)
		dataSheet.write(rowCounter, columnAlign+2, minScore, numberFormat)
		dataSheet.write(rowCounter, columnAlign+3, minFitness, numberFormat)
		rowCounter += 1
		dataSheet.write(rowCounter, columnAlign, "Promedio", boldFormat)
		dataSheet.write(rowCounter, columnAlign+2, promScore, numberFormat)
		dataSheet.write(rowCounter, columnAlign+3, promFitness, numberFormat)
		rowCounter += 2
		# Agregar estadísticas a la hoja de gráficos
		graphSheet.write_row(rowCounter_graph, columnAlign_graph,
			[rowCounter_graph])
		graphSheet.write_row(rowCounter_graph, columnAlign_graph+1,
			[minScore, promScore, maxScore], numberFormat)
		rowCounter_graph += 1

#################################
# INICIO DEL PROGRAMA PRINCIPAL #
#################################

clearScreen()

iteraciones = int(input("Ingrese cantidad de iteraciones a ejecutar: "))

clearScreen()

print ("1. Ruleta")
print ("2. Ruleta con elitismo")
print ("3. Torneo")
print ("4. Torneo con elitismo")
print ("0. Salir")

option = int(input('Ingrese un numero entre 0 y 4: '))

if(option == 2 or option == 4):
	elitism = True
if(option == 3 or option == 4):
	method = "tournament" 

clearScreen()


# Configuración para xlsxwriter
elit = ''
if elitism:
	elit = 'with_elitism'
else:
	elit = 'without_elitism'
rowCounter = 0
rowCounter_graph = 0
columnAlign = 0
columnAlign_graph = 0
filename = "Result_{method}_{elisism}_{iter}_{date}.xlsx".format(iter=iteraciones, method=method, elisism=elit, date=datetime.datetime.now().strftime("%d-%m-%Y_%H%M%S"))
workbook = xlsxwriter.Workbook(filename)
summarySheet = workbook.add_worksheet("Resumen")
summarySheet.set_column(0, 0, 18)
summarySheet.set_column(1, 1, 34)
dataSheet = workbook.add_worksheet("Data")
dataSheet.set_column(0, 0, 34)
dataSheet.set_column(1, 1, 12)
graphSheet = workbook.add_worksheet("Gráfico")
numberFormat = workbook.add_format({
	"valign": "right",
	"num_format": "0.00000"})
boldFormat = workbook.add_format({"bold": True})
chromFormat = workbook.add_format({"font_name": "Consolas"})
titleFormat = workbook.add_format({
	"bold": True,
	"align": "center",
	"valign": "vcenter"})

# Crear encabezado para página de gráfico
graphSheet.write_row(rowCounter_graph, columnAlign_graph,
	["Generación", "Mínimo", "Promedio", "Máximo"], boldFormat)
rowCounter_graph += 1

# Crear primera instancia de la población
newPopulation = Population(None, method, elitism)
maximum = newPopulation.chromosomes[0]

for n in range(iteraciones):
	# Calcular y guardar puntajes y valores fitness de los cromosomas
	newPopulation.calculateTotalScore()
	newPopulation.sortByFitness()
	# Escribir datos de la población en archivo
	newPopulation.exportDataToSpreadsheet(n)
	# Crear nueva población en base a la anterior
	prevPopulation = newPopulation
	newPopulation = Population(prevPopulation, method, elitism)

# Generar hoja resumen
row = 0
column = 0
resultChrom = prevPopulation.chromosomes[-1]
summarySheet.merge_range(row, column, row, column+1, "Parámetros", titleFormat)
row += 1
summarySheet.write(row, column, "Iteraciones")
summarySheet.write(row, column+1, iteraciones)
row += 1
summarySheet.write(row, column, "Tamaño población")
summarySheet.write(row, column+1, popSize)
row += 1
summarySheet.write(row, column, "Tamaño cromosomas")
summarySheet.write(row, column+1, chromSize)
row += 1
summarySheet.write(row, column, "Prob. crossover")
summarySheet.write(row, column+1, probCrossover*100)
row += 1
summarySheet.write(row, column, "Prob. mutación")
summarySheet.write(row, column+1, probMutacionActual*100)
row += 1
summarySheet.write(row, column, "Método de cruce")
summarySheet.write(row, column+1, method)
row += 1
summarySheet.write(row, column, "Elitismo")
summarySheet.write(row, column+1, str(elitism))
row += 1
summarySheet.merge_range(row, column, row, column+1, "Resultado", titleFormat)
row += 1
summarySheet.write(row, column, "Cromosoma máximo")
summarySheet.write(row, column+1, resultChrom.asString(), chromFormat)
row += 1
summarySheet.write(row, column, "Valor entero")
summarySheet.write(row, column+1, resultChrom.value)
row += 1
summarySheet.write(row, column, "Función objetivo")
summarySheet.write(row, column+1, resultChrom.score)
row += 1
summarySheet.write(row, column, "Función fitness")
summarySheet.write(row, column+1, resultChrom.fitness)

# Generar gráfico
chart = workbook.add_chart({"type": "line"})
for col in range(1,4):
	chart.add_series({
		"name":       ["Gráfico", 0, col],
		"values":     ["Gráfico", 1, col, iteraciones, col],
	})
chart.set_title ({"name": "Evolución de la población"})
chart.set_x_axis({"name": "Generación"})
chart.set_y_axis({"name": "Puntaje"})
chart.set_style(10)
summarySheet.insert_chart("D1", chart, {"x_scale": 1.9, "y_scale": 1.85})

# Imprimir resultado final en pantalla
print("Resultado\n Cromosoma: {chrom}\n Valor entero: {value}\n Objetivo: {score}\n Fitness: {fitness}"
	.format(
		chrom = resultChrom.asString(),
		value = resultChrom.value,
		score = resultChrom.score,
		fitness = resultChrom.fitness))
workbook.close()
print("Resultados guardados en {}".format(filename))
input("Presione una tecla para cerrar...")