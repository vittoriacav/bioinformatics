#Maria Vittoria Cavicchioli assignemnt 1
#Needleman & Wunsch algorithm (global alignment)

"""This module will be used later to copy the initialized matrix into another
that will be used to keep track of the movements"""
import copy

"""This two functions are used in the end to create a string from the 
list that is manipulated in the program and then to reverse it to display the 
user the sequences in the order in which he entered them"""
def joinList(l):
    return ' '.join(l)

def reverseString(s):
    return s[::-1]

#scores
match = 1
mismatch = -1 
gap = -2

#I get from the user the 2 sequences
seq1 = input("SEQUENCE 1:   ")
seq2 = input("SEQUENCE 2:   ")

#I transform the two strings in lists so I can easily handle them
seq1 = list(seq1)
seq2 = list(seq2)

"""I insert in the sequence1 two spaces that will accomodate the first two additional 
columns in the matrix (first with sequence2 and second with the progressive gap penalties)"""
seq1.insert(0, " ")
seq1.insert(0, " ")

"""I calculate the lenght of the sequeces that will also be the dimensions of the matrix
For the m dimension I add 2 since later in the code the matrix will be constructed with 2 additional 
rows before sequence2 starts (first with sequence1 and second with the progressive gap penalties)"""
n = len(seq1)
m = len(seq2)+2

#This piece of code construct the two first rows of the matrix
row1=[" "]
for i in range(n-1):
    row1.append(i*-2)
M = [seq1, row1]

"""Here I fill the matrix adding subsequential rows that has in the first cell the nucleotide,
in the second the gap penalty and all the other with a 0 that will be filled later with scores"""
i = 2
while i < m:
    c = (i-1)*(-2)
    row = [seq2[i-2], c]
    for j in range(n-2):
        row.append(0)
    M.append(row)
    i += 1

#With deepcopy I copy the M matrix content to another matrix with a differet reference (that's why I need to use deepcopy)
Mb = copy.deepcopy(M)

"""This two for loops scan all the cells (excluding the first two columns and rows), and assign them a score
following the Needleman & Wunsch scoring method and using score values decided at the beginning"""
for i in range(2, m):
    for j in range(2, n):
        up = M[i-1][j]+gap
        right = M[i][j-1]+gap
        if M[0][j] == M[i][0]:
            diag = M[i-1][j-1] + match
        else: 
            diag = M[i-1][j-1] + mismatch
        score = max(up, right, diag)
        M[i][j] = score
        
        #I write in the "backtracking matrix" (Mb) the movements that I'm performing
        if score == up:
            Mb[i][j] = "up"
        elif score == right:
            Mb[i][j] = "right"
        else:
            Mb[i][j] = "diag"

#I create the empty lists that will accomodate the alignment
str1 = []
spacer = []
str2 = []

"""Starting from the last cell of the "backtracking matrix" Mb the backtracking starts, checking what direction the cell contains.
Depending on it the strings are created """
r = m-1
c = n-1
while r!=1 or c!=1:
    if Mb[r][c]== "up":
        str1.append(M[r][0])
        spacer.append(" ")
        str2.append("-")
        r -= 1   
    elif Mb[r][c]== "diag":
        str1.append(M[r][0])
        str2.append(M[0][c])
        if Mb[r][0] == Mb[0][c]:
            spacer.append("*")
        else:
            spacer.append("|")
        r -= 1  
        c -= 1 
    else:
        str1.append("-")
        spacer.append(" ")
        str2.append(M[0][c])
        c -= 1   

print("\n")
print(reverseString(joinList(str1)))
print(reverseString(joinList(spacer)))
print(reverseString(joinList(str2)))
print("\n")

#To print normal matrix or backtracking matrix:
'''for row in M:
    print (row)   
print("\n")
for row in Mb:
    print (row)
'''