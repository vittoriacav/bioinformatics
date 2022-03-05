#Maria Vittoria Cavicchioli assignemnt 3
#Burrows-Wheeler transform of a string and string matching implementation

def rotations(t):
    #return list of rotations of input string t
    tt = t * 2
    return [ [tt[i:i+len(t)], i] for i in range(0,len(t))]

def BWT(t):
    #return lexicographically sorted list of t's rotations
    return sorted(rotations(t))

def LastColumn(t):
    #given t, returns BWT(T) by way of the last column of the matrix
    return ''.join(map(lambda x: x[0][-1], BWT(t)))

def offesetsArrayCreator(t):
    #given t, returns the offsets of BWT(t)
    offesetsArray = []
    dataset = BWT(t)
    for i in dataset:
        offesetsArray.append(i[1])
    return offesetsArray

def stringContentDictionay(t):
    #given t, returns a dictionary where keys are all kinds of characters found in t and the 
    #values are integers representing how many times each character was found in string t
    chr_counter = 0
    chr_kinds = []
    chr_dict = {}

    i = 0
    while i != len(t):
        if t[i] in chr_kinds:
            i += 1 
        else:
            chr_kinds.append(t[i]) 
            for j in t:
                if j == t[i]:
                    chr_counter += 1
            chr_dict[t[i]] = chr_counter
            chr_counter = 0
            i += 1   
    return chr_dict 

def rankCalculator(t, offset):
    #given a string t and an offset of this string, it returns the rank 
    #of the character positioned in that offset
    #ex. t = a0 b0 a1 a2 b1 a3 --> rank at offset 3 (a2) is 2 since 
    #until that point, 'a' occurs 3 times (0, 1, 2)
    rank = 0
    i = 0
    while i <= offset:
        if t[i] == t[offset]:
            rank += 1
        i+=1
    return rank

def nextOffsetCalculator(lastC, offset, stringComposition):
    nextOffset = rankCalculator(lastC, offset) #to calculate next offset, firstly it is added a number equal to the rank of the character at the current offset...
    for i in stringComposition:
        if i < lastC[offset]:
            nextOffset += stringComposition[i] #...then, exploiting the lexicographical order, all the blocks of character before the offset are added
    return nextOffset

def reverseBWT(lastC, offset, stringComposition, originalString, recursionNumber):
    #given the last column (lastC) of a BWT matrix, it returns the orginal string
    #with no need of any other part of the BWT matrix
    recursionNumber += 1
    originalString = lastC[offset] + originalString
    if recursionNumber != len(lastC)-1:
        nextOffset = nextOffsetCalculator(lastC, offset, stringComposition)
        return reverseBWT(lastC, nextOffset, stringComposition, originalString, recursionNumber) #recursive call 
    else:
        return originalString

def matchingAlgo(lastC, offset, stringComposition, query, offsetQuery, offsetsArray):
    #given the last column (lastC) of a BWT matrix and a query that has to be matched, it returns a boolean:
    #True if the matching is present and False if the matching is not present. In case of present matching also 
    #its offset is returned 
    
    if offsetQuery == 0:
        matchOffset = nextOffsetCalculator(lastC, offset, stringComposition)
        return [True, offsetsArray[matchOffset]]
    
    else:
        nextOffset = nextOffsetCalculator(lastC, offset, stringComposition)
        
        if lastC[nextOffset] == query[offsetQuery-1]:
           return matchingAlgo(lastC, nextOffset, stringComposition, query, offsetQuery-1, offsetsArray) 
        
        else:
            return [False]

#User interface
genome_string = input("\nEnter your genome string: ") 
content = stringContentDictionay(genome_string)
genome_string = genome_string + '$'
offsetsArray = offesetsArrayCreator(genome_string)

lastC = LastColumn(genome_string)
print("\nLast Column of the BWT matrix: ", lastC)

originalString = ''
backToOriginal = reverseBWT(lastC, 0, content, originalString, 0)
print("\nCalculation of the original string with the last column only:   ", backToOriginal)
if genome_string[ : -1] != backToOriginal:
    print ("\nERROR")

query = input("\nEnter your query string: ") 

start = 0
if query[-1] in content:
    for c in content:
        if c < query[-1]:
            start += content[c]
    i = start + 1
    end = i + content[query[-1]] 
    
    matchingOffsets = []
    while i != end:
        if lastC[i] == query[-2]:
            check = matchingAlgo(lastC, i, content, query, len(query)-2, offsetsArray)
            if check[0]:
                matchingOffsets.append(check[1])
        i += 1          
else:
    print("\nNo match")

if matchingOffsets:
    print("\nMatching was found at offset/offsets: ", matchingOffsets)
else:
    print("\nNo match")