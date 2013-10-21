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
#      is used to map a vertex combination, represented as a binary string, to an index in A. Each digit of the
#      binary number represents a vertex; the value is 1 if the vertex is present in a particular
#      subset, and zero if it is absent. The dict allows us to make the subset dimension of the A array only
#      as large as the number of subsets needed for a given interation.
#   4. Calculate all possible subsets at the outset of the program, and store them in a min-heap, according to
#      their size.  The min-heap is a convenient way to get all the subsets of a specified size from smallest to
#      largest as the algorithm progresses.
#   5. Then the algorithm is:
#        For each vertex subset size subSize = 2 to nVertex (including vertex 1):
#          For each possible combination S of the given size that contains vertex 1
#            For each possible final vertex j in the combination (any vertex in the combination except vertex 1)
#              The shortest path from vertices 1 to j A[S,j] containing only the vertices in S is
#                 min k in S, k!=j ( A[S-{j},k] + Ckj )
#        Return min j =2..n ( A[{all vertices},j] + Cj1 )
#   6. Need to store only A_1 and S_1, which are the A matrix and S dict from the previous iteration, in order to
#      calculate A and S for the current iteration.
#
# 10/7/13: Program is running very slowly and will take too long to finish. Try computing the vertex
#      indices in each subset at the outset as part of step 4 above, which is more efficient than computing them
#      separately.

from sys import exit, maxint   # allows me to exit the program early using exit(0)
import time                    # allows me to time the execution of various parts of code
import heapq

class city:
    def __init__(self, x, y):
        self.x = x  # index of the vertex in V
        self.y = y  # index of the vertex in V

class subset:
    def __init__(self, size, binRep):
        self.size = size
        self.binRep = binRep
    def __cmp__(self, other):
        return cmp(self.size, other.size)

class binrep:
    def __init__(self):
        self.nOnes = 0
        self.onesPositions = []

def get_ones_positions(binRep, m, n):
# return a list of the bit positions between m and n inclusive containing a 1
    nDigits = n - m + 1
    mask = (2**(nDigits) - 1) << (m - 1)     # 1's in positions m through n
    if mask & binRep == mask:
        return [k for k in xrange(m, n+1)]
    elif nDigits > 1:
        midpt = (m + n)//2
        return get_ones_positions(binRep, m, midpt) + get_ones_positions(binRep, midpt+1, n)
    else:
        return []

def count_ones(binRep, m, n):
# count the number of 1's between bit positions m through n in the binary representation of the integer binRep
    nDigits = n - m + 1
    mask = (2**(nDigits) - 1) << (m - 1)     # 1's in positions m through n
    if mask & binRep == mask:
        return nDigits
    elif nDigits > 1:
        midpt = (m + n)//2
        return count_ones(binRep, m, midpt) + count_ones(binRep, midpt+1, n)
    else:
        return 0                             # nDigits is 1, but the bit in position m is a 0

def create_subsets(nV, nSubsets):
# create a heap of all subsets of nV vertices, which have binary representations with nV digits
# in the range 1 to 2**nV - 1; nSubsets is a list such that nSubsets[vCount] = the number of subsets
# of size vCount
    subsets = []
    for binRep in xrange(1, 2**nV):    # i.e. 1 to 2**nV - 1
        nVertices = count_ones(binRep, 1, nV)
        heapq.heappush(subsets, subset(nVertices, binRep))
        nSubsets[nVertices] += 1
        if float(binRep)/1000000 == binRep//1000000:
            print "Creating subset", binRep
    return subsets

dataFile = open('HWwk5_tsp_example2.txt', 'r')
#dataFile = open('HWwk5_tsp_example.txt', 'r')
#dataFile = open('HWwk5_tsp.txt', 'r')

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

nSubsets = [0 for sSize in xrange(0, n)]
S = create_subsets(n-1, nSubsets)               # create a min-heap of the subsets of all vertices except vertex 1

# initialize A; pad the zero indices of both array dimensions with dummy values
A = [[float("inf") for j in xrange(0, 2)] for s in xrange(0, n+1)]  # there are n subsets that have 1 vertex
A[1][1] = 0.0                            # distance from vertex 1 to itself
S_list = {'0': 1}                        # create a dictionary
start = time.time()
curSize = 0                              # size of subsets; the vertex 1 was not explicitly included in the subsets in S
for iSubset in xrange(0, len(S)):
    curSubset = heapq.heappop(S)
    if curSubset.size > curSize:         # finished processing the subsets of size curSize
        curSize = curSubset.size         # prepare to process the next group of subsets
        end = time.time()
        print "Time: ", end - start
        start = time.time()
        print "Processing subsets of size", curSize, "of which there are", nSubsets[curSize]
        A_1 = A
        S_list_1 = S_list
        A = [[float("inf") for j in xrange(0,n+1)] for s in xrange(0, nSubsets[curSize] + 1)]
        S_list = dict()                  # the value of the S_list[key] will be the index of key in A
        s_Index = 0
    s_Index += 1
    S_list[str(curSubset.binRep)] = s_Index   # so can later look up values in A_1
    vertex_in_S = get_ones_positions(curSubset.binRep, 1, n-1)
    for v in vertex_in_S:   # for each vertex in the current subset
        j = v + 1           # vertex number = bit position + 1
        binRep_j = curSubset.binRep & mask_j[v]  # remove vertex v (i.e., j) from curSubset
        s_1_Index = S_list_1[str(binRep_j)]   # need dictionary to look up the s Index in A, given the binary representation binRep
        minCost = float("inf")
        for u in [0] + vertex_in_S:      # prepend [0] since k needs to include vertex 1
            k = u + 1                    # vertex number = bit position + 1
            if k != j:
                print "  j, binRep_j, k, A_1[s_1_Index][k]", j, binRep_j, k, A_1[s_1_Index][k]
                minCost = min(minCost, A_1[s_1_Index][k] + c[k][j])
        A[s_Index][j] = minCost
minCost = float("inf")
for j in xrange(2, n+1):
    minCost = min(minCost, A[1][j] + c[j][1])  # s_Index is 1 for the last subset in S, which contains all vertices except the first
#exit(0)

print "The minimum distance for a circuit visiting all vertices once and returning to the beginning is:", minCost
