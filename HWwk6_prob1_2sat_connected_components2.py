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
# 10/14/13: implemented lists instead of deques for tracking vertices, but still running too slowly!
#      To speed up, will try making vertex lists global instead of passing them as arguments. (Will probably
#      not help since Python objects are passed by reference, but I need to find a way to speed this up!)

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

def depthFirst(listV, listDone):
#   do normal depth first search on the directed graph specified by vertices in listV
#   return listDone, a list of vertices added in post-visit order (last one added has the
#   highest post-visit value of postOrder; vertices in listDone have .cc = index of the connected
#   component to which they belong
    startIndex = -1
    for iV in xrange(1, len(listV)):
        if listV[iV] != listV[0]:
            startIndex = iV
            break
    if startIndex > 0:
        curV = listV[startIndex]
        listV[curV.order] = listV[0]         # indicates that the vertex has been visited
        explore(curV, listV, listDone)

def explore(curV, listV, listDone):
#   explore the graph in the normal direction starting at vertex curV; delete vertices from listV as
#   they are explored; add vertices to listDone in post-visit order
    global vOrder, postOrder, ccIndex
    vOrder += 1
    curV.pre = vOrder
    for edge in curV.outEdges:       # exploring the graph as-specified!
        nextV = edge.head
        if listV[nextV.order] != listV[0]:   # nextV has not been visited yet
            listV[nextV.order] = listV[0]    # set list element to dummy vertex
            explore(nextV, listV, listDone)
    vOrder += 1
    curV.post = vOrder
    postOrder += 1
    curV.cc = ccIndex
    listDone[postOrder] = curV
#    print "explore: finish vertex", curV.index, "with postOrder", vOrder

def depthFirst_Rev(listV, listRev):
#   do depth first search on the reverse of the directed graph specified by vertices in listV
#   return listRev, a list with vertices added in post-visiting order (last one added has the
#   highest post-visit value of postOrder
    startIndex = -1
    for iV in xrange(1, len(listV)):
        if listV[iV] != listV[0]:
            startIndex = iV
            break
    if startIndex > 0:
        curV = listV[startIndex]
        listV[curV.order] = listV[0]         # indicates that the vertex has been visited
        explore_Rev(curV, listV, listRev)
    else:
        print "Unexpectedly found all zeroes in depthFirst_Rev"

def explore_Rev(curV, listV, listRev):
#   explore the graph in the reverse direction starting at vertex curV; delete vertices from listV as
#   they are explored; add vertices to listRev in post-visit order
    global vOrder, postOrder
    vOrder += 1
    curV.pre = vOrder
    for edge in curV.inEdges:        # exploring the reverse of the graph specified!
        nextV = edge.tail            # the reverse direction!
        if listV[nextV.order] != listV[0]:   # nextV has not been visited yet
            listV[nextV.order] = listV[0]    # now it has
            explore_Rev(nextV, listV, listRev)
    vOrder += 1
    curV.post = vOrder
    postOrder += 1
    listRev[postOrder] = curV
#    print "explore_Rev: finish vertex", curV.index, "with postOrder", vOrder

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

# read in clauses and create the graph (2nV vertices, 2nC edges)
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

vOrder = 0                                # global variable to assign pre- and post-visit order for each vertex
postOrder = 0
while postOrder < 2*nV:                      # visit all vertices in the reverse of the original graph
    depthFirst_Rev(V, V_Rev)              # and return listRev with vertices added in post-visit order
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
    depthFirst(V_Rev, V_Done)
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
