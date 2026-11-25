
def est_schema(h,individu):
    if (len(h)!=len(individu)):
        return False
    for i in range(len(h)):
        if (h[i]=="*"):
            continue
        if (h[i]!=individu[i]):
            return False
    return True

def nb_attendu_schema(h, population,fitness):
    s = 0
    fit = 0
    for i in range(len(population)):
        if est_schema(h, population[i]):
            s += 1
            fit += fitness[i]
    if (s!=0):
        return s,fit/s
    return s,1
def longueur_utile_shema(h):
    a=0
    b=len(h)-1
    while (a<len(h) and h[a]=="*"):
        a+=1
    while (b>=0 and h[b]=="*"):
        b-=1
    return b-a
def nb_attendu_generation_1(h):
    population_initiale = ["10001","11100","00011","01110"]
    fitness_initiale = [20,10,5,15]
    F = sum(fitness_initiale)
    nb_attendu_gen_0 ,fit_gen_0= nb_attendu_schema(h,population_initiale,fitness_initiale)
    l_schema_utile = longueur_utile_shema(h)
    l = len(h)
    nb_etoiles = h.count("x")
    pm=0.01
    pc=0.1
    return nb_attendu_gen_0*(fit_gen_0/F)*(1-pc*l_schema_utile/(l-1)- nb_etoiles*pm)

def main():
    h1="1*****"
    h2="0**10"
    print(" le nombre attendu de schèmes de la forme H 1 dans génération 1 est supérieur ou égale à: " + str(nb_attendu_generation_1(h1)))
    print(" le nombre attendu de schèmes de la forme H 2 dans génération 1 est supérieur ou égale à: " + str(nb_attendu_generation_1(h2)))

if __name__ == "__main__":
    main()