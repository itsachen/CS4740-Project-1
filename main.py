from Parser import *
from probabilityTable import *
from frequencyTable import *
import random
import sys

#hotel and unigram are boolean, n is the number of sentences
def write_sentences(hotel, unigram, n):
    if hotel :
        outList = parse_hotel_reviews()
    else :
        outList = parse_bible()
    if unigram :
        for i in range(n):
            cumulativeTable = createCumulativeTable(createProbabilityTable(create_unigram_frequency_table(outList)))
            #print cumulativeTable
            token = '<s>'
            s = ""
            while token != '<e>' :
                r = random.random()
                for (token, probability) in cumulativeTable :
                    if r < probability :
                        if not(token == '<e>' or token == '<s>') :
                            if s != "":
                                s+= " "
                            s += token
                        break
            print s + "\n"
    else :
        for i in range(n):
            #TODO: bigramify
            cumulativeTable = createBigramCumulativeTable(createBigramProbabilityTable(create_bigram_frequency_table(outList)))
            
            #print cumulativeTable
            token = '<s>'
            s = ""
            while token != '<e>' :
                r = random.random()
                for (token, probability) in cumulativeTable[token] :
                    if r < probability :
                        if not(token == '<e>' or token == '<s>') :
                            if s != "":
                                s+= " "
                            s += token
                        break
            print s + "\n"
            
write_sentences(sys.argv[1] == 'True', sys.argv[2] == 'True', int(sys.argv[3]))