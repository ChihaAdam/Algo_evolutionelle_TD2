from collections import deque
def evaluer(individu,poids,valeur,capacite_sac):
    somme = 0
    poids_total = 0
    for i in range(len(individu)):
        poids_total += int(individu[i])*poids[i]
        somme += int(individu[i])*valeur[i]
    if poids_total > capacite_sac:
        return 0
    return somme
def calcul_voisins(individu):
    v = []
    voisin = [*individu]
    for i in range(len(individu)-1):
        voisin[i] = "1" if voisin[i]=="0" else "0"
        v.append("".join(voisin))
        voisin[i] = "1" if voisin[i] == "0" else "0"
    return v
def tabou(initial,poids,valeur,capacite_sac,iters,taille_tabou):
    s = initial
    d = evaluer(initial,poids,valeur,capacite_sac)
    tab = deque(maxlen=taille_tabou)
    for i in range(iters):
        voisins = calcul_voisins(s)
        voisins = [voisin for voisin in voisins if voisin not in tab]
        if (len(voisins)==0):
            break
        s_prime = max(voisins,key=lambda x:evaluer(x,poids,valeur,capacite_sac))
        d_prime = evaluer(s_prime,poids,valeur,capacite_sac)
        tab.append(s_prime)
        if d_prime>d:
            s = s_prime
            d = d_prime
    return d,s
if __name__=="__main__":
    capacite_sac = 100
    poids = [8,7,10,25,30,10,8,2,7,9]
    valeurs = [20,24,2,70,60,20,30,15,40,25]
    meilleur_score, meilleur = tabou("1001011010",poids, valeurs, capacite_sac,100,5)
    print(meilleur_score)
    print(meilleur)