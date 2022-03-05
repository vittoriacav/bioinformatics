#Maria Vittoria Cavicchioli assignemnt 4
#Compute the inside and outside CpG island models, and use them
#for scoring a query sequence

import csv
import itertools  
import random
import math

#Function used to calculate the outside and inside models

def calculateModel(alphabet, all_dimers, dataset):
    
    #CALCULATION DIMER FREQUENCIES
    
    #Construction of the the "emtpy" dictionary that will accomodate 
    # the frequencies of each dimer
    dimers_freq = {}
    for oneDimer in all_dimers:
        key = oneDimer[0]+oneDimer[1]
        dimers_freq[key] = 0

    for nt in alphabet:
        key = nt+"X"
        dimers_freq[key] = 0

    #Fill the dictionary with the frequencies of each dimer
    for oneSeq in dataset:
        for nt in alphabet:
            key = nt+"X"
            dimers_freq[key] += oneSeq[:-1].count(nt)
        for oneDimer in dimers_freq:
            N = 0
            while N < len(oneSeq)-1:
                if oneDimer[0] == oneSeq[N]:
                    if oneDimer[1] == oneSeq[N+1]:
                        dimers_freq[oneDimer] += 1
                N += 1  

    #CALCULATION CONDITIONAL PROBABILITIES 

    #Construction of the the "emtpy" dictionary that will accomodate 
    # the conditional probability of each dimer
    dimers_condProb = {}
    for oneDimer in all_dimers:
        key = oneDimer[0]+"|"+oneDimer[1]
        dimers_condProb[key] = 0

    #Fill the dictionary with the conditional probability of each dimer
    for one_condProb in dimers_condProb:
        for one_freq in dimers_freq:
            if one_condProb[2] + one_condProb[0] == one_freq:
                dimers_condProb[one_condProb] = round(dimers_freq[one_freq]/dimers_freq[one_condProb[2]+"X"], 2)
    
    return dimers_condProb

def getSequence(length):
    sequence = "".join(random.choice("AGCT") for i in range(length))
    return sequence

def calculateLogRatio(sequence, inside_model, outside_model):
    #The two probabilities are set with the probability of 
    #the first nucleotide that is for semplicity = log(0.25)
    inside_prob = outside_prob = math.log(0.25, 10)

    nt = 1
    while nt < len(sequence):
        for outside, inside in zip(outside_model, inside_model):
            #outside probability calculation
            if sequence[nt] == outside[0]:
                if sequence[nt-1] == outside[2]:
                    outside_prob += math.log(outside_model[outside], 10)
            #inside probability calculation
            if sequence[nt] == inside[0]:
                if sequence[nt-1] == inside[2]:                
                    inside_prob += math.log(inside_model[inside],10)
        
        nt += 1

    log_ratio = inside_prob - outside_prob

    return log_ratio

###################################################################

#Read the chromosome 22 file and create a unique sequence

with open('chr22.fa', 'r') as file:
    data = file.read().replace('\n', '')

chr22_seq = data[6:].upper()

#Extract the CpG islands and random sequences
cpg_file = open("cpg_islands.txt")

reader = csv.reader(open('cpg_islands.txt'), delimiter="\t")
reader = list(zip(*reader))
chr_name_list = reader[0]
starts_list = reader[1]
ends_lists = reader[2]
lengths_list = reader[3]

CpGs_list = []
nonCpGs_list =[]

i = 0
while i < len(chr_name_list):
    if chr_name_list[i] == "chr22":
        start = int(starts_list[i]) - 1
        end = int(ends_lists[i])
        CpGs_list.append(chr22_seq[start:end])
        
        random_seq = "N" * int(lengths_list[i])
        while random_seq.count("N") >= int(lengths_list[i]) // 2:
            rStart = random.randint(1 , len(chr22_seq)-int(lengths_list[i])-1)
            rEnd = rStart + int(lengths_list[i])
            random_seq = chr22_seq[rStart:rEnd]

        nonCpGs_list.append(random_seq)
    i += 1

alphabet = ['A', 'C', 'G', 'T']
all_dimers = [p for p in itertools.product(alphabet, repeat=2)]

#INSIDE CpG
inside_model = calculateModel(alphabet, all_dimers, CpGs_list)

#OUTSIDE CpG
outside_model = calculateModel(alphabet, all_dimers, nonCpGs_list)


#Create random sequence of 100 nts to test the two models
query = getSequence(100)

#These following alternative sequence are a known CpG island and a known NON-CpG island sequences
#They're both around 100 nucleotides
#Commeent the previous sequence variable and uncomment:
        #   - the first sequence to test the right prediction of inside model
        #   - the second sequence to test the right prediction of outside model
#query = CpGs_list[29] 
#query = chr22_seq[16415700:16415800]

print("\n1. SCORING A QUERY SEQUENCE AND IDENTIFY MOST PROBABLE MODEL")
print("   ---------------------------------------------------------")
print("\nYour query:")
print(query)

log_ratio = calculateLogRatio(query, inside_model, outside_model)

if log_ratio > 0:
    print("\nInside model is more probable")
elif log_ratio == 0:
    print("\nInside model and outside model are equally probable")
else:
    print("\nOutside model is more probable")

print("Score = ", round(log_ratio, 3))

######################################################################################################

#BONUS ASSIGNMENT: scan a long genome sequence using a sliding window

#Create random genome of 1000 nts 
genome = getSequence(1000)

#"Genome" where are present for sure CpG islands. 
#Uncomment this genome and comment the previous one to test it
#genome = chr22_seq[51221735:51222735]

#Calculate average length of a CpG island from data on chrr22

tot_length = 0
for oneCpG in CpGs_list:
    tot_length += len(oneCpG)
  
avg_len = int(tot_length/len(CpGs_list))
print("\n\n\n2. SCAN A LONG GENOME SEQUENCE USING A SLIDING WINDOW")
print("   --------------------------------------------------")
print("\nGiven your genome, we found these probable CpG islands:")

#Calculate log ratio scores for each window
start = 0
flag = 0

while start < len(genome)-avg_len+1:
    end = start+avg_len
    window = genome[start: end]
    wlog_ratio = calculateLogRatio(window, inside_model, outside_model)
    if wlog_ratio > 0:
        if flag == 0 :
            print("\nSTART\t END\t SCORE")
            flag = 1
        print(start,"\t", end, "\t", wlog_ratio)
    start += 1

if flag == 0:
    print("\n!! Apparently your genome lacks CpG island !!")