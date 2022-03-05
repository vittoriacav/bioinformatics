#Maria Vittoria Cavicchioli assignment 2
#Greedy Algorithm to solve SCS problem

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
    i = 3 #"the overlap must be at least 3 characters long"
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
'''each time, the updater takes the substrings set as argument and if the length
is more than one (meaning that we have other substrings to merge), a for loop scans 
all the permutations for the set of substrings. For each permutation it computes 
the overlap score...'''
def updater(stringSet):
    weight = 0
    pairToMerge = []
    if len(stringSet) == 1:
        return stringSet
    else:
        for pair in itertools.permutations(stringSet, 2):
            o = computeOverlap(pair[0], pair[1])
            #...with this if-elif block we create a list of the edges having the highest weight
            if o > weight:
                weight = o
                pairToMerge = []
                pairToMerge.append(list(pair))
            elif o == weight:
                pairToMerge.append(list(pair))
        #between the edges having the highest weight, one is chosen randomly and the pair is merged(later)
        chosenPair = random.choice(pairToMerge)
        #than the original pair of single strings merged are removed from the substrings set
        stringSet.remove(chosenPair[0])
        stringSet.remove(chosenPair[1])
        merged = merger(chosenPair[0], chosenPair[1], weight)
        stringSet.append(merged)
        #since the substrings in the set were major than 1, the updater is called again recursively 
        updater(stringSet)
    return stringSet 
        
         
L = getSubstrings(getGenome(length = 15), length = 6)
print("\nSubstrings set: ", L)
print("\nSHORTEST COMMON SUBSTRING: ", updater(L)[0])