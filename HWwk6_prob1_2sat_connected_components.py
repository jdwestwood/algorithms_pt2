# Algorithms Pt2 HW 6 problem 1  10/11/2013  2SAT problems
#
# File format is:
# [n], the number of both variables and clauses, followed by the clauses, which are represented as
# [variable no][variable no], one clause per line.  A negative variable number corresponds to the
# negation of that clause.
#
# Use the connected components approach to solve these problems (see Vazirani pdf book, ch. 3.4 and problem 3.28),
# and aim for a linear-time algorithm.  The Papadimitriou algorithm from class runs in n**2 log(n) and will
# be too slow, by the time I get to the sixth file (1,000,000 variables and clauses).
#
# Basic algorithm is:
#   1. Construct a directed graph with 2*nvariables vertices and 2*nClauses edges that encodes the problem.
#   2. Calculate the connected components of the graph:
#       a. Do depth first search on the reverse of the graph and order the vertices by decreasing post-visit
#          ordering.
#       b. Do depth first search on the original graph, taking vertices in decreasing post-visit order.
#   3. Check each connected component to see if a variable and its inverse are found together.  If so,
#      there is no solution to the 2SAT problem.  If not, a solution can be constructed by assigning all
#      the vertices in a given connected component to TRUE and eliminating the corresponding negations
#      of those vertices in the other connected components. Repeat for the next connected component until
#      all vertices are TRUE.  Then translate the remaining graph back to assignments for the variables.
#
# 10/14/13: Implemented the algorithm here using recursion and deques to maintain queues of vertices.
#           Algorithm runs correctly but is extremely slow.  The 1st (smallest) data set is taking many
#           hours to run. Freeze this program as is and continue with ver. 2.  Will eliminate the deques
#           and use lists to try to speed up (??).

from sys import exit, maxint   # allows me to exit the program early using exit(0)
import time                    # allows me to time the execution of various parts of code
from collections import deque

class edge:
    def __init__(self, tail, head):
        self.tail = tail  # the tail vertex in V
        self.head = head  # the head vertex in V

class vertex:
    def __init__(self, index):    # index is the index of the vertex in the initial vertex list V
        self.index = index
        self.inEdges = []         # will be list of indices in the E list of edges that have the vertex as a head
        self.outEdges = []        # will be list of indices in the E list of edges that have the vertex as a tail
        self.pre = 0              # pre-visiting order in depth-first-search
        self.post = 0             # post-visiting order in depth-first-search
        self.cc = 0               # index of the connected component vertex is a member of
        self.negation = None      # the vertex representation of the negation of self

def depthFirst(deqV, deqDone):
#   do normal depth first search on the directed graph specified by vertices in deqV
#   return deqDone, a deque with vertices added in post-visit order (last one added has the
#   highest post-visit value of vOrder; vertices in deqDone have .cc = index of the connected
#   component to which they belong
    global vOrder
    curV = deqV.pop()
    explore(curV, deqV, deqDone)

def explore(curV, deqV, deqDone):
#   explore the graph in the normal direction starting at vertex curV; delete vertices from deqV as
#   they are explored; add vertices to deqDone in post-visit order
    global vOrder, ccIndex
    vOrder += 1
    curV.pre = vOrder
    for edge in curV.outEdges:     # exploring the graph as-specified!
        nextV = edge.head
        if nextV in deqV:
            deqV.remove(nextV)
            explore(nextV, deqV, deqDone)
    curV.post = vOrder
    curV.cc = ccIndex
    deqDone.append(curV)

def depthFirst_Rev(deqV, deqRev):
#   do depth first search on the reverse of the directed graph specified by vertices in deqV
#   return deqRev, a deque with vertices added in post-visiting order (last one added has the
#   highest post-visit value of vOrder
    global vOrder
    curV = deqV.pop()
    explore_Rev(curV, deqV, deqRev)

def explore_Rev(curV, deqV, deqRev):
#   explore the graph in the reverse direction starting at vertex curV; delete vertices from deqV as
#   they are explored; add vertices to reqRev in post-visit order
    global vOrder
    vOrder += 1
    curV.pre = vOrder
    for edge in curV.inEdges:      # exploring the reverse of the graph specified!
        nextV = edge.tail          # the reverse direction!
        if nextV in deqV:
            deqV.remove(nextV)
            explore_Rev(nextV, deqV, deqRev)
    curV.post = vOrder
    deqRev.append(curV)

dataFile = open('HWwk6_2sat_example.txt', 'r')
#dataFile = open('HWwk6_2sat1.txt', 'r')

header = dataFile.readline().split()
nV = int(header[0])                # number of variables
nC = int(header[1])                # number of clauses
print nV, nC

# initialize vertex and edge lists of the graph corresponding to the variables and clauses
V = [0] + [vertex(iV) for iV in xrange(1, 2*nV + 1)]  # dummy vertex at index 0
for iV in xrange(1, nV+1):
    V[iV].negation = V[-iV]
    V[-iV].negation = V[iV]

# read in clauses and create the graph (2nV vertices, 2nE edges)
E = [edge(0,0)]                          # list of edges with dummy edge at index 0
for line in dataFile:                      # read items into array of item objects
    edgeData = line.split()
    var1 = int(edgeData[0])                # will use both positive and negative variable indices
    var2 = int(edgeData[1])                # unchanged; negative index runs backwards from end of V
    firstEdge = edge(V[-var1], V[var2])
    E.append(firstEdge)
    V[-var1].outEdges.append(firstEdge)
    V[var2].inEdges.append(firstEdge)
    secondEdge = edge(V[-var2], V[var1])
    E.append(secondEdge)
    V[-var2].outEdges.append(secondEdge)
    V[var1].inEdges.append(secondEdge)

# no longer need V as a list; convert to a deque
deqV = deque(V[1:2*nV+1])
deqRev = deque([])                        # empty deque for the vertices in post-visit order

vOrder = 0                                # global variable to assign pre- and post-visit order for each vertex
while len(deqV) > 0:                      # visit all vertices in the reverse of the original graph
    depthFirst_Rev(deqV, deqRev)          # and return deqRev with vertices added in post-visit order

deqDone = deque([])                       # deqDone will contain the vertices from depRev that have been explored and had .cc value assigned
vOrder = 0
ccIndex = 0                               # just need indices of connected components, not lists of vertices in connected components
while len(deqRev) > 0:
    ccIndex += 1
    depthFirst(deqRev, deqDone)
print "Found", ccIndex, "connected components"

for v in deqDone:
    v_neg = v.negation
    if v.cc == v_neg.cc:
        print "Found variable:", v.index, "and", v_neg.index, "in connected component", v.cc
        print "2SAT clauses cannot be satisfied"
        exit()

print "2SAT clauses can all be satisfied"
