from random import randint, randrange,random,shuffle
from itertools import accumulate

def generer_generation_initiale(nb_packs,n=8):
    generation_initiale = []
    for i in range(n):
        ind = ""
        for j in range(nb_packs):
            ind += str(randint(0,1))
        generation_initiale.append(ind)
    return generation_initiale

def evaluer(individu,poids,valeur,capacite_sac):
    somme = 0
    poids_total = 0
    for i in range(len(individu)):
        poids_total += int(individu[i])*poids[i]
        somme += int(individu[i])*valeur[i]
    if poids_total > capacite_sac:
        return 0
    return somme
def calcul_fitness(generation,poids,valeur,capacite_sac):
    return [evaluer(individu,poids,valeur,capacite_sac) for individu in generation]

def croisement(p1, p2):
    a,b= randint(1,len(p1)-1), randint(1,len(p2)-1)
    while a==b :
        a,b= randint(1,len(p1)-1), randint(1,len(p2)-1)
    point1 = min(a,b)
    point2 = max(a,b)
    fils1 = p1[:point1] + p2[point1:point2] + p1[point2:]
    fils2 = p2[:point1] + p1[point1:point2] + p2[point2:]
    return fils1,fils2

def mutation(chromosome, probabilite_mutation=10**(-2)):
    genes = [*chromosome]
    for i in range(len(genes)):
        if random() < probabilite_mutation:
            genes[i] = "1" if genes[i] == "0" else "0"

    return "".join(genes)

def selection_roulette(generation,poids,valeur,capacite_sac):
    fit = calcul_fitness(generation,poids,valeur,capacite_sac)
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

def algo_genetique(poids,valeur,capacite_sac):
    generation = generer_generation_initiale(len(poids))
    meilleur, meilleur_score = None, -1
    for _ in range(8):
        for ind in generation:
            s = evaluer(ind,poids,valeur,capacite_sac)
            if s > meilleur_score:
                meilleur_score, meilleur = s, ind[:]
        selectionnes = selection_roulette(generation,poids,valeur,capacite_sac)
        new_generation = []
        for i in range(0, len(selectionnes) - 1, 2):
            f1, f2 = croisement(selectionnes[i], selectionnes[i + 1])
            new_generation.append(mutation(f1))
            new_generation.append(mutation(f2))
        generation = new_generation[:]
    for ind in generation:
        s = evaluer(ind,poids,valeur,capacite_sac)
        if s > meilleur_score:
            meilleur_score, meilleur = s, ind[:]
    return meilleur_score, meilleur

if __name__=="__main__":
    capacite_sac = 100
    poids = [8,7,10,25,30,10,8,2,7,9]
    valeurs = [20,24,2,70,60,20,30,15,40,25]
    meilleur_score, meilleur = algo_genetique(poids, valeurs, capacite_sac)
    print(meilleur_score)
