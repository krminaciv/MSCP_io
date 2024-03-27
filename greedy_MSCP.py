from create_graph import *

def greedy_mscp(g):
     colors = {}   #mapiranje cvorova na boje = 'cvor': boja
     used_colors = set()

     sorted_nodes = sorted(g.keys(), key=lambda x: len(g[x]))    #sortiramo cvorove po njihovom stepenu
     #print(sorted_nodes)                                        #od najmanjeg ka najvecem

     for node in sorted_nodes:
          neighbor_colors = {colors[neighbor] for neighbor in graph[node] if neighbor in colors}
          available_colors = set(range(1, len(used_colors) + 3)) - neighbor_colors
          color = min(available_colors)
          colors[node] = color
          used_colors.add(color)
     
     return colors

graph = create_graph("instances/male -50/queen5_5.txt")
print("graf: ", graph)

coloring = greedy_mscp(graph)
print("bojenje: ", coloring)

min_sum = sum(coloring.values())   #tražena suma MSCP-a
print("min suma: ", min_sum)