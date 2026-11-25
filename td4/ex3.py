from random import randint, random


def f(x):
    return -(x**2)+ 4*x

def generer_population_initiale(n):
    x = [randint(-5,5) for _ in range(n)]
    v = [randint(1,10) for _ in range(n)]
    p = [f(xi) for xi in x]
    g = max(p)
    return x,v,p,g

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
def pso_test(iterations,x,v,inertie,congnitive,sociale):
    p = [f(xi) for xi in x]
    g = max(p)
    for i in range(iterations):
        x,v,p,g = calcul_a_t_plus_1(x,v,p,g,inertie,congnitive,sociale)
    return g

def tester():
    x=[2,4,-1]
    v=[0,0,0]
    c1=0.8
    c2=2
    c3=2
    print("exercice 1: ")
    print("i=1")
    print(pso_test(1,x,v,c1,c2,c3))
    print("i=3")
    print(pso_test(3, x, v, c1, c2, c3))
    print("\n===============================\n")

if __name__=="__main__":
    tester()
    inertie = random()
    congnitive = 2
    sociale = 2
    iterations = 20
    population = 20
    resultat = pso(iterations,population,inertie,congnitive,sociale)
    print(resultat)