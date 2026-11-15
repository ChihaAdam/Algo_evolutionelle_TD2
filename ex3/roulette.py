from random import shuffle,randint,random

def f(s,villes):
    somme = 0
    for i in range(len(villes)):
        a = s[i] - 1
        b = s[(i+1)%len(villes)] -1 
        if villes[a][b]==-1 :
            return float("inf")
        curr = villes[a][b]
        somme += curr
    return somme
def calculFitness(generation,villes):
    somme = 0
    for individu in generation:
        somme += f(individu,villes)
    return somme
def generer_initial(nb,villes):
    liste = []
    initial = [i+1 for i in range(len(villes))]
    while len(liste)!=nb:
        shuffle(initial)
        if initial in liste:
            continue
        liste.append(initial[:])
    return liste
def crossover(pere1,pere2):
    fils1=[]
    fils2=[]
    pt = randint(0,len(pere1)-1)
    for i in range(pt+1):
        fils1.append(pere1[i])
        fils2.append(pere2[i])
    for i in range(pt+1,len(pere1)):
        fils1.append(pere2[i])
        fils2.append(pere1[i])
    return fils1,fils2
def mutate(trajet):
    #1er cas de mutation . chemin invalide
    vu = set()
    for i in range(len(trajet)):
        vu.add(trajet[i])
    if len(vu)<len(trajet):
        nonvu= set()
        for i in range(1,len(trajet)+1):
            if not i in vu:
                nonvu.add(i)
        vu = set()
        for i in range(len(trajet)):
            if trajet[i] in vu:
                trajet[i] = nonvu.pop()
            else:
                vu.add(trajet[i])
    #2eme cas . par probabilite
    q = 10**(-3)
    p = random()
    if (q<=p):
        x = randint(0,len(trajet)-1)
        y = randint(0,len(trajet)-1)
        trajet[x],trajet[y] = trajet[y],trajet[x]
    return trajet

def roulette(villes):
    generation_initial = generer_initial(25,villes)
    for _ in range(25):
        fitness = calculFitness(generation_initial,villes)
        probabilite_selection = [f(generation_initial[0],villes)/fitness]
        for i in range(1,len(generation_initial)):
            probabilite_selection.append(probabilite_selection[-1] + f(generation_initial[i],villes)/fitness)
        r1 = random()
        x=-1

        r2=random()
        y=-1
        for i in range(0,len(villes)):
            if r1<=probabilite_selection[i]:
                x=i
                break
        for j in range(0,len(villes)):
            if r2<=probabilite_selection[j]:
                y=j
                break
        fils1,fils2 = crossover(generation_initial[x],generation_initial[y])
        fils1 = mutate(fils1)
        fils2 = mutate(fils2)
        generation_initial[x],generation_initial[y]=fils1,fils2
    resultat = float("inf")
    for i in range(len(generation_initial)):
        resultat = min(resultat,f(generation_initial[i],villes))
    return resultat
def main():
    villes = [
        [-1, 14, 15, 22, 25, 20, 19, 17],
        [14, -1, 13, 14, 20, 16, 18, 21],
        [15, 13, -1, 11, 21, 17, 9, 9],
        [22, 14, 11, -1, 11, 10, 8, 20],
        [25, 20, 21, 11, -1, 15, 18, 19],
        [20, 16, 17, 10, 15, -1, 9, 22],
        [19, 18, 9, 8, 18, 9, -1, 13],
        [17, 21, 9, 20, 19, 22, 13, -1]
    ]
    resultat = roulette(villes)
    print(resultat)

if __name__ == "__main__":
    main()