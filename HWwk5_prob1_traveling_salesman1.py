# Algorithms Pt2 HW 4 problem 1  10/1/2013
#
# File format is:
# [no. of cities], followed by [x][y] coordinates ... , one city per line
# Find length of the shortest round trip path visiting each city (except the starting city) exactly once.
#
# See slides-npc-algo2-np-exact5-traveling-salesman-dynamic.pdf from lecture notes for the algorithm
#
# Basic algorithm is:
#   1. Read in the data and calculate the distances Cij between all pairs of cities; populate the vertex and edge lists
#   2. Set up and initialize the matrix A[nVertex][nCombinations]. nCombinations is the number of unique combinations
#      of vertices, containing at least two vertices and containing vertex 1 (which is an arbitrary vertex, the
#      starting point of the trip.
#   3. There are 2**nVertex combinations of vertices, and 2**(nVertex-1) combinations containing vertex 1. It is
#      convenient to map a vertex combination to an index in A by representing each combination as a binary number:
#      each digit of the number represents a vertex; the value is 1 if the vertex is present in a particular
#      combination, and zero if it is absent. The base10 representation is the index of the combination in A. 
#   4. Then the algorithm is:
#        For each vertex combination size 2 to nVertex
#          For each possible combination S of the given size that contains vertex 1
#            For each possible final vertex j in the combination (any vertex in the combination except vertex 1)
#              The shortest path from vertices 1 to j A[S,j] containing only the vertices in S is
#                 min k in S, k!=j ( A[S-{j},k] + Ckj )
#        Return min j =2..n ( A[{all vertices},j] + Cj1 )
#
# 10/7/13: ran program on the problem datasets:
#    Graph 1: BF found negative cost cycle.

from sys import exit, maxint   # allows me to exit the program early using exit(0)
import time                    # allows me to time the execution of various parts of code
import heapq

class city:
    def __init__(self, x, y):
        self.x = x  # index of the vertex in V
        self.y = y  # index of the vertex in V

class subset:
    def __init__(self, size, binRep, positions):
        self.size = size
        self.binRep = binRep
        self.positions = positions
    def __cmp__(self, other):
        return cmp(self.size, other.size)

class binrep:
    def __init__(self):
        self.nOnes = 0
        self.onesPositions = []

#dataFile = open('HWwk5_tsp_example2.txt', 'r')
#dataFile = open('HWwk5_tsp_example.txt', 'r')
dataFile = open('HWwk5_tsp.txt', 'r')

header = dataFile.readline().split()
n = int(header[0])
print n

# read in city coordinates
V = [city(0,0)]                           # dummy city at index 0
for line in dataFile:                     # read items into array of item objects
    cityCoord = line.split()
    V.append(city(float(cityCoord[0]), float(cityCoord[1])))

# initialize cost array
c = [[0 for jCity in xrange(0, n+1)] for iCity in xrange(0, n+1)]
for i in xrange(1, n+1):
    for j in range(i, n+1):
        c[i][j] = int(round(10000*(((V[i].x - V[j].x)**2 + (V[i].y - V[j].y)**2)**0.5)))
        c[j][i] = c[i][j]

# initialize pre-computed array of powers of 2, used to create a binary number representing the subset
# of vertices without vertex j
mask_j = [0] + [~(2**(j-1)) for j in xrange(1, n+1)]      # mask_j[0] is a dummy list entry
bit_j = [0] + [2**(j-1) for j in xrange(1, n+1)]

# nSubsets = [0 for sSize in xrange(0, n)]
# S = create_subsets(n-1, nSubsets)               # create a min-heap of the subsets of all vertices except vertex 1

def makeS(S_1, digits):
    # given a dictionary of subsets S_1 containing all subsets containing nV_1 vertices, return
    # the dictionary containing all subsets of size nV_1 + 1; digits is the number of bit positions in the
    # binary representation of a subset, i.e., the number of vertices being permuted
    global bit_j
    S = dict()
    iSubset = 0                                 # index of a new subset
    for subset in S_1.items():
        binRep_1  = subset[0]                   # key is the binary representation of the subset
        bitPosList_1 = subset[1]                # value is the list of vertices in the subset
        for bitPos in range(1, digits+1):
            binRep = binRep_1 | bit_j[bitPos]
            if binRep > binRep_1:                 # if bit position bitPos in binRep_1 is 0
                iSubset += 1
                S[binRep] = bitPosList_1 + [bitPos]
            else:                               # stop generating new subsets based on binRep_1
                break                           # if bit position bitPos in binRep_1 is 1
    return S

#for ss in S:
#    print ss.size, ss.binRep, ss.positions

# initialize A; pad the zero indices of both array dimensions with dummy values
A = dict()                               # key is tuple (binary representation, vertex j), like
for j in xrange(0, n+1):                 # the A matrix in the pseudo-code
    A[(0,j)] = maxint
A[(0,1)] = 0
S = {0 : []}        # key is the binary representation of the subset, value is the list of vertices in S

start = time.time()
for subSize in xrange(1, n):             # for all subset sizes
    end = time.time()
    print "Time: ", end - start
    start = time.time()
    print "Processing subsets of size", subSize
    S = makeS(S, n-1)
    A_1 = A
    A = dict()
    for subset in S.items():
        binRep = subset[0]               # key of the dictionary entry
        vertices = subset[1]             # second member of the tuple value
#        print "binRep, vertices", binRep, vertices
        for v in vertices:               # for each vertex in S
            j = v + 1                    # vertex number = bit position + 1
            binRep_j = binRep & mask_j[v]   # remove vertex v (i.e., j) from binRep
            minCost = maxint
            for u in [0] + vertices:
                k = u + 1                 # vertex number = bit position + 1
                if k != j or binRep_j == 0:
                    minCost_k = A_1.get((binRep_j, k))
#                    print "    j, binRep_j, k, minCost_k:", j, binRep_j, k, minCost_k
                    if minCost_k != None:
                        minCost = min(minCost, minCost_k + c[k][j])
            A[(binRep, j)] = minCost
#            print "binRep, j, A[(binRep,j)]:", binRep, j, A[(binRep,j)]
minCost = maxint
key = S.items()[0][0]                     # only one entry in S
for j in xrange(2, n+1):
    minCost = min(minCost, A[(key,j)] + c[j][1])  # s_Index is 1 for the last subset in S, which contains all vertices except the first

#exit(0)

print "The minimum distance for a circuit visiting all vertices once and returning to the beginning is:", float(minCost)/10000
