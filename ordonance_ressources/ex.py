from random import shuffle, random, randint, randrange
from itertools import accumulate

def evaluer(chromosome, capacites_unites, demande, capacite_totale):
    reserves = [capacite_totale - d for d in demande]
    for u, gene in enumerate(chromosome):
        for i in range(4):
            if gene[i] == "1":
                reserves[i] -= capacites_unites[u]
    return max(min(reserves), 0)

def encoder(nb_intervalles_par_unite):
    chromosome = []
    for n in nb_intervalles_par_unite:
        T = ["1"] * n + ["0"] * (4 - n)
        shuffle(T)
        chromosome.append("".join(T))
    return chromosome

def generer_generation_initiale(nb_intervalles_par_unite, nb_individus):
    return [encoder(nb_intervalles_par_unite) for _ in range(nb_individus)]

def calcul_fitness(generation, capacites_unites, demande, capacite_totale):
    return [evaluer(ind, capacites_unites, demande, capacite_totale) for ind in generation]

def croisement(p1, p2):
    a,b= randint(1,len(p1)-1), randint(1,len(p2)-1)
    while (a==b):
        a,b= randint(1,len(p1)-1), randint(1,len(p2)-1)
    point1 = min(a,b)
    point2 = max(a,b)
    fils1 = p1[:point1] + p2[point1:point2] + p1[point2:]
    fils2 = p2[:point1] + p1[point1:point2] + p2[point2:]
    return fils1,fils2

def mutation(chromosome, probabilite_mutation=10**(-2)):
    resultat = []
    for gene in chromosome:
        if random() < probabilite_mutation:
            g = list(gene)
            a, b = randrange(4), randrange(4)
            g[a], g[b] = g[b], g[a]
            gene = "".join(g)
        resultat.append(gene)
    return resultat

def selection_roulette(generation, capacites_unites, demande, capacite_totale):
    fit = calcul_fitness(generation, capacites_unites, demande, capacite_totale)
    F = sum(fit)
    p = [f / F if F != 0 else 1 / len(fit) for f in fit]
    q = list(accumulate(p))
    q[-1] = 1.0
    selectionnes = []
    for _ in range(len(generation)):
        r = random()
        for j in range(len(q)):
            if r <= q[j]:
                selectionnes.append(generation[j])
                break
    shuffle(selectionnes)
    return selectionnes

def algo_genetique(nb_intervalles_par_unite, nb_individus, capacites_unites, demande, capacite_totale, nb_generations=100):
    generation = generer_generation_initiale(nb_intervalles_par_unite, nb_individus)
    meilleur, meilleur_score = None, -1
    for _ in range(nb_generations):
        for ind in generation:
            s = evaluer(ind, capacites_unites, demande, capacite_totale)
            if s > meilleur_score:
                meilleur_score, meilleur = s, ind[:]
        selectionnes = selection_roulette(generation, capacites_unites, demande, capacite_totale)
        new_generation = []
        for i in range(0, len(selectionnes) - 1, 2):
            f1, f2 = croisement(selectionnes[i], selectionnes[i + 1])
            new_generation.append(mutation(f1))
            new_generation.append(mutation(f2))
        while len(new_generation) < nb_individus:
            new_generation.append(meilleur[:])
        generation = new_generation
    for ind in generation:
        s = evaluer(ind, capacites_unites, demande, capacite_totale)
        if s > meilleur_score:
            meilleur_score, meilleur = s, ind[:]
    return meilleur_score, meilleur

if __name__ == "__main__":
    CAPACITES = [20, 15, 35, 40, 15, 15, 10]
    NB_INTERVALLES = [2, 2, 1, 1, 1, 1, 1]
    NB_INDIVIDUS = 20
    DEMANDE = [80, 90, 65, 70]
    CAPACITE_TOTALE = sum(CAPACITES)
    maxx, chromosome = algo_genetique(NB_INTERVALLES, NB_INDIVIDUS, CAPACITES, DEMANDE, CAPACITE_TOTALE)
    print(f"solution {chromosome} avec cout {maxx}")