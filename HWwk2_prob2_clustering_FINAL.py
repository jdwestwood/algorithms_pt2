# Algorithms Pt2 HW 2 problem 2  9/19/2013
#
# Given a set of 200000 nodes, what is the maximum number of clusters for which
# the minimum Hamming distance (no. of bits that are different) between clusters is >= 3.
#
# 1. Calculate the edges of the graph with Hamming distance <= 2.
#    a.  Strategy is to check all possible combinations of bit positions taken two at a time:
#    b.  Move the two bits of interest to the first and second least significant bit
#        positions by exchanging them with the bits originally in those positions;
#        the resulting number is stored in node.testNum.
#    c.  Sort the node list by node.testNum.
#    d.  Nodes whose testNum values differ by at most 2 bits will have values within
#        3 (2**2 - 1) of each other; check each node with its neighbors in the
#        sorted list to see if any are within Hamming distance 2.
#    e.  Similarly, nodes whose testNum values differ by at most 1 bit (the least
#        significant bit) will have values within 1 of each other; check each node with
#        its neighbors to see if any are within Hamming distance 1.
#    f.  Add indices of the node pairs together with the Hamming distance to the edgeList.
# 2. Iterate through the edges and use path compression to find the number of clusters in
#    the graph.
#
# see slides-greedy-algo2-greedy-clustering.pdf's from lecture notes.
# running on my laptop computer is faster; problem is CPU intensive

from sys import exit       # allows me to exit the program early using exit(0)
import time                # allows me to time the execution of various parts of code

class node:
    origNum = 0            # the binary string interpreted as an unsigned int
    testNum = 0            # will contain bit-manipulated version of origLabel
    parent = 0
    rank = 0

class edge:
    n1 = 0
    n2 = 0
    dist = float("inf")      # the Hamming distance

def appendEdge(edgeList, i, j, dist):
    curEdge = edge()
    curEdge.n1 = i
    curEdge.n2 = j
    curEdge.dist = dist
    edgeList.append(curEdge)

def swapBits(num, bitA, bitB):
# swap bits in positions A and B of num, assuming num is an unsigned int
    maskA = 2**bitA                     # 1 in the bitA position
    maskB = 2**bitB                     # 1 in the bitB position
    swappedNum = num & ~maskA & ~maskB  # clear the bits in positions A and B of num
    if num & maskA == maskA:
        swappedNum = swappedNum | maskB # if 1 in bitA, put 1 in bitB
    if num & maskB == maskB:
        swappedNum = swappedNum | maskA # if 1 in bitB, put 1 in bitA
    return swappedNum

def getRoot(node, nodeList):
    parentIndex = node.parent
    while node != nodeList[parentIndex]:
        node = nodeList[parentIndex]
        parentIndex = node.parent
    return node

def pathCompress(node, root, nodeList):
    parentIndex = node.parent
    node.parent = root.parent
    while node != nodeList[parentIndex]:
        node = nodeList[parentIndex]
        parentIndex = node.parent
        node.parent = root.parent

dataFile = open('HWwk2_prob2_clustering_big.txt', 'r')
#dataFile = open('HWwk2_prob2_short1.txt', 'r')

header = dataFile.readline().split()
nNodes = int(header[0])
nBits = int(header[1])
print nNodes, nBits

edgeList = []
nodeList = []
nodeIndex = 0
for line in dataFile:     # read nodes into array of node objects
    curNode = node()
    curNode.origNum = int(line.replace(" ",""),2)  # interpret string as binary number
    curNode.testNum = curNode.origNum
    curNode.parent = nodeIndex                     # parent of each node is itself
    nodeList.append(curNode)
    nodeIndex += 1

