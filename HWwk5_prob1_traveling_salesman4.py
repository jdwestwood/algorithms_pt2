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
#   2. Set up and initialize the matrix A[subset index][vertex index], which will contain the minimum length paths
#      computed at each iteration of the algorithm. Vertex 1 is the starting point of the trip.
#   3. There are 2**nVertex subsets of vertices, and 2**(nVertex-1) subsets containing vertex 1. A Python dict S
#      is used to map a vertex combination, represented as a binary string, to the list of vertices in the subset.
#      Each digit of the binary number represents a vertex; the value is 1 if the vertex is present in a particular
#      subset, and zero if it is absent.
#   4. Calculate possible subsets for the current iteration from the subsets from the previous iteration to save
#      memory.
#   5. Then the algorithm is:
#        For each vertex subset size subSize = 2 to nVertex (including vertex 1):
#          For each possible combination S of the given size that contains vertex 1
#            For each possible final vertex j in the combination (any vertex in the combination except vertex 1)
#              The shortest path from vertices 1 to j A[(S,j)] containing only the vertices in S is
#                 min k in S, k!=j ( A[(S-{j},k)] + Ckj )
#        Return min j =2..n ( A[({all vertices},j)] + Cj1 )
#   6. Need to store only S_1, which is the S dict from the previous iteration, in order to calculate S for the current
#      iteration.  The A matrix is full size here, so no need for A_1 as in previous versions.
#
# 10/7/13: Go back to implementing A as a matrix, but use a matrix of integers instead of floats to save memory.
#      (Multiply all floats by 10000 and round to nearest integer in order to be able to get away with this!).  
#      implement A as a large simple matrix with dimensions A[total number of subsets][nVertices]. Continue to compute
#      the subsets for the current iteration from the subsets from the previous iteration. Program still runs out of
#      memory so need to go back to implementing A and A_1 the same way I did initially (except will use int instead of
#      float).

from sys import exit, maxint   # allows me to exit the program early using exit(0)
import time                    # allows me to time the execution of various parts of code

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

S = {0 : []}        # key is the binary representation of the subset, value is the list of vertices in S
A = [[maxint for j in xrange(0, n+1)] for s in xrange(0, 2**(n-1))]
A[0][1] = 0

start = time.time()
for subSize in xrange(1, n):             # for all subset sizes
    end = time.time()
    print "Time: ", end - start
    start = time.time()
    print "Processing subsets of size", subSize
    S = makeS(S, n-1)
    for subset in S.items():
        binRep = subset[0]               # key of the dictionary entry
        vertices = subset[1]             # second member of the tuple value
        for v in vertices:               # for each vertex in S
            j = v + 1                    # vertex number = bit position + 1
            binRep_j = binRep & mask_j[v]   # remove vertex v (i.e., j) from binRep
            minCost = maxint
            for u in [0] + vertices:
                k = u + 1                 # vertex number = bit position + 1
                if k != j:   # or binRep_j == 0:
                    minCost = min(minCost, A[binRep_j][k] + c[k][j])
            A[binRep][j] = minCost
minCost = maxint
key = S.items()[0][0]                     # only one entry in S
for j in xrange(2, n+1):
    minCost = min(minCost, A[key][j] + c[j][1])  # s_Index is 1 for the last subset in S, which contains all vertices except the first

#exit(0)

print "The minimum distance for a circuit visiting all vertices once and returning to the beginning is:", float(minCost)/10000
