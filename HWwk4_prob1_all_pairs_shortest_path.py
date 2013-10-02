# Algorithms Pt2 HW 4 problem 1  10/1/2013
#
# File format is:
# [n vertices][m edges], followed by [tail vertex][head vertex][cost] ... , one edge per line
# Find minimum shortest path over all pairs using Johnson's algorithm; appropriate in this case
# because the graphs are relatively sparse (1000 vertices, ~47000 edges).
#
# See slides-dp-algo2-dp-apsp.pdf's, slides-dp-algo2-dp, and slides-intro-algo1-dijkstra-basics from lecture notes
#
# Basic algorithm is:
#   1. Add a vertex with edges of zero cost directed from the added vertex to all vertices in the graph.
#   2. Run the Bellman-Ford algorithm once to get the shortest paths from the added vertex to all other
#      vertices.
#   3. Check for negative cost cycles in the graph, and stop if any are found.
#   4. Use the shortest path distances to each vertex to reweight the edges so all have positive costs.
#   5. Run Dijkstra's algorithm to get the shortest paths between all combinations of vertices.
#   6. Recalculate the shortest path distances for the original edge costs.
#
# 10/2/13: ran program on the problem datasets:
#    Graph 1: BF found negative cost cycle.
#    Graph 2: BF found negative cost cycle.
#    Graph 3: min path cost for all pairs of vertices is -19.

from sys import exit, maxint   # allows me to exit the program early using exit(0)
import time                    # allows me to time the execution of various parts of code
import heapq

class edge:
    def __init__(self, tail, head, cost):
        self.tail = tail  # index of the tail vertex in V
        self.head = head  # index of the head vertex in V
        self.cost = cost
        self.total = maxint
    def __cmp__(self, other):
        return cmp(self.total, other.total)

class vertex:
    def __init__(self, dummy):
        self.inEdges = []         # will be list of indices in the E list of edges that have the vertex as a head
        self.outEdges = []        # will be list of indices in the E list of edges that have the vertex as a tail

# Bellman-Ford algorithm:

def Bellman_Ford(V, n, s, E):
    # compute the all pairs minimum cost from the source vertex indexed by s in V to all vertices,
    # where n is the number of vertices in the graph.  E is the list of edges.
    # if there are any negative cycles, return -1; otherwise, return the list Ai of shortest path distances
    # from s to all vertices.
    Ai = [maxint for v in range(0, n+1)]  # initialize: all distances are infinite
    Ai[s] = 0                             # except for distance from the source vertex to itself
    for i in xrange(1, n+1):
        Ai_1 = Ai
        Ai = [maxint for v in range(0, n+1)]  # initialize: all distances are infinite
        for v in xrange(1, n+1):
            minCost = Ai_1[v]
            for iEdge in V[v].inEdges:
                minCost = min(minCost, Ai_1[E[iEdge].tail] + E[iEdge].cost)
            Ai[v] = minCost
    for v in xrange(1, n+1):    # now check for negative distance cycles
        if Ai_1[v] != Ai[v]:
            return -1
    return Ai

# Dijkstra algorithm:
def Dijkstra(V, n, s, E, checkNegative):
    # compute the minimum cost from the source vertex indexed by s in V to all vertices,
    # where n is the number of vertices in the graph.  E is the list of edges.
    # if there are any negative edge lengths, return -1; otherwise, return the list A of shortest path distances
    # from s to all vertices.
    # if checkNegative is True, loop through the edges to see if any have negative cost; return -1 if so
    if checkNegative:
        for curEdge in E:
            if curEdge.cost < 0:
                print "Found negative edge length.  Cannot use Dijkstra.  Exiting..."
                return -1
    A = [0 for v in xrange(0, n+1)]   # initialize A, the list of minimum distances to each vertex, with dummy vertex at index 0
    V_X = [v for v in xrange(1, n+1)] # V-X
    curVIndex = s
    X = [curVIndex]                  # add index of source vertex to X
    V_X.remove(curVIndex)            # delete index of source vertex from V_X
    crossingEdges = []
    while len(V_X) > 0:
        for outEdgeIndex in V[curVIndex].outEdges:           # for all outgoing edges from the most recently added vertex to X
            curEdge = E[outEdgeIndex]
            if curEdge.head not in X:                        # tail in X, head in V_X: add to heap
                curEdge.total = A[curEdge.tail] + curEdge.cost
                heapq.heappush(crossingEdges, curEdge)
        minCostEdge = heapq.heappop(crossingEdges)
        while not (minCostEdge.tail in X and minCostEdge.head in V_X):  # pop the lowest cost edge until we get one that crosses
            minCostEdge = heapq.heappop(crossingEdges)                # between X and V_X
        nextVIndex = minCostEdge.head                        # index of next vertex to be added to X and deleted from X_W
        X.append(nextVIndex)
        V_X.remove(nextVIndex)
        A[nextVIndex] = minCostEdge.total                    # the cost of the shortest path from vertex indexed by V[s] to V[nextVIndex]
        curVIndex = nextVIndex
    return A
    
