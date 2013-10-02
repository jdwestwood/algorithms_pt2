# Algorithms Pt2 HW 3 multiple choice question 5  9/29/2013
#
# Use algorithm for binary search tree to compute the expected number of searches,
# given a set of seven probabilities
# see the slides-dp-algo2-dp-bst1-5.pdf files for the algorithm

from sys import exit, maxint    # allows me to exit the program early using exit(0)
import time                # allows me to time the execution of various parts of code

class item:
    value = 0
    weight = 0

p = [0, 0.05, 0.4, 0.08, 0.04, 0.1, 0.1, 0.23]
A = [[0 for j in range(0,8)] for i in range(0,8)]
for s in range(0,7):
    for i in range(1,8-s):           # (typo on slide!)
        sum_pk = 0
        for k in range(i, i+s+1):    # (typo on slide!)
            sum_pk += p[k]
        min_root = maxint
        for r in range(i, i+s+1):    # (typo on slide!)
            min_term = sum_pk
            if r-1 >= i:
                min_term += A[i][r-1]
            if r+1 <= i+s:
                min_term += A[r+1][i+s]
            min_root = min(min_root, min_term)
        A[i][i+s] = min_root

print "The expected number of searches is:", A[1][7]
