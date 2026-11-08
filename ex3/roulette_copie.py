from random import randint, random, shuffle


def f(s, villes):
    """Coût d'un trajet. Retourne l'infini si le trajet emprunte une arête absente."""
    somme = 0
    for i in range(len(villes)):
        a = s[i] - 1
        b = s[(i + 1) % len(villes)] - 1  # retourner au point de départ
        if villes[a][b] == -1:
            return float("inf")
        somme += villes[a][b]
    return somme


def estValide(s, villes):
    return f(s, villes) != float("inf")


def calculFitness(generation, villes):
    """Fitness de chaque individu : d'autant plus grande que le coût est petit."""
    fitness = []
    for individu in generation:
        cout = f(individu, villes)
        if cout == float("inf"):
            fitness.append(0.0)
        else:
            fitness.append(1.0 / (1.0 + cout))
    return fitness


def generer_initial(nb, villes):
    """Génère nb trajets valides (permutations des villes) sans doublon."""
    liste = []
    depart = list(range(1, len(villes) + 1))
    essais = 0
    while len(liste) < nb and essais < 10000:
        essais += 1
        shuffle(depart)
        if not estValide(depart, villes):
            continue
        if depart in liste:
            continue
        liste.append(depart[:])

    # Sécurité : si le graphe est très contraint, on duplique des trajets valides.
    while len(liste) < nb:
        liste.append(liste[randint(0, len(liste) - 1)][:])
    return liste


def selection_roulette(generation, villes):
    """Sélection par roulette : probabilité proportionnelle à la fitness."""
    fitness = calculFitness(generation, villes)
    total = sum(fitness)

    # Si aucun individu valide, on tire uniformément.
    if total == 0:
        return generation[randint(0, len(generation) - 1)][:]

    probabilites = []
    cumul = 0.0
    for valeur in fitness:
        cumul += valeur / total
        probabilites.append(cumul)

    r = random()
    for i in range(len(probabilites)):
        if r <= probabilites[i]:
            return generation[i][:]
    return generation[-1][:]


def crossover(pere1, pere2):
    """Croisement ordonné (OX) : conserve une permutation valide."""
    n = len(pere1)
    a = randint(0, n - 1)
    b = randint(0, n - 1)
    if a > b:
        a, b = b, a

    fils1 = [None] * n
    fils2 = [None] * n
    fils1[a:b + 1] = pere1[a:b + 1]
    fils2[a:b + 1] = pere2[a:b + 1]

    def completer(fils, parent):
        position = (b + 1) % n
        for i in range(n):
            gene = parent[(b + 1 + i) % n]
            if gene not in fils:
                fils[position] = gene
                position = (position + 1) % n

    completer(fils1, pere2)
    completer(fils2, pere1)
    return fils1, fils2


def mutate(trajet, taux_mutation=0.1):
    """Mutation par échange de deux villes avec probabilité taux_mutation."""
    trajet = trajet[:]
    if random() < taux_mutation:
        x = randint(0, len(trajet) - 1)
        y = randint(0, len(trajet) - 1)
        while y == x:
            y = randint(0, len(trajet) - 1)
        trajet[x], trajet[y] = trajet[y], trajet[x]
    return trajet


def roulette(villes, taille_population=50, nb_generations=200,
             taux_mutation=0.1, nb_elites=2):
    """Algorithme génétique avec sélection par roulette.

    Retourne le meilleur trajet trouvé.
    """
    population = generer_initial(taille_population, villes)
    population.sort(key=lambda s: f(s, villes))
    meilleur = population[0][:]

    for _ in range(nb_generations):
        # Élitisme : on garde les meilleurs individus d'une génération à l'autre.
        nouvelle_generation = [population[i][:] for i in range(nb_elites)]

        while len(nouvelle_generation) < taille_population:
            pere1 = selection_roulette(population, villes)
            pere2 = selection_roulette(population, villes)
            fils1, fils2 = crossover(pere1, pere2)
            nouvelle_generation.append(mutate(fils1, taux_mutation))
            if len(nouvelle_generation) < taille_population:
                nouvelle_generation.append(mutate(fils2, taux_mutation))

        population = nouvelle_generation
        population.sort(key=lambda s: f(s, villes))
        if f(population[0], villes) < f(meilleur, villes):
            meilleur = population[0][:]

    return meilleur


def main():
    villes = [
        [-1, 14, 15, -1, -1, -1, -1, 17],
        [14, -1, 13, 14, 20, -1, -1, 21],
        [15, 13, -1, 11, 21, 17, 9, 9],
        [-1, 14, 11, -1, 11, 10, 8, 20],
        [-1, 20, 21, 11, -1, 15, 18, -1],
        [-1, -1, 17, 10, 15, -1, 9, -1],
        [-1, -1, 9, 8, 18, 9, -1, 13],
        [17, 21, 9, 20, -1, -1, 13, -1]
    ]
    s = roulette(villes)
    print(f"le chemin est {s}")
    print(f"le cout est {f(s, villes)}")


if __name__ == "__main__":
    main()
