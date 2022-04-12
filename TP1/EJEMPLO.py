from lib2to3.pgen2.token import COMMENT
import numpy as np
import random

class DNA():
    def __init__(self, target, mutation_rate, n_individuals, n_selection, n_generation, verbose=True):
        self.target = target
        self.mutation_rate = mutation_rate
        self.n_individuals = n_individuals
        self.n_selection = n_selection
        self.n_generation = n_generation
        self.verbose = verbose
        
    def create_individual(self, min=0, max=1):
        # CREA EL INDIVIDUO
        individual = [np.random.randint(min, max) for i in range(len(self.target))]
        return individual
    
    def create_population(self):
        # CREA EL INDIVIDUO
        population = [self.create_individual() for i in range(self.n_individuals)]
        return population
    
    def fitness(self, individual):
        # EVALUA EL INDIVIDUO
        fitness = 0
        for i in range(len(individual)):
            if individual[i] == self.target[i]:
                fitness += 1
        return fitness
    
    def selection(self, population):
        scores = [(self.fitness(i), i) for i in population]
        scores = [(i[1]) for i in sorted(scores)]
        selected = scores[len(scores) - self.n_selection :]
        return selected
    
    def reproduction(self, population, selected):
        point = 0
        father = []
        for i in range(len(population)):
            point += np.random.randint(1,len(self.target)-1)
            father = random.sample(selected,2)
            population[i][:point] = father[0][:point]
            population[i][point:] = father[1][point:]
        return population
        
    def mutation(self, population):
        for i in range(len(population)):
            if random.random() <= self.mutation_rate:
                point = random.randint(1,len(self.target)-1)
                new_value = np.random.randint(0,9)
                while new_value == population[i][point]:
                    new_value = np.random.randint(0,9)
                population[i][point] = new_value
        return population
    
    def run_geneticalgo(self):
        population = self.create_population()
        for i in range(self.n_generation):
            if self.verbose:
                print('___________')
                print('Generacion',i)
                print('Poblacion', population)
            selected = self.selection(population)
            population = self.reproduction(population,selected)
            population = self.mutation(population)
            
                        
def main():
    target = [1 , 0 , 0 , 1 , 0 ]
    model = DNA(target = target, mutation_rate = 0.2, n_individuals = 100, n_selection = 5, n_generation = 50, verbose = True)
    model.run_geneticalgo()
            
if __name__ == '__main__':
    main()