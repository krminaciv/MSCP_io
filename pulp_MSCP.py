from pulp import *
from create_graph import *
import time

startTime = time.time()
graph = create_graph("instances/velike -200/queen13_13.txt")
vertices = set(graph.keys())
k = len(vertices) + 1

#problem
problem = pulp.LpProblem('MinimumSumColoringProblem', LpMinimize)

#varijable
x = pulp.LpVariable.dicts('x', [(v, c) for v in vertices for c in range(1,k)], cat='Binary')

#funkcija cilja
problem += lpSum(c * x[v, c] for v in vertices for c in range(1, k))

#uslov 1
for v in vertices:
    for neighbor in graph[v]:
        for c in range(1,k):
            problem += x[v, c] + x[neighbor, c] <= 1

#uslov 2
for v in vertices:
    problem += lpSum(x[v, c] for c in range(1,k)) == 1


problem.solve(PULP_CBC_CMD(maxSeconds=600))


mscp = 0
print("Optimal Solution:")
for v in vertices:
    for c in range(1,k):
        if x[v, c].varValue == 1:
            print(f"Vertex {v} is colored with color {c}")
            mscp += c
print("MSCP =", mscp)
print("vrijeme: ", time.time() - startTime)

