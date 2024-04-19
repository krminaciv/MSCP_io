from create_graph import *
import random
import time


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


def correction(g, child):
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


def mutation(child, g):
     oldchild = child.copy()
     v = str(random.randint(1, len(g)))
     # print("random cvor: ", v)
     child[v] += 1
     for node in g[v]:
          #stavi mu manju boju ako moze
          neighbor_colors = {child[neighbor] for neighbor in g[node]}
          available_colors = set(range(1, len(g))) - neighbor_colors
          child[node] = min(available_colors)
     if(sum(child.values()) < sum(oldchild.values())): 
          return child
     return oldchild
     



def genetic_algorithm(g, size, stop):

     population = inicialPopulation(g, size)
     t = time.time()
     counter = 0
     while True:

          counter += 1
          population.sort(key=lambda child: fitness(child))

          elite = population[:2]
          newGen = []
          newGen.append(elite[0])
          newGen.append(elite[1])
          # print(newGen)

          fitnessRate = [1/fitness(child) for child in population]

          for i in range(size//2):
               parent1, parent2 = random.choices(population, fitnessRate, k=2)    
               child = crossover(parent1, parent2)
               child = correction(g,child)
               for _ in range(10):
                    child = mutation(child, g)
               newGen.append(child)
          
          population = newGen

          if((time.time() - t) > 100 or counter > stop): break

     print("Populacija - krajnji rezultat: ")
     # for p in population: print(p, "mscp: ", sum(p.values()))
     minChild = min(population, key=lambda p: sum(p.values()))
     print("minimalna jedinka: ", minChild, "mscp: ", sum(minChild.values()))



startTime = time.time()
graph = create_graph("instances/srednje -130/huck_74.txt")

populationSize = 50
genetic_algorithm(graph, populationSize,100)
print("vrijeme: ", time.time() - startTime)