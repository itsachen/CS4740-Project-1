from Parser import *
from probabilityTable import *
from frequencyTable import *
import random
outList = parse_hotel_reviews()
cumulativeTable = createCumulativeTable(createProbabilityTable(create_frequency_table(outList)))
#print cumulativeTable
token = '<s>'
while token != '<e>' :
    r = random.random()
    for (token, probability) in cumulativeTable :
        if r < probability :
            if token != '<e>' :
                print token
            break