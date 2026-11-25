from random import randint, random

def encode(cand):
    s=""
    while cand>0:
        s+=str(cand%2)
        cand//=2
    return s
def f(cand,poids,valeur,capacite_sac):
    individu = encode(cand)
    somme = 0
    poids_total = 0
    for i in range(len(individu)):
        poids_total += int(individu[i])*poids[i]
        somme += int(individu[i])*valeur[i]
    if poids_total > capacite_sac:
        return 0
    return somme

def generer_population_initiale(nb_packs,poids,valeurs,capacite_sac,n=8):
    x = []
    for i in range(n):
        x.append(randint(0,2**nb_packs - 1))
    v = [randint(1, 10) for _ in range(n)]
    p = [xi for xi in x]
    g = max(p, key=lambda xi: f(xi,poids,valeurs,capacite_sac))
    return x, v, p, g

def calcul_vitesse_a_t_plus_1(x,v,p,g,inertie,congnitive,sociale):
    new_v = []
    for i in range(len(v)):
        r1 = random()
        r2 = random()
        b1 = r1*congnitive
        b2 = r2*sociale
        new_v.append(inertie*v[i] + b1*(p[i]-x[i]) + b2*(g-x[i]))
    return new_v

def calcul_a_t_plus_1(x,v,p,g,inertie,congnitive,sociale,poids,valeurs,capacite_sac):
    new_v = calcul_vitesse_a_t_plus_1(x,v,p,g,inertie,congnitive,sociale)
    new_x = [x[i]+new_v[i] for i in range(len(v))]
    for i in range(len(new_x)):
        if new_x[i] < -5:
            new_x[i] = -5
        if new_x[i] > 5:
            new_x[i] = 5
    new_p = [max(p[i],new_x[i],key=lambda k:f(k,poids,valeurs,capacite_sac)) for i in range(len(v))]
    new_cand_g = max(new_p,key=lambda k:f(k,poids,valeurs,capacite_sac))
    new_g = max(g,new_cand_g,key=lambda k:f(k,poids,valeurs,capacite_sac))
    return new_x,new_v,new_p,new_g

def pso(iterations,population,inertie,congnitive,sociale,poids,valeurs,capacite_sac):
    x,v,p,g = generer_population_initiale(len(poids),poids,valeurs,capacite_sac)
    for i in range(iterations):
        x,v,p,g = calcul_a_t_plus_1(x,v,p,g,inertie,congnitive,sociale,poids,valeurs,capacite_sac)
    return g


if __name__=="__main__":
    capacite_sac = 100
    poids = [8, 7, 10, 25, 30, 10, 8, 2, 7, 9,10]
    valeurs = [20, 24, 2, 70, 60, 20, 30, 15, 40, 25,4]
    inertie = random()
    congnitive = 2
    sociale = 2
    iterations = 20
    population = 20
    resultat = pso(iterations,population,inertie,congnitive,sociale,poids,valeurs,capacite_sac)
    print(encode(resultat))
    print(f(resultat,poids,valeurs,capacite_sac))