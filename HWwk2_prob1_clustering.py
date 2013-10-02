# Algorithms Pt2 HW 2 problem 1  9/19/2013
#
# Given a set of edges for a complete graph with 500 nodes, what is the maximum
# minimum distance between 4 clusters of nodes.
#
# see slides-greedy-algo2-greedy-clustering.pdf's from lecture notes.
# running on my laptop computer is faster; problem is CPU intensive

from sys import exit       # allows me to exit the program early using exit(0)
import time                # allows me to time the execution of various parts of code

class node:
    parent = 0
    rank = 0

class edge:
    n1 = 0
    n2 = 0
    cost = 0

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

k = 4                     # number of clusters

dataFile = open('HWwk2_prob1_clustering.txt', 'r')
#dataFile = open('HWwk2_prob1_short.txt', 'r')

header = dataFile.readline().split()
nNodes = int(header[0])
print nNodes

edgeList = []
nodeList = []
for line in dataFile:     # read edges into array of edge objects
    edgeData = line.split()
    curEdge = edge()
    curEdge.n1 = int(edgeData[0]) - 1  # to make node numbers begin at 0 instead of 1
    curEdge.n2 = int(edgeData[1]) - 1
    curEdge.cost = int(edgeData[2])
    edgeList.append(curEdge)

# initialize nodes
for i in range(0, nNodes):
    curNode = node()
    curNode.parent = i    # parent is itself
    curNode.rank = 0
    nodeList.append(curNode)

edgeList.sort(key=lambda edge: edge.cost)
iEdge = 0
nTree = len(nodeList)
while nTree >= k:               # use >= to continue to process internal edges
    curEdge = edgeList[iEdge]   # after reaching nTree = k
    nodeIndex1 = curEdge.n1
    nodeIndex2 = curEdge.n2
    node1 = nodeList[nodeIndex1]
    node2 = nodeList[nodeIndex2]
    node1root = getRoot(node1, nodeList)
    node2root = getRoot(node2, nodeList)
    if node1root != node2root:  # nodes in different trees; merge trees
        if nTree != k:          # unless we are about to fall below k trees
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
        else:
            break               # have reached an edge which will reduce nTree below k
    iEdge += 1

print "For k-clustering, k and max min cluster distance are:", k, curEdge.cost
