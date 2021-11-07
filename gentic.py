from math import floor
from random import randint, random, choice, uniform
from operator import add
from functools import reduce

def individual(weight_bag, items_length, items_list):
    'Create a member of the population.'
    bag = [0] * items_length
    aux_list = [0] * items_length
    current_weight = 0

    # Não ta otimizado
    while (current_weight < weight_bag) and (0 in aux_list):
        item_index = randint(0, items_length-1)
        new_item = items_list[item_index]
        if new_item[0] + current_weight <= weight_bag and aux_list[item_index] != 1:
            if bag[item_index] != 1:
                bag[item_index] = 1
                current_weight += new_item[0]
        aux_list[item_index] = 1
    return bag

def population(count, items_length, items_list, weight_bag):
    """
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the minimum possible value in an individual's list of values
    max: the maximum possible value in an individual's list of values
    """
    return [ individual(weight_bag, items_length, items_list) for x in range(count) ]

def fitness(individual, items_list, items_length):
    """
    Determine the fitness of an individual. Higher is better.

    individual: the individual to evaluate
    target: the target number individuals are aiming for

    O fitness do individuo perfeito sera ZERO, ja que o somatorio dara o target
    reduce: reduz um vetor a um escalar, neste caso usando o operador add
    """
    price = [ items_list[item][1] for item in range(items_length) if individual[item] == 1 ]     
    sum = reduce(add, price, 0)
    return sum

def media_fitness(pop, items_list, items_length):
    'Find average fitness for a population.'
    summed = reduce(add, (fitness(x, items_list, items_length) for x in pop))
    return summed / (len(pop) * 1.0)

def evolve(pop, items_list, items_length, weight_bag, retain=0.2, mutate=0.01):
    'Tabula cada individuo e o seu fitness'
    graded = [ (fitness(x, items_list, items_length), x) for x in pop]
    'Ordenar o grade em ordem crescente de fitness'
    graded = [ x for x in sorted(graded, reverse=True)]
    ''
    fitness_list = [graded[x][0]*(x+1) for x in range(len(graded))]

    'cria variveis auxiliares'
    parents = []
    probability = []
    sum_fitness = reduce(add, fitness_list, 0)
    prev_value = 0
    
    'lista de intervalos de probabilidade'
    for i in fitness_list:
        new_probability = prev_value + ((i/sum_fitness))
        probability.append(new_probability)
        prev_value = new_probability

    'Metodo da roleta para selecionar os parents'
    for parent in range(int(retain * len(pop))):
        random_number = uniform(0, probability[-1])
        for i in range(len(probability)):
            if random_number <= probability[i]:
                parents.append(graded[parent][1])
                break

    'mutate some individuals'
    for x in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(parents)-1)
            parents[pos_to_mutate] = individual(weight_bag, items_length, items_list)

    # 'crossover parents to create children'
    # 'descobre quantos filhos terao que ser gerados alem da elite e aleatorios'
    desired_length = len(pop) - len(parents)
    children = []
    # 'comeca a gerar filhos que faltam'
    while len(children) < desired_length:
    #     'escolhe pai e mae no conjunto de pais'
        male = randint(0, len(parents)-1)
        female = randint(0, len(parents)-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) // 2
            'gera filho metade de cada'
            child1 = male[:half] + female[half:]
            child2 = male[half:] + female[:half] 
            'adiciona novo filho a lista de filhos'
            children.append(child1)
            children.append(child2)
    parents.extend(children)
    return parents



#########################################################################################
 #from genetic2020 import *
items_length = 1000     #1000
weight_bag = 2000       #2000  #tamanho da matriz de itens e vetor da mochila
weight_min = 1      
weight_max = 50
price_min = 1
price_max = 100
p_count = 100           #elementos da população
epochs = 30             #30

#Lista de itens é criada aqui, pois ela é igual para toda população
items_list = [(randint(weight_min, weight_max), randint(price_min, price_max)) for x in range(items_length)]

p = population(p_count, items_length, items_list, weight_bag)

fitness_history = [media_fitness(p, items_list, items_length),]

for i in range(epochs-1):
    p = evolve(p, items_list, items_length, weight_bag)
    fitness_history.append(media_fitness(p, items_list, items_length)) #media de fitness da geração, ou seja a media do fitness dos 100 da população

media=0
for datum in fitness_history:
    print (datum)
    media+=datum
print ('Media: ', (media/epochs))


    