# find all node pairs with Hamming distance <= 2 and add them to edgeList (see implementation
# description above).
for newBit0 in xrange(nBits-1):              # 0 to nBits-2
    print "Swapping bit 0 for bit", newBit0
    for curNode in nodeList:
        if newBit0 == 0:
            break
        curNode.testNum = swapBits(curNode.origNum, 0, newBit0)
    for newBit1 in xrange(newBit0+1, nBits): # newBit0+1 to nBits-1
        for curNode in nodeList:            # swap bits for each node
            if newBit1 == 1:
                break
            curNode.testNum = swapBits(curNode.testNum, 1, newBit1)
        nodeList.sort(key=lambda node: node.testNum)  # ascending order
        start_time = time.time()
        i = 0
        while i < nNodes-1:                 # search through pairs of nodes for
            curNode = nodeList[i]           # two bit differences in the bit 0 and
            j = i + 1                       # bit 1 positions
            while j < nNodes:
                nextNode = nodeList[j]
                numDiff = nextNode.testNum - curNode.testNum
                if numDiff <= 3:
                    aa = 1
                    bit10i = curNode.testNum & 3
                    bit10j = nextNode.testNum & 3
                    if bit10i == 0:
                        if bit10j == 3:
                            appendEdge(edgeList, curNode.parent, nextNode.parent, 2)
                    if bit10i == 1:
                        if bit10j == 2:
                            appendEdge(edgeList, curNode.parent, nextNode.parent, 2)
                else:
                    break
                j += 1
            i += 1
        end_time = time.time()
        print "Time for loop bit0, bit1:", newBit0, newBit1, end_time - start_time

    # now look for single bit differences in bit position 0
    i = 0
    while i < nNodes-1:                     # search through pairs of nodes for
        curNode = nodeList[i]               # single bit differences in the bit 0
        j = i + 1                           # position
        while j < nNodes:
            nextNode = nodeList[j]
            numDiff = nextNode.testNum - curNode.testNum
            if numDiff == 1:
                bit10i = curNode.testNum & 3
                bit10j = nextNode.testNum & 3
                if bit10i == 0:
                    if bit10j == 1:
                        appendEdge(edgeList, curNode.parent, nextNode.parent, 1)
                if bit10i == 2:
                    if bit10j == 3:
                        appendEdge(edgeList, curNode.parent, nextNode.parent, 1)
            else:
                break
            j += 1
        i += 1
# still need to check: single bit difference only in the most significant bit,
# which is now in the bit 1 position; also find the duplicate nodes.
i = 0
while i < nNodes-1:                     # search through pairs of nodes for
    curNode = nodeList[i]               # single bit differences in the bit 0
    j = i + 1                           # position
    while j < nNodes:
        nextNode = nodeList[j]
        numDiff = nextNode.testNum - curNode.testNum
        if numDiff == 0:                # duplicate nodes
            appendEdge(edgeList, curNode.parent, nextNode.parent, 0)
        if numDiff == 2:
            bit10i = curNode.testNum & 3
            bit10j = nextNode.testNum & 3
            if bit10i == 0:
                if bit10j == 2:
                    appendEdge(edgeList, curNode.parent, nextNode.parent, 1)
            if bit10i == 1:
                if bit10j == 3:
                    appendEdge(edgeList, curNode.parent, nextNode.parent, 1)
        else:
            break
        j += 1
    i += 1

#print "edgeList:", [(curEdge.n1, curEdge.n2, curEdge.dist) for curEdge in edgeList]
#exit(0)

# edgeList now contains all edges with Hamming distance <= 2.  Sort this list and
# and use clustering algorithm to assign each edge to a tree.
edgeList.sort(key=lambda edge: edge.dist)
nodeList.sort(key=lambda node: node.parent)
nTree = len(nodeList)
print "Forming clusters..."
for curEdge in edgeList:
    nodeIndex1 = curEdge.n1
    nodeIndex2 = curEdge.n2
    node1 = nodeList[nodeIndex1]
    node2 = nodeList[nodeIndex2]
    node1root = getRoot(node1, nodeList)
    node2root = getRoot(node2, nodeList)
    if node1root != node2root:          # nodes belong to different trees; merge trees
        nTree -= 1
        if node1root.rank >= node2root.rank:
            pathCompress(node1, node1root, nodeList) # add tree 2 under tree 1 and
            pathCompress(node2, node1root, nodeList) # compress paths
            if node1root.rank == node2root.rank:
                node1root.rank += 1
        else:
            pathCompress(node1, node2root, nodeList) # add tree 1 under tree 2 and
            pathCompress(node2, node2root, nodeList) # compress paths 
            if node2root.rank == node1root.rank:
                node2root.rank += 1

print "The value of k for k-clustering with spacing >= 3 is:", nTree
