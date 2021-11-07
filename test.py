from random import randint, random
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
                #print("Current: ", current_weight)
                #print("Weight: ", weight_bag)
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
    #maior preco por kg possivel é 100 (price_max)
    #print("AQUI")
    price = [ items_list[item][1] for item in range(items_length) if individual[item] == 1 ]     
    # file.write(str(pricePweight))
    sum = reduce(add, price, 0)
    return sum

def media_fitness(pop, items_list, items_length):
    'Find average fitness for a population.'
    summed = reduce(add, (fitness(x, items_list, items_length) for x in pop))
    return summed / (len(pop) * 1.0)


def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.01):
    'Tabula cada individuo e o seu fitness'
    graded = [ (fitness(x, target), x) for x in pop]
    'Ordena pelo fitness os individuos - menor->maior'
    graded = [ x[1] for x in sorted(graded)]
    'calcula qtos serao elite'
    retain_length = int(len(graded)*retain)
    'elites ja viram pais'
    parents = graded[:retain_length]
    # randomly add other POUCOS individuals to
    # promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)
    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            individual[pos_to_mutate] = randint(
                min(individual), max(individual))
    # crossover parents to create children
    parents_length = len(parents)
    'descobre quantos filhos terao que ser gerados alem da elite e aleatorios'
    desired_length = len(pop) - parents_length
    children = []
    'comeca a gerar filhos que faltam'
    while len(children) < desired_length:
        'escolhe pai e mae no conjunto de pais'
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) // 2
            'gera filho metade de cada'
            child = male[:half] + female[half:]
            'adiciona novo filho a lista de filhos'
            children.append(child)
    'adiciona a lista de pais (elites) os filhos gerados'
    parents.extend(children)
    return parents


# Objetivo: achar um vetor de inteiros (entre i_min e i_max) com i_length posicoes cuja a soma de todos os termos seja o mais proximo possivel de target

#O algoritmo rodara epochs vezes -> numero de populacoes geradas. Sera impresso a media de fitness de cada uma das epochs populacoes

#RODAR COM PYTHON 2!!! (senao colocar () em print e tirar x de xrange

target = 3700
i_length = 30
i_min = 0
i_max = 1000
p_count = 100
epochs = 30
p = population(p_count, i_length, i_min, i_max)
fitness_history = [media_fitness(p, target),]
for i in range(epochs):
    p = evolve(p, target)
    fitness_history.append(media_fitness(p, target))

for datum in fitness_history:
   print (datum)
