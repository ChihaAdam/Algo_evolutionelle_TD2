from random import randint, random


def f(individu,poids,valeur,capacite_sac):
    somme = 0
    poids_total = 0
    for i in range(len(individu)):
        poids_total += int(individu[i])*poids[i]
        somme += int(individu[i])*valeur[i]
    if poids_total > capacite_sac:
        return 0
    return somme

def generer_population_initiale(nb_packs,n=8):
    generation_initiale = []
    for i in range(n):
        ind = ""
        for j in range(nb_packs):
            ind += str(randint(0,1))
        generation_initiale.append(ind)
    return generation_initiale

def calcul_vitesse_a_t_plus_1(x,v,p,g,inertie,congnitive,sociale):
    new_v = []
    for i in range(len(v)):
        r1 = random()
        r2 = random()
        b1 = r1*congnitive
        b2 = r2*sociale
        new_v.append(inertie*v[i] + b1*(p[i]-x[i]) + b2*(g-x[i]))
    return new_v

def calcul_a_t_plus_1(x,v,p,g,inertie,congnitive,sociale):
    new_v = calcul_vitesse_a_t_plus_1(x,v,p,g,inertie,congnitive,sociale)
    new_x = [x[i]+new_v[i] for i in range(len(v))]
    for i in range(len(new_x)):
        if new_x[i] < -5:
            new_x[i] = -5
        if new_x[i] > 5:
            new_x[i] = 5
    new_p = [max(p[i],f(new_x[i])) for i in range(len(v))]
    new_g = max(g,max(new_p))
    return new_x,new_v,new_p,new_g

def pso(iterations,population,inertie,congnitive,sociale):
    x,v,p,g = generer_population_initiale(population)
    for i in range(iterations):
        x,v,p,g = calcul_a_t_plus_1(x,v,p,g,inertie,congnitive,sociale)
    return g


if __name__=="__main__":
    capacite_sac = 100
    poids = [8, 7, 10, 25, 30, 10, 8, 2, 7, 9]
    valeurs = [20, 24, 2, 70, 60, 20, 30, 15, 40, 25]
    inertie = random()
    congnitive = 2
    sociale = 2
    iterations = 20
    population = 20
    resultat = pso(iterations,population,inertie,congnitive,sociale,pods)
    print(resultat)