# Algorithms Pt2 HW 1 problem 3  9/12/2013 
#
# Implement Prim's minimum spanning tree algorithm without heap optimization
#
# first line of input file is number vertices and edges.
# subsequent lines are vertex1, vertex2, and cost for each edge.
#
# objective is tree T with minimum total cost of edges.
# 
# see slides-greedy-algo2-greedy--minimum-spanning-tree-6.pdf from lecture notes.

import copy

class edge:
    v1 = 0
    v2 = 0
    cost = float("inf")

dataFile = open('HWwk1_problem_3_edges.txt', 'r')
#dataFile = open('HWwk1_short.txt', 'r')

header = dataFile.readline().split()
nV = int(header[0])
nE = int(header[1])

edgeList = []
for line in dataFile:     # read edge data into edge object and add to edge list
    edgeDesc = line.split()
    edgeObj = edge()
    edgeObj.v1 = int(edgeDesc[0])
    edgeObj.v2 = int(edgeDesc[1])
    edgeObj.cost = int(edgeDesc[2])
#    print line, edgeObj.v1, edgeObj.v2, edgeObj.cost
    edgeList.append(edgeObj)

X = [1]
V = range(2, nV+1)        # integers from 2 to nV
T = []

# Prim's algorithm
for v in range(1, nV):     # for the nV-1 vertices in V
    minCost = float("inf")
    minVert = 0
    minEdge = ''
    for iEdge in range(len(edgeList)-1, -1, -1):  # search through the edges
        e = edgeList[iEdge]
        v1_in_X = e.v1 in X
        v2_in_X = e.v2 in X
        v1_in_V = e.v1 in V
        v2_in_V = e.v2 in V
        if (v1_in_X and v2_in_V) or (v1_in_V and v2_in_X):   # found edge to check
            if e.cost < minCost:       # found new mininum edge cost
                minEdge = e
                if v1_in_V:
                    minVert = e.v1
                else:
                    minVert = e.v2
                minCost = e.cost
        if v1_in_X and v2_in_X:                   # no longer need to check this edge
            edgeList.remove(e)
    X.append(minVert)
    T.append(copy.deepcopy(minEdge))  # next pass will delete minEdge from edgeList
    V.remove(minVert)

# calculate the cost of the minimum spanning tree
treeCost = 0
for e in T:
    treeCost += e.cost

print 'Cost of MST:', treeCost





