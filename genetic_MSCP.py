from create_graph import *
import random


def color_graph(g):
     colors = {}   #mapiranje cvorova na boje = 'cvor': boja
     used_colors = set()

     random_nodes = sorted(g.keys(), key=lambda x: random.randrange(0,len(g)))
     # print(random_nodes)

     for node in random_nodes:
          neighbor_colors = {colors[neighbor] for neighbor in g[node] if neighbor in colors}
          available_colors = set(range(1, len(used_colors) + 3)) - neighbor_colors
          color = min(available_colors)
          colors[node] = color
          used_colors.add(color)
     
     colors = dict(sorted(colors.items()))
     return colors


#pravi pocetnu populaciju
def inicialPopulation(g, size):
     p = []
     for _ in range(0, size):
          child  = color_graph(g)
          p.append(child)
     return p


def fitness(child):
     mscp = sum(child.values())    #mjera prilagodjenosti ce da bude nasa trazena suma
     return 1/mscp


def crossover(parent1, parent2):
     l = len(parent1)
     crosspoint = random.randint(1, l)
     # print("crosspt: ", crosspoint)

     child = {}
     for i in range(1,l+1):
          if(i <= crosspoint): 
               child[str(i)] = parent1[str(i)]
          else:
               child[str(i)] = parent2[str(i)]
     return child


def mutation(g, child):
    for v1 in g:
        for v2 in g[v1]:
            if(child[v1] == child[v2]): #oboji cvor nekom dostupnom bojom
                chr = child[max(child, key= child.get)]
                changed = False
                for color in range(1, chr+1):
                    available = True
                    for neighbor in g[v1]:
                        if child[neighbor] == color: 
                            available = False
                            break
                    if available:
                        child[v1] = color
                        changed = True
                if not changed:
                    child[v1] = chr+1

    return child



def genetic_algorithm(g, size):

     population = inicialPopulation(g, size)

     #while petlja

     population.sort(key=lambda child: fitness(child))

     elite = population[:2]
     newGen = []
     newGen.append(elite[0])
     newGen.append(elite[1])
     # print(newGen)

     fitnessRate = [1/fitness(child) for child in population]

     for _ in range(populationSize//2):
          parent1, parent2 = random.choices(population, fitnessRate, k=2)    
          child = crossover(parent1, parent2)
          child = mutation(g,child)
          newGen.append(child)
     
     population = newGen

     print("Populacija - krajnji rezultat: ")
     for p in population: print(p, "mscp: ", sum(p.values()))
     minChild = min(population, key=lambda p: sum(p.values()))
     print("minimalna jedinka: ", minChild, "mscp: ", sum(minChild.values()))




graph = create_graph("instances/male -50/queen5_5.txt")
populationSize = 10
genetic_algorithm(graph, populationSize)