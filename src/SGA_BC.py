# -*- coding: utf-8 -*-
"""
SGA_BC.py
Simple Genetic Algorithm for the Brachistochrone Curve problem.
Pedro Geadas, May, 2011.
"""

import csv
import random
from operator import itemgetter

import math

from BrachFitness import *


def sga(numb_genera, size_pop, num_pontos, alphabet, size_tournament, prob_crossover, n_crossover, prob_mutation,
        size_elite, selection_mode, spacement, mut_type, times):
    total = 0.0
    file = open('population_alldata.txt', 'w', encoding='utf-8')
    file2 = open('population_avg.txt', 'w', encoding='utf-8')
    count_mutation = 0
    count_crossover = 0
    avg_pop = 0.0
    pop_times = 0.0
    the_less_fitest = 0.0
    the_fitest = float('inf')
    the_best = 0.0
    the_worst = 0.0
    af = []
    dp = []
    total_mut = total_cross = 0
    result_file = open('results.csv', 'w', newline='', encoding='utf-8')
    resultWriter = csv.writer(result_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # create initial population
    population = create_population(size_pop, alphabet, num_pontos, spacement)

    desvio = 0.0

    for vezes in range(times):
        # evaluate population
        population = [[indiv[0], calcBrachTime(indiv[0], False)] for indiv in population]
        best_generation = [population[0][1]]
        count_mutation = count_crossover = 0

        for generation in range(numb_genera):
            # Select parents
            if selection_mode == 1:
                parents = [tournament_selection(population, size_tournament) for _ in range(size_pop)]
            else:
                total = sum(indiv[1] for indiv in population)
                parents = [roulette_selection(population, size_tournament, total) for _ in range(size_pop)]

            # Produce offspring
            # a) crossover
            offspring = []
            for i in range(0, size_pop, 2):  # population must have an even size...
                if random.random() < prob_crossover:
                    offspring.extend(n_point_crossover(parents[i], parents[i + 1], n_crossover, spacement))
                    count_crossover += 2
                    total_cross += 2
                else:
                    offspring.extend([parents[i], parents[i + 1]])

            # b) mutation
            for j in range(size_pop):
                if random.random() < prob_mutation:
                    if spacement == 1:
                        if mut_type == 2:
                            offspring[j] = mutation_gaussian(offspring[j][0], alphabet)
                        else:
                            offspring[j] = mutation(offspring[j][0], alphabet)
                    else:
                        if mut_type == 2:
                            offspring[j] = mutation_gaussian_xy(offspring[j][0], alphabet)
                        else:
                            offspring[j] = mutation(offspring[j][0], alphabet)
                    count_mutation += 1
                    total_mut += 1

            # Evaluate offspring
            offspring = [[indiv[0], calcBrachTime(indiv[0], False)] for indiv in offspring]
            offspring.sort(key=itemgetter(1))
            # Select Survivors
            population = elitism_selection(population, offspring, size_elite)
            # show best
            population.sort(key=itemgetter(1))
            best_generation.append(population[0][1])

        pop_times = 0.0
        for indiv in population:
            if indiv[1] > the_less_fitest:
                the_less_fitest = indiv[1]
            if indiv[1] < the_fitest:
                the_fitest = indiv[1]
            pop_times += indiv[1]

        avg_pop += pop_times / float(len(population))  # (xBarra)

        s = 0.0
        sBarra = pop_times / float(len(population))

        for indiv in population:
            s += (indiv[1] - sBarra) ** 2

        s = math.sqrt(s * (1 / float((len(population) - 1)))) if len(population) > 1 else 0.0

        desvio += s
        dp.append(s)
        print(s)
        print(desvio)
        print(desvio / times)

        avg_pop_str = f"AVG POP {vezes}, is {pop_times / len(population):.6f}!"
        print(avg_pop_str)
        file.write(avg_pop_str + '\n')

        desvio_str = f"DESVIO PADRAO: {s:.6f}!"
        print(desvio_str)
        file.write(desvio_str + '\n')

        crossovers_str = f"Crossovers: {count_crossover}"
        print(crossovers_str)
        file.write(crossovers_str + '\n')

        mutations_str = f"Mutations: {count_mutation}"
        print(mutations_str)
        file.write(mutations_str + '\n')

        cross_mut_str = f"Crossovers:{total_cross}\tMutations:{total_mut}"
        print(cross_mut_str)
        file.write(cross_mut_str + '\n')

        best_fit_str = f"the_best_fitness {population[0][1]!r}"
        print(best_fit_str)
        file.write(best_fit_str + '\n')

        worst_fit_str = f"the_worst_fitness {population[-1][1]!r}"
        print(worst_fit_str)
        file.write(worst_fit_str + '\n')

        fitest_str = f"THE FITEST {the_fitest:.6f}"
        print(fitest_str)
        file.write(fitest_str + '\n')

        less_fitest_str = f"THE LESS FITEST {the_less_fitest:.6f}\n"
        print(less_fitest_str)
        file.write(less_fitest_str + '\n')

        the_best += population[0][1]
        the_worst += population[-1][1]
        print(vezes)
        print(desvio / times)
        af.append(pop_times / len(population))

    mean_sd_str = f"desvio padrão médio: {desvio / float(times):.6f} "
    print(mean_sd_str)
    file2.write(mean_sd_str + '\n')

    mean_best_str = f"aptidao media do melhor {times} vezes: {the_best / times:.6f} "
    print(mean_best_str)
    file2.write(mean_best_str + '\n')

    mean_worst_str = f"aptidao media do worst {times} vezes: {the_worst / times:.6f} "
    print(mean_worst_str)
    file2.write(mean_worst_str + '\n')

    avg_total_pop_str = f"AVG TOTAL POPULATION: {avg_pop / times:.6f} "
    print(avg_total_pop_str)
    file2.write(avg_total_pop_str + '\n')

    fitest_str = f"THE FITEST {the_fitest:.6f}"
    print(fitest_str)
    file2.write(fitest_str + '\n')

    least_fit_str = f"THE LEAST FIT {the_less_fitest:.6f}"
    print(least_fit_str)
    file2.write(least_fit_str + '\n')

    af.sort(reverse=True)
    resultWriter.writerow(af)
    resultWriter.writerow(dp)
    file.close()
    file2.close()
    result_file.close()
    return [best_generation, population[0][0], population]


def create_indiv_random_spacement(alphabet, num_pontos):
    indiv = []
    maxHeight = alphabet[1]
    x_max = alphabet[2]
    x_0 = alphabet[0]
    xx = []
    yy = []

    indiv.extend([x_0, maxHeight])

    while len(xx) != (num_pontos) - 2:
        new_x = random.uniform(x_0, x_max)
        while new_x <= x_0 or new_x >= x_max:
            new_x = random.uniform(x_0, x_max)
        if new_x not in xx:
            xx.append(new_x)

    while len(yy) != (num_pontos) - 2:
        new_y = random.uniform(0, alphabet[1] + alphabet[3]) - alphabet[3]
        while new_y >= maxHeight:
            new_y = random.uniform(0, alphabet[1] + alphabet[3]) - alphabet[3]
        if new_y not in yy:
            yy.append(new_y)

    xx.sort()
    for i in range(len(xx)):
        point = [xx[i], yy[i]]
        indiv.extend(point)

    point = [alphabet[2], alphabet[3]]
    indiv.extend(point)
    return [indiv, 0]


def create_indiv_same_spacement(alphabet, num_pontos):
    indiv = []
    maxHeight = alphabet[1]
    indiv.extend([alphabet[0], alphabet[1]])
    offset = (alphabet[2] - alphabet[0]) / num_pontos
    i = offset + alphabet[0]

    while len(indiv) != (num_pontos * 2) - 2:
        point = [i, random.uniform(0, alphabet[1] + alphabet[3]) - alphabet[3]]
        while point[1] >= maxHeight:
            point = [i, random.uniform(0, alphabet[1] + alphabet[3]) - alphabet[3]]
        indiv.extend(point)
        i = i + offset

    point = [alphabet[2], alphabet[3]]
    indiv.extend(point)
    return [indiv, 0]


def create_population(size_pop, alphabet, num_pontos, spacement):
    if spacement == 1:
        pop = [create_indiv_same_spacement(alphabet, num_pontos) for _ in range(size_pop)]
    else:
        pop = [create_indiv_random_spacement(alphabet, num_pontos) for _ in range(size_pop)]
    print('a pop e' + repr(pop))
    return pop


def tournament_selection(population, size_tournament):
    tournament = random.sample(population, size_tournament)
    tournament.sort(key=itemgetter(1))
    return tournament[0]


def roulette_selection(population, size_tournament, total):
    new_total = 0
    probab = [0.0]
    roulette = []
    tam = len(population)

    for i in range(tam):
        inverte = (total - population[i][1]) / total
        probab.append(probab[i] + inverte)
        new_total += inverte

    probab[-1] = new_total
    probab.pop(0)

    x = random.random() * new_total
    for i in range(tam):
        if x < probab[i]:
            roulette.append(population[i])
            break
    return roulette[0]


def elitism_selection(parents, offspring, size_elite):
    size = int(len(parents) * size_elite)
    new_pop = parents[:size] + offspring[:len(parents) - size]
    new_pop.sort(key=itemgetter(1))
    return new_pop


def mutation(indiv, alphabet):
    index = random.choice(list(range(4, len(indiv) - 2)))
    if index % 2 == 0:
        index = index - 1

    new_gene = random.uniform(0, alphabet[1] + alphabet[3]) - alphabet[3]
    while new_gene > indiv[1]:
        new_gene = random.uniform(0, alphabet[1] + alphabet[3]) - alphabet[3]

    indiv[index] = new_gene
    return [indiv, 3]


def mutation_gaussian(indiv, alphabet):
    index = random.choice(list(range(4, len(indiv) - 2)))
    if index % 2 == 0:
        index = index - 1
    new_gene = random.gauss(0, 1) + indiv[index]
    while new_gene > indiv[1]:
        new_gene = random.gauss(0, 1) + indiv[index]
    indiv[index] = new_gene
    return [indiv, 3]


def mutation_gaussian_xy(indiv, alphabet):
    index = random.choice(list(range(4, len(indiv) - 2)))
    if index % 2 == 0:
        new_gene = random.gauss(0, 1) + indiv[index]
        while new_gene > indiv[index + 2] or new_gene < indiv[index - 2]:
            new_gene = random.gauss(0, 1) + indiv[index]
    else:
        new_gene = random.gauss(0, 1) + indiv[index]
        while new_gene > indiv[1]:
            new_gene = random.gauss(0, 1) + indiv[index]
    indiv[index] = new_gene
    return [indiv, 3]


def n_point_crossover(parent_1, parent_2, n_crossover, spacement):
    if n_crossover > 0:
        if spacement == 1:
            return crossover_same_spacement(parent_1, parent_2, n_crossover)
        else:
            return crossover_random_spacement(parent_1, parent_2, n_crossover)
    else:
        return [[parent_1, 0], [parent_2, 0]]


def crossover_same_spacement(parent_1, parent_2, n_crossover):
    offspring_1 = []
    offspring_2 = []
    cross_point = []

    ptr = [parent_1[0], parent_2[0]]
    while len(cross_point) != n_crossover:
        x = random.choice(list(range(len(parent_1[0]) // 2 - 1)))
        if x not in cross_point and x != 0 and x != (len(parent_1[0]) // 2 - 1) and x != 1:
            cross_point.append(x)

    cross_point.extend([0, len(parent_1[0]) // 2])
    cross_point.sort()

    pai = 0
    i = 0
    offspring_1.extend(ptr[pai][cross_point[i] * 2:cross_point[(i + 1)] * 2])
    pai = (pai + 1) % 2
    offspring_2.extend(ptr[pai][cross_point[i] * 2:cross_point[(i + 1)] * 2])
    i = i + 1

    while True:
        if i >= len(cross_point) - 1:
            break
        else:
            offspring_1.extend(ptr[pai][cross_point[i] * 2:cross_point[(i + 1)] * 2])
            pai = (pai + 1) % 2
            offspring_2.extend(ptr[pai][cross_point[i] * 2:cross_point[(i + 1)] * 2])
        i = i + 1

    return [[offspring_1, 1], [offspring_2, 2]]


def crossover_random_spacement(parent_1, parent_2, n_crossover):
    offspring_1 = []
    offspring_2 = []
    cross_point = []

    ptr = [parent_1[0], parent_2[0]]
    while len(cross_point) != n_crossover:
        x = random.choice(list(range(len(parent_1[0]) // 2 - 1)))
        if x not in cross_point and x != 0 and x != (len(parent_1[0]) // 2 - 1) and x != 1:
            cross_point.append(x)

    cross_point.extend([0, len(parent_1[0]) // 2])
    cross_point.sort()

    pai = 0
    i = 0
    offspring_1.extend(ptr[pai][cross_point[i] * 2:cross_point[(i + 1)] * 2])
    pai = (pai + 1) % 2
    offspring_2.extend(ptr[pai][cross_point[i] * 2:cross_point[(i + 1)] * 2])
    i = i + 1

    while True:
        if i >= len(cross_point) - 1:
            break
        else:
            element_aux = ptr[pai][cross_point[i] * 2:cross_point[(i + 1)] * 2]
            while len(element_aux) != 0:
                if offspring_1[-2] < element_aux[0]:
                    offspring_1.append(element_aux.pop(0))
                    offspring_1.append(element_aux.pop(0))
                elif offspring_1[-2] >= element_aux[0]:
                    for k in range(len(offspring_1) - 2, -2, -2):
                        if element_aux[0] > offspring_1[k]:
                            offspring_1.insert(k + 2, element_aux.pop(0))
                            offspring_1.insert(k + 1 + 2, element_aux.pop(0))
                            break
                        elif element_aux[0] == offspring_1[k]:
                            x_actual = offspring_1[-4] if offspring_1[-2] == element_aux[0] else offspring_1[-2]
                            x_max = element_aux[0]
                            new_x = random.uniform(x_actual, x_max)
                            while new_x in offspring_1 or new_x in element_aux:
                                new_x = random.uniform(x_actual, x_max)
                            element_aux[0] = new_x
                            break

            pai = (pai + 1) % 2
            element_aux = ptr[pai][cross_point[i] * 2:cross_point[(i + 1)] * 2]
            while len(element_aux) != 0:
                if offspring_2[-2] < element_aux[0]:
                    offspring_2.append(element_aux.pop(0))
                    offspring_2.append(element_aux.pop(0))
                elif offspring_2[-2] >= element_aux[0]:
                    for k in range(len(offspring_2) - 2, -2, -2):
                        if element_aux[0] > offspring_2[k]:
                            offspring_2.insert(k + 2, element_aux.pop(0))
                            offspring_2.insert(k + 1 + 2, element_aux.pop(0))
                            break
                        elif element_aux[0] == offspring_2[k]:
                            x_actual = offspring_2[-4] if offspring_2[-2] == element_aux[0] else offspring_2[-2]
                            x_max = element_aux[0]
                            new_x = random.uniform(x_actual, x_max)
                            while new_x in offspring_2 or new_x in element_aux:
                                new_x = random.uniform(x_actual, x_max)
                            element_aux[0] = new_x
                            break
        i = i + 1

    return [[offspring_1, 1], [offspring_2, 2]]
