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
# 10/14/13: vertex lists are now global, but the program is running overnight on the first (smallest) dataset
#      and still not done.... Next will try writing the depth-first search non-recursively, which will be
#      a challenge, since the algorithm is so naturally recursive.

from sys import exit, maxint   # allows me to exit the program early using exit(0)
import time                    # allows me to time the execution of various parts of code

class edge:
    def __init__(self, tail, head):
        self.tail = tail  # the tail vertex in V
        self.head = head  # the head vertex in V

class vertex:
    def __init__(self, index): # index is the index of the vertex in the initial vertex list V
        self.index = index
        self.order = index
        self.inEdges = []           # will be list of indices in the E list of edges that have the vertex as a head
        self.outEdges = []          # will be list of indices in the E list of edges that have the vertex as a tail
        self.pre = 0                # pre-visiting order in depth-first-search
        self.post = 0               # post-visiting order in depth-first-search
        self.cc = 0                 # index of the connected component vertex is a member of
        self.negation = None        # the vertex representation of the negation of self

def depthFirst():
#   do normal depth first search on the directed graph specified by vertices in listV
#   return listDone, a list of vertices added in post-visit order (last one added has the
#   highest post-visit value of postOrder; vertices in listDone have .cc = index of the connected
#   component to which they belong
    global V_Rev, V_Done
    startIndex = -1
    for iV in xrange(1, len(V_Rev)):
        if V_Rev[iV] != V_Rev[0]:
            startIndex = iV
            break
    if startIndex > 0:
        curV = V_Rev[startIndex]
        V_Rev[curV.order] = V_Rev[0]         # indicates that the vertex has been visited
        explore(curV)

def explore(curV):
#   explore the graph in the normal direction starting at vertex curV; delete vertices from listV as
#   they are explored; add vertices to listDone in post-visit order
    global V_Rev, V_Done
    global vOrder, postOrder, ccIndex
    vOrder += 1
    curV.pre = vOrder
    for iEdge in xrange(0, len(curV.outEdges)):
        nextV = curV.outEdges[iEdge].head
        if V_Rev[nextV.order] != V_Rev[0]:   # nextV has not been visited yet
            V_Rev[nextV.order] = V_Rev[0]    # set list element to dummy vertex
            explore(nextV)
    vOrder += 1
    curV.post = vOrder
    postOrder += 1
    curV.cc = ccIndex
    V_Done[postOrder] = curV
#    print "explore: finish vertex", curV.index, "with postOrder", vOrder

def depthFirst_Rev():
#   do depth first search on the reverse of the directed graph specified by vertices in listV
#   return listRev, a list with vertices added in post-visiting order (last one added has the
#   highest post-visit value of postOrder
    global V, V_Rev
    startIndex = -1
    for iV in xrange(1, len(V)):
        if V[iV] != V[0]:
            startIndex = iV
            break
    if startIndex > 0:
        curV = V[startIndex]
        V[curV.order] = V[0]         # indicates that the vertex has been visited
        explore_Rev(curV)
    else:
        print "Unexpectedly found all zeroes in depthFirst_Rev"

def explore_Rev(curV):
#   explore the graph in the reverse direction starting at vertex curV; delete vertices from V as
#   they are explored; add vertices to V_Rev in post-visit order
    global V, V_Rev, start_time
    global vOrder, postOrder, rDepth
    rDepth += 1
    if rDepth%100 == 0:
        print "rDepth:", rDepth
    vOrder += 1
    if vOrder%10000 == 0:
        print "vOrder:", vOrder, time.time() - start_time
    curV.pre = vOrder
    for iEdge in xrange(0, len(curV.inEdges)):
        nextV = curV.inEdges[iEdge].tail
        if V[nextV.order] != V[0]:   # nextV has not been visited yet
            V[nextV.order] = V[0]    # now it has
            explore_Rev(nextV)
    vOrder += 1
    rDepth -= 1
    curV.post = vOrder
    postOrder += 1
    V_Rev[postOrder] = curV
    if postOrder%10000 == 0:
        print "postOrder", postOrder, time.time() - start_time

start_time = time.time()
#dataFile = open('HWwk6_2sat_example.txt', 'r')
dataFile = open('HWwk6_2sat1.txt', 'r')

header = dataFile.readline().split()
nV = int(header[0])                # number of variables
nC = int(header[1])                # number of clauses
print nV, nC

# initialize vertex and edge lists of the graph corresponding to the variables and clauses
V = [vertex(iV) for iV in xrange(0, 2*nV + 1)]  # dummy vertex at index 0
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
print "Read file: ", time.time() - start_time

V_Rev = [V[0] for iV in xrange(0, 2*nV + 1)] # initialize with dummy vertex for all list positions
print "Initialize V_Rev:", time.time() - start_time

rDepth = 0                                # recursion depth
vOrder = 0                                # global variable to assign pre- and post-visit order for each vertex
postOrder = 0
while postOrder < 2*nV:                   # visit all vertices in the reverse of the original graph
    depthFirst_Rev()                      # and return V_Rev with vertices added in post-visit order
print "Calculate V_Rev:", time.time() - start_time

dumV = V[0]                               # put vertices in post order high to low
for iV in xrange(1, nV + 1):
    dumV = V_Rev[iV]
    V_Rev[iV] = V_Rev[-iV]
    V_Rev[-iV] = dumV
    V_Rev[iV].order = iV                  # update .order to reflect the vertex position in V_Rev
    V_Rev[-iV].order = 2*nV + 1 - iV
print "Reverse V_Rev:", time.time() - start_time

V_Done = [V[0] for iV in xrange(0, 2*nV + 1)]  # V_Done will contain the vertices from V_Rev that have been explored and had .cc value assigned
print "Initialize V_Dome:", time.time() - start_time

vOrder = 0
postOrder = 0
ccIndex = 0                               # just need indices of connected components, not lists of vertices in connected components
while postOrder < 2*nV:
    ccIndex += 1
    depthFirst()
print "Calculate V_Done:", time.time() - start_time
print "Found", ccIndex, "connected components"

for iV in xrange(1, 2*nV + 1):
    v = V_Done[iV]
    v_neg = v.negation
    if v.cc == v_neg.cc:
        print "Found variable:", v.index, "and", v_neg.index, "in connected component", v.cc
        print "2SAT clauses cannot be satisfied"
        print "Completed:", time.time() - start_time
        exit()

print "2SAT clauses can all be satisfied"
print "Completed:", time.time() - start_time
