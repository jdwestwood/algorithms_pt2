# Algorithms Pt2 HW 3 problem 2  9/26/2013
#
# File format is:
# [knapsack_size][number_of_items], followed by [value1][weight1] ... , one item per line
# Maximum value of items in knapsack, subject to total weight <= knapsack size
#
# see slides-dp-algo2-dp-knapsack.pdf's from lecture notes
# 9/27/13: ran program on problem 1 dataset and obtain 2493893 for the maximum value, with weight 9976.
# 9/27/13: ran program on problem 2 dataset and obtain 2493893 for the maximum value, with weight 9976.

from sys import exit       # allows me to exit the program early using exit(0)
import time                # allows me to time the execution of various parts of code

class item:
    def __init__(self, value=float(0), weight=0):
        self.value = float(value)
        self.weight = weight

class knapState:
    def __init__(self, weight=0, value=float(0)):
        self.weight = weight
        self.value = float(value)

return_wt_index = 0
def findEntry(jWeight, Ai_1, last_wt_index):
    # find the value in list Ai_1 corresponding to the entry A[iItem-1][jWeight].  The list Ai_1 contains only
    # unique knapState (weight, value) entries.  We search through the entries for the one with
    # Ai_1[j-1].weight <= jWeight < Ai_1[j].weight, beginning at j-1 = last_wt_index.
    global return_wt_index
    for j in range(last_wt_index, len(Ai_1)):
        if Ai_1[j].weight > jWeight:
            return_wt_index = j - 1
            return Ai_1[return_wt_index].value
            break
    return_wt_index = j
    return Ai_1[return_wt_index].value

#dataFile = open('HWwk3_prob1_knapsack_example.txt', 'r')
#dataFile = open('HWwk3_prob1_knapsack.txt', 'r')
dataFile = open('HWwk3_prob2_knapsack_big.txt', 'r')

header = dataFile.readline().split()
knapSize = int(header[0])
nItem = int(header[1])
print knapSize, nItem

# For problem 2, just store the values for items i-1 and i, and just store the entries
# for which the total value in the knapsack increases
# create the knapsack value lists for items i-1 and i
itemList = []
itemList.append(item(0,0))                    # add empty item to occupy the 0-index position
for line in dataFile:                      # read items into array of item objects
    itemData = line.split()
    curItem = item(float(itemData[0]), int(itemData[1]))
    itemList.append(curItem)

# use knapsack algorithm using optimized array storage.
Ai = [knapState(0,0)]                          # will use the 0 indices in the algorithm
for iItem in range(1,nItem+1):                 # 1 to nItem
    Ai_1 = Ai
    Ai = [knapState(0,0)]
    last_wt_index = 0                          # index at which to start searching in Ai_1   
    for jWeight in range(knapSize+1):          # 0 to knapSize
        noItem_i = findEntry(jWeight, Ai_1, last_wt_index)    # A[iItem-1][jWeight]
        if jWeight - itemList[iItem].weight >= 0:
            withItem_i = findEntry(jWeight - itemList[iItem].weight, Ai_1, last_wt_index) + itemList[iItem].value
            last_wt_index = return_wt_index    # start all subsequent searches through Ai_1 at the new value of last_wt_index
        else:
            withItem_i = 0
        if withItem_i > noItem_i:
            knapStateEntry = knapState(jWeight, withItem_i)
        else:
            knapStateEntry = knapState(jWeight, noItem_i)
        if knapStateEntry.value > Ai[-1].value:   # add the higher value knapsack state to Ai
            Ai.append(knapStateEntry)

print "The maximum value for items in the knapsack is:", Ai[-1].value, " with weight", Ai[-1].weight
