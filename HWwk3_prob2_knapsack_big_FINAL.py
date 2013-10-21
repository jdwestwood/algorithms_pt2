# Algorithms Pt2 HW 3 problem 2  9/26/2013
#
# File format is:
# [knapsack_size][number_of_items], followed by [value1][weight1] ... , one item per line
# Maximum value of items in knapsack, subject to total weight <= knapsack size
#
# see slides-dp-algo2-dp-knapsack.pdf's from lecture notes for the dynamic programming algorithm.
#
# Challenge with this big dataset is to use storage efficiently:
#   1. Store values only for Ai (the current iteration) and Ai_1 (the previous iteration).
#   2. Store values for Ai and Ai_1 only for weights where the value changes.
#   3. Use recursion to calculate the needed Ai values more efficiently than simply
#      iterating through all knapSize entries.
#
# 9/29/13: ran program on problem 1 dataset and obtain 2493893 for the maximum value, with weight 9976.
# 9/27/13: ran program on problem 2 dataset and obtain 4243395 for the maximum value, with weight 1999783.

from sys import exit       # allows me to exit the program early using exit(0)
import time                # allows me to time the execution of various parts of code

class item:
    def __init__(self, value=float(0), weight=0):
        self.value = float(value)
        self.weight = weight

class A_entry:
    def __init__(self, weight, value, i_prev, i_self, i_next):
        self.weight = weight
        self.value = float(value)
        self.i_prev = i_prev
        self.i_self = i_self
        self.i_next = i_next

def fill_Ai(itemEntry, Ai, Ai_start, Ai_end):
# recursively fill the Ai list; entries in Ai are instances of the A_entry class
    if Ai_end.weight - Ai_start.weight < 2:     # no more mid weights to calculate
        return
    Ai_midWeight = (Ai_start.weight + Ai_end.weight)//2
    Ai_midValue = getAijValue(itemEntry, Ai_midWeight, Ai_1)
    if Ai_start.value == Ai_midValue and Ai_midValue == Ai_end.value:
        # do not insert Ai_mid
        # do not call fill_Ai for either interval
        print "Found equal values in fill_Ai; this should never happen!"
    if Ai_start.value < Ai_midValue and Ai_midValue == Ai_end.value:
        # replace Ai_end by Ai_mid - all that needs to be updated is the weight
        Ai_end.weight = Ai_midWeight
        fill_Ai(itemEntry, Ai, Ai_start, Ai_end)
    if Ai_start.value == Ai_midValue and Ai_midValue < Ai_end.value:
        # temporarily change the weight of Ai_start.weight to Ai_midWeight to restrict the search range; do not insert Ai_mid
        Ai_start_origWeight = Ai_start.weight
        Ai_start.weight = Ai_midWeight
        fill_Ai(itemEntry, Ai, Ai_start, Ai_end)
        Ai_start.weight = Ai_start_origWeight
    if Ai_start.value < Ai_midValue and Ai_midValue < Ai_end.value:
        # create Ai_mid and insert it
        Ai_mid = A_entry(Ai_midWeight, Ai_midValue, Ai_start.i_self, len(Ai), Ai_end.i_self)  # will append to the end of Ai
        Ai_start.i_next = Ai_mid.i_self
        Ai_end.i_prev = Ai_mid.i_self
        Ai.append(Ai_mid)
        fill_Ai(itemEntry, Ai, Ai_start, Ai_mid)
        fill_Ai(itemEntry, Ai, Ai_mid, Ai_end)

def findValue(jWeight, Ai_1):
# search down through the Ai_1 tree to find the value of Ai_1 for jWeight
    curIndex = 3
    if len(Ai_1) == 3:
        curIndex = 0
    Ai_1_cur = Ai_1[curIndex]
    while not (Ai_1_cur.weight <= jWeight and jWeight < Ai_1[Ai_1_cur.i_next].weight):
        if jWeight > Ai_1_cur.weight:
            curIndex = Ai_1_cur.i_next
        elif jWeight < Ai_1_cur.weight:
            curIndex = Ai_1_cur.i_prev
        else:
            return Ai_1_cur.value
        Ai_1_cur = Ai_1[curIndex]
    return Ai_1_cur.value

def getAijValue(itemEntry, jWeight, Ai_1):
# return the value of A[itemIndex][jWeight], where itemEntry = itemList[itemIndex]
    noItem_i = findValue(jWeight, Ai_1)        # A[iItem-1][jWeight]
    if jWeight - itemEntry.weight >= 0:
        withItem_i = findValue(jWeight - itemEntry.weight, Ai_1) + itemList[iItem].value
    else:
        withItem_i = 0
    if withItem_i > noItem_i:
        return withItem_i
    else:
        return noItem_i

#dataFile = open('example10.txt', 'r')
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
itemList.append(item(0,0))                 # add empty item to occupy the 0-index position
for line in dataFile:                      # read items into array of item objects
    itemData = line.split()
    curItem = item(float(itemData[0]), int(itemData[1]))
    itemList.append(curItem)

# use knapsack algorithm using optimized array storage.
Ai_1 = []
Ai = [A_entry(0, 0, 0, 0, 1), A_entry(knapSize, 0, 0, 1, 2), A_entry(knapSize, 0, 1, 2, 2)]  # will use the item 0 index in the algorithm
for iItem in range(1,nItem+1):                 # 1 to nItem
    del Ai_1
    Ai_1 = Ai
    # initialize the weight 0 and weight knapSize endpoints of Ai
    Ai_knapSize = getAijValue(itemList[iItem], knapSize, Ai_1)
    Ai = [A_entry(0, 0, 0, 0, 1), A_entry(knapSize, Ai_knapSize, 0, 1, 2), A_entry(knapSize, Ai_knapSize, 1, 2, 2)]
    fill_Ai(itemList[iItem], Ai, Ai[0], Ai[1]) # calculated the needed values of Ai recursively; Ai[2] is always for weight knapSize; A[1] weight will change
    print "Done iteration", iItem

print "The maximum value for items in the knapsack is:", Ai[1].value, " with weight", Ai[1].weight
