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
# 10/14/13: depth-first search using recursion is extremely slow (1st dataset takes > overnight); rewrite the
#           depth-first search non-recursively here using a list as a stack. Now the problems run in 30 sec - 2 min!
#
# 10/15/13: ran program on the problem datasets:
#    1: can be satisfied: 199988 connected components
#    2: cannot be satisfied: 399893 connected components
#    3: can be satisfied: 799653 connected components
#    4: can be Satisfied: 1199922 connected components
#    5: cannot be satisfied: 1599683 connected components
#    6: cannot be satisfied: 1999912 connected components

from sys import exit, maxint   # allows me to exit the program early using exit(0)
import time                    # allows me to time the execution of various parts of code

class edge:
    def __init__(self, tail, head):
        self.tail = tail  # the tail vertex in V
        self.head = head  # the head vertex in V
#    def __cmp__(self, other):
#        return cmp(self.cost, other.cost)

class vertex:
    def __init__(self, index): # index is the index of the vertex in the initial vertex list V
        self.index = index
        self.inEdges = []           # will be list of indices in the E list of edges that have the vertex as a head
        self.outEdges = []          # will be list of indices in the E list of edges that have the vertex as a tail
        self.pre = 0                # pre-visiting order in depth-first-search
        self.post = 0               # post-visiting order in depth-first-search
        self.cc = 0                 # index of the connected component vertex is a member of
        self.negation = None        # the vertex representation of the negation of self
        self.visited = False

#    Would need the logic in the following code to reconstruct clauses from graph edges
#    if curV.index <= nV:
#        impliedIndex = -curV.index
#    else:
#        impliedIndex = 2*nV+1 - curV.index
#            if nextV.index <= nV:
#                impliedCurIndex = nextV.index
#            else:
#                impliedCurIndex = -(2*nV+1 - nextV.index)
#            print "explore: following edge from", curV.index, "to vertex:", nextV.index
#            print "      implies clause:", impliedIndex, "or", impliedCurIndex

def depthFirst_Rev():
#   do depth first search in the reverse direction on the directed graph specified by vertices in V
#   return V_rev, a list of vertices added in post-visit order (last one added has the
#   highest post-visit value of postOrder.
    global V, V_rev, vOrder
    V_stack = []
    if len(V) > 0:
        nextV = V[-1]                      # must be an unvisited vertex
        curV = nextV
        vOrder +=1
        curV.pre = vOrder
        V_stack.append(curV)
        while len(V_stack) > 0:
            curV = V_stack[-1]
            stackBefore = len(V_stack)
            if not curV.visited:
                for iEdge in xrange(0, len(curV.inEdges)):
                    if curV.inEdges[iEdge].tail.pre == 0:  # has not been pre-visited
                        foundV = curV.inEdges[iEdge].tail
                        vOrder += 1        # pre-visit
                        foundV.pre = vOrder
                        V_stack.append(foundV)
                curV.visited = True        # consider vertex visited if its unexplored children are on the stack
            stackAfter = len(V_stack)
            if stackAfter == stackBefore:  # no vertices left to explore from curV
                vOrder += 1                # post-visit
                curV.post = vOrder
                V_rev.append(curV)
                V_stack.pop()              # finished with current curV
                if vOrder%10000 == 0:
                    print "vOrder:", vOrder, time.time() - start_time
        while len(V) > 0 and V[-1].visited:  # so calling function can decide
            V.pop()                        # whether the search is done

def depthFirst():
#   do normal depth first search on the directed graph specified by vertices in V_rev
#   return V_done, a list of vertices added in post-visit order (last one added has the
#   highest post-visit value of postOrder; vertices in V_done have .cc = index of the connected
#   component to which they belong
    global V_rev, V_done, vOrder
    V_stack = []
    if len(V_rev) > 0:
        nextV = V_rev[-1]                  # must be an unvisited vertex
        curV = nextV
        vOrder +=1
        curV.pre = vOrder
        V_stack.append(curV)
        while len(V_stack) > 0:
            curV = V_stack[-1]
            stackBefore = len(V_stack)
            if not curV.visited:
                for iEdge in xrange(0, len(curV.outEdges)):
                    if curV.outEdges[iEdge].head.pre == 0:  # has not been pre-visited
                        foundV = curV.outEdges[iEdge].head
                        vOrder += 1        # pre-visit
                        foundV.pre = vOrder
                        V_stack.append(foundV)
                curV.visited = True        # consider vertex visited if its unexplored children are on the stack
            stackAfter = len(V_stack)
            if stackAfter == stackBefore:  # no vertices left to explore from curV
                vOrder += 1                # post-visit
                curV.post = vOrder
                curV.cc = ccIndex
                V_done.append(curV)
                V_stack.pop()              # finished with current curV
                if vOrder%10000 == 0:
                    print "vOrder:", vOrder, time.time() - start_time
        while len(V_rev) > 0 and V_rev[-1].visited:  # so calling function can decide
            V_rev.pop()                    # whether the search is done

start_time = time.time()
#dataFile = open('HWwk6_2sat_example.txt', 'r')
dataFile = open('HWwk6_2sat6.txt', 'r')

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
del V[0]
print "Read file: ", time.time() - start_time

V_rev = []                                # will contain the vertices in post-visit order
vOrder = 0                                # global variable to assign pre- and post-visit order for each vertex
while len(V) > 0:                         # visit all vertices in the reverse of the original graph
    depthFirst_Rev()                      # and return V_rev with vertices added in post-visit order

for v in V_rev:                           # re-initialize vertex traversal history
    v.pre = 0
    v.post = 0
    v.visited = False
print "Calculate V_rev:", time.time() - start_time

V_done = []                               # V_done will contain the vertices from V_rev that have been explored and had .cc value assigned
vOrder = 0
ccIndex = 0                               # just need indices of connected components, not lists of vertices in connected components
while len(V_rev) > 0:
    ccIndex += 1
    depthFirst()

print "Calculate V_done:", time.time() - start_time
print "Found", ccIndex, "connected components"

for v in V_done:
    v_neg = v.negation
    if v.cc == v_neg.cc:
        print "Found variable:", v.index, "and", v_neg.index, "in connected component", v.cc
        print "2SAT clauses cannot be satisfied"
        print "Completed:", time.time() - start_time
        exit()

print "2SAT clauses can all be satisfied"
print "Completed:", time.time() - start_time
