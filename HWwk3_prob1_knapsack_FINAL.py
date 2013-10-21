# Algorithms Pt2 HW 3 problem 1  9/19/2013
#
# File format is:
# [knapsack_size][number_of_items], followed by [value1][weight1] ... , one item per line
# Maximum value of items in knapsack, subject to total weight <= knapsack size
#
# see slides-dp-algo2-dp-knapsack.pdf's from lecture notes
#
# Implement the algorithm as given in the notes.  The problem is small, so no storage
# optimizations are needed.
#
# 9/26/13: ran program on the problem dataset and obtain 2493893 for the maximum value.

from sys import exit       # allows me to exit the program early using exit(0)
import time                # allows me to time the execution of various parts of code

class item:
    value = 0
    weight = 0

dataFile = open('example10.txt', 'r')
#dataFile = open('HWwk3_prob1_knapsack_example.txt', 'r')
#dataFile = open('HWwk3_prob1_knapsack.txt', 'r')

header = dataFile.readline().split()
knapSize = int(header[0])
nItem = int(header[1])
print knapSize, nItem

# create the knapsack value array A[iItem][jWeight]
A = [[0 for jWeight in range(knapSize+1)] for iItem in range(nItem+1)]  # will use the 0 indices in the algorithm

itemList = []
itemList.append(item())                    # add empty item to occupy the 0-index position
for line in dataFile:                      # read items into array of item objects
    itemData = line.split()
    curItem = item()
    curItem.value = float(itemData[0])
    curItem.weight = int(itemData[1])
    itemList.append(curItem)

# use knapsack algorithm without optimizing the array storage strategy.

for iItem in range(1,nItem+1):                   # 1 to nItem-1
    for jWeight in range(knapSize+1):            # 0 to knapSize
        noItem_i = A[iItem-1][jWeight]
        if jWeight - itemList[iItem].weight >= 0:
            withItem_i = A[iItem-1][jWeight - itemList[iItem].weight] + itemList[iItem].value
        else:
            withItem_i = 0
        A[iItem][jWeight] = max(noItem_i, withItem_i)

print "The maximum value for items in the knapsack is:", A[nItem][knapSize]
