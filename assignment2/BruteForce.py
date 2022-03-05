#Maria Vittoria Cavicchioli assignment 2
#Brute Force Algorithm to solve SCS problem

import itertools
import random

#The following 2 functions create the input set of substrings
def getGenome(length = 10000):
    genome = "".join(random.choice("AGCT") for i in range(length))
    return genome

def getSubstrings(seq, length = 100):
    L = []
    for i in range(len(seq)-length+1):
        L.append(seq[i:i+length])
    return L

'''These 2 following functions will be used by the core function "updater"
to compute the overlap score between two strings and to merge two strings'''
def computeOverlap(s1, s2):
    i = 1 
    overlap = 0
    while i < len(s1):
        if s1[-i:] == s2[:i]:
            overlap = i
        i += 1
    return overlap

def merger(s1, s2, overlap):
    mergedString = s1 + s2[overlap:]   
    return mergedString

#Core fuction
'''This function takes as argument one specific permutation and create a superstring 
starting from that strings in that order, merging or contatenating them'''
def makeSuperstring(permX):
    superString = ''
    for i in range(len(permX)):
        o = computeOverlap(superString, permX[i])
        if o != 0:
            superString = merger(superString, permX[i], o)
        else:
            superString = superString + permX[i]
    return superString

stringSet = getSubstrings(getGenome(length = 15), length = 6)
'''bestSuperstring is initialized as all the substrings concatenated
since no longer superstring could exist and in this way we can 
appreciate each shorter superstring found'''
bestSuperstring = "".join(stringSet)
currentSuperstring = []

'''with the for loop we scan all possible permutations of a given set of substrings
and we calculate the related superstring. Just the shortest superstring is taken 
in consideration and printed as output'''
for perm in itertools.permutations(stringSet):
    currentSuperstring = makeSuperstring(perm)
    if len(currentSuperstring) < len(bestSuperstring):
        bestSuperstring = currentSuperstring

print("\nSubstrings set: ", stringSet)
print("\nSHORTEST COMMON SUBSTRING: ", bestSuperstring)
