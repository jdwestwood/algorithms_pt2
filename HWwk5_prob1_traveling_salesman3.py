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
#   2. Set up and initialize the dict A whose keys are tuples (binary representation, vertex j), and whose values are
#      the minimum length paths computed at each iteration of the algorithm. Vertex 1 is the starting point of the trip.
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
#   6. Need to store only A_1 and S_1, which are the A matrix and S dict from the previous iteration, in order to
#      calculate A and S for the current iteration.
#
# 10/7/13: Changed A from a 'matrix' (list of lists), to a dictionary.  Should consume less memory since A is a somewhat
#      sparse array. Stop computing the vertex list associated with every subset at the outset, which will also save
#      memory. Compute the subsets for the current iteration from the subsets from the previous iteration.
#      Program still runs out of memory and runs very slowly. Try using numpy array for A to speed things up.

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
c = [[0.0 for jCity in xrange(0, n+1)] for iCity in xrange(0, n+1)]
for i in xrange(1, n+1):
    for j in range(i, n+1):
        c[i][j] = ((V[i].x - V[j].x)**2 + (V[i].y - V[j].y)**2)**0.5
        c[j][i] = c[i][j]

# initialize pre-computed array of powers of 2, used to create a binary number representing the subset
# of vertices without vertex j
mask_j = [0] + [~(2**(j-1)) for j in xrange(1, n+1)]      # mask_j[0] is a dummy list entry
bit_j = [0] + [2**(j-1) for j in xrange(1, n+1)]


def get_vertices(binRep, m, n, maxCount):
# return a list of the bit positions between m and n inclusive containing a 1
    nDigits = n - m + 1
    mask = (2**(nDigits) - 1) << (m - 1)     # 1's in positions m through n
    if mask & binRep == mask:
        return [k for k in xrange(m, n+1)]
    elif nDigits > 1:
        midpt = (m + n)//2
        list1 = get_vertices(binRep, m, midpt, maxCount)
        if len(list1) == maxCount:
            return list1
        else:
            list2 = get_vertices(binRep, midpt+1, n, maxCount-len(list1))
            if len(list2) == maxCount:
                return list2
            else:
                return list1 + list2
    else:
        return []

def makeS(S_1, digits):
    # given a dictionary of subsets S_1 containing all subsets containing nV_1 vertices, return
    # the dictionary containing all subsets of size nV_1 + 1; digits is the number of bit positions in the
    # binary representation of a subset, i.e., the number of vertices being permuted
    global bit_j
    S = set()                                   # is a set of binary representations of vertices
    for binRep_1 in S_1:
        for bitPos in range(1, digits+1):
            binRep = binRep_1 | bit_j[bitPos]
            if binRep > binRep_1:               # if bit position bitPos in binRep_1 is 0
                S.add(binRep)
            else:                               # stop generating new subsets based on binRep_1
                break                           # if bit position bitPos in binRep_1 is 1
    return S

A = dict()                               # key is tuple (binary representation, vertex j), like
for j in xrange(0, n+1):                 # the A matrix in the pseudo-code
    A[(0,j)] = float("inf")
A[(0,1)] = 0.0
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
    for binRep in S:
        vertices = get_vertices(binRep, 1, n-1, subSize)
        for v in vertices:               # for each vertex in S
            j = v + 1                    # vertex number = bit position + 1
            binRep_j = binRep & mask_j[v]   # remove vertex v (i.e., j) from binRep
            minCost = float("inf")
            for u in [0] + vertices:
                k = u + 1                 # vertex number = bit position + 1
                if k != j or binRep_j == 0:
                    minCost_k = A_1.get((binRep_j, k))
                    if minCost_k != None:
                        minCost = min(minCost, minCost_k + c[k][j])
            A[(binRep, j)] = minCost
minCost = float("inf")
binRep = S.pop()                             # only one entry in S
for j in xrange(2, n+1):
    minCost = min(minCost, A[(binRep,j)] + c[j][1])  # s_Index is 1 for the last subset in S, which contains all vertices except the first

#exit(0)

print "The minimum distance for a circuit visiting all vertices once and returning to the beginning is:", minCost