#dataFile = open('HWwk4_example.txt', 'r')
dataFile = open('HWwk4_prob1_g3.txt', 'r')

header = dataFile.readline().split()
n = int(header[0])
m = int(header[1])
print n, m

# initialize vertex list
V = [vertex(v) for v in xrange(0, n+1)]

# read in edges and add edges to vertices
edgeIndex = 0
E = [edge(0,0,0)]                          # list of edges with dummy edge at index 0
for line in dataFile:                      # read items into array of item objects
    edgeIndex += 1
    edgeData = line.split()
    tailVertex = int(edgeData[0])
    headVertex = int(edgeData[1])
    edgeCost = int(edgeData[2])
    E.append(edge(tailVertex, headVertex, edgeCost))
    V[tailVertex].outEdges.append(edgeIndex)
    V[headVertex].inEdges.append(edgeIndex)

#s = 6
#bf = Bellman_Ford(V, n, s, E)
#dij = Dijkstra(V, n, s, E, True)
#print "BF:", bf
#print "Dij:", dij
#exit(0)

# add vertex with outgoing edges of zero cost to all other vertices in preparation for
# running Bellman-Ford algorithm 1x
V.append(vertex(n+1))
for v in xrange(1,n+1):
    E.append(edge(n+1, v, 0))
    lastEdgeIndex = len(E) - 1
    V[v].inEdges.append(lastEdgeIndex)
    V[n+1].outEdges.append(lastEdgeIndex)

print "Calculating reweighting list using Bellman-Ford"
s = n+1
p = Bellman_Ford(V, n+1, s, E)             # calculate the reweighting contribution associated with each vertex
if p == -1:
    print "BF found a negative cost cycle. Exiting..."
    exit(0)

# delete the added vertex and associated edges
del V[n+1]
del E[m+1:len(E)]
for vert in V[1:n+1]:
    del vert.inEdges[-1]

# reweight the edges according to the bf_costs results
for curEdge in E:
    curEdge.cost += p[curEdge.tail] - p[curEdge.head]

# run Dijkstra for all vertices as the source and correct back to the original edge weights
# first run Dijkstra 1x checking for negative edges
s = 1
print "Calculating Dijkstra shortest distances for vertex", s
dij_shortest_paths = Dijkstra(V, n, s, E, True)
if dij_shortest_paths == -1:
    exit(0)
minPathCost = maxint
for v in xrange(1, n+1):
    dij_shortest_paths[v] += -p[s] + p[v]
dij_shortest_paths[1] = maxint                                   # effectively exclude the path from the source to itself from
minPathCost = min(minPathCost, min(dij_shortest_paths[1:n+1]))   # consideration as the minimum length path
# run Dijkstra on all the remaining vertices as the source
for s in xrange(2, n+1):
    print "Calculating Dijkstra shortest distances for vertex", s
    print "Current minPathCost is", minPathCost
    print ""
    dij_shortest_paths = Dijkstra(V, n, s, E, False)
    for v in xrange(1, n+1):                                      # correct the path lengths to correspond with the original edge weightings
        dij_shortest_paths[v] += -p[s] + p[v]
    dij_shortest_paths[s] = maxint                                  # effectively exclude the path from the source to itself from
    minPathCost = min(minPathCost, min(dij_shortest_paths[1:n+1]))  # consideration as the minimum length path

print "The minimum path length between all pair of vertices is:", minPathCost
