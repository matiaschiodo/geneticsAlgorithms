import numpy as np
import random

class DNA:
    def __init__(self, target, prob_mutacion, individuos, seleccionados, n_generations, verbose = True):
        self.target = target
        self.prob_mutacion = prob_mutacion
        self.individuos = individuos
        self.seleccionados = seleccionados
        self.generaciones = generaciones
        self.verbose = verbose


    def crear_individuo(self):
        return [np.random.randint(0,1) for i in range(len(self.target))]

    def crear_poblacion(self):
        return [self.crear_individuo() for i in range(self.individuos)]


    def fitness(self, individuo):
        fitness = objetivo.individuo

        for i in range(len(individuo)):
            if individuo[i] == self.target[i]:
                fitness += 1
        
        return fitness
    
    def seleccion_ruleta(poblacion):

        fitness = sum([individuo.fitness for individuo in poblacion])
        individuo_probabilidad = [(individuo.fitness*100) for individuo in poblacion] 
        return np.random.choice(poblacion = individuo_probabilidad)

    """def selection(self, poblacion): 'seleccion normal'

        scores = [(self.fitness(i), i) for i in poblacion]
        scores = [i[1] for i in sorted(scores)]

        return scores[len(scores)-self.seleccionados:]"""
    
    def reproduction(self, poblacion, selected):

        point = 0
        father = []

        for i in range(len(poblacion)):
            point = np.random.randint(1, len(self.target) - 1)
            father = random.sample(selected, 2)

            poblacion[i][:point] = father[0][:point]
            poblacion[i][point:] = father[1][point:]
        
        return poblacion
    
    def mutation(self, poblacion):
        
        for i in range(len(poblacion)):
            if random.random() <= self.prob_mutacion:
                point = np.random.randint(len(self.target))
                new_value = np.random.randint(0, 9)

                while new_value == poblacion[i][point]:
                    new_value = np.random.randint(0, 9)
                
                poblacion[i][point] = new_value
            return poblacion
    
    def run_geneticalgo(self):
        poblacion = self.crear_poblacion()

        for i in range(self.n_generations):

            if self.verbose:
                print('___________')
                print('Generacion: ', i)
                print('Poblacion', poblacion)
                print()

            selected = self.selection(poblacion)
            poblacion = self.reproduction(poblacion, selected)
            poblacion = self.mutation(poblacion)

def main():
    target = [1,1,1,1,1]
    model = DNA(
        target = target,
        prob_mutacion = 0.05,
        prob_crossover = 0.75,
        individuos = 10,
        seleccionados = 10,
        generaciones = 20,
        verbose=True)
    model.run_geneticalgo()

    
if __name__ == '__main__':
    main()