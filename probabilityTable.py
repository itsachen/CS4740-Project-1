def createProbabilityTable(frequencyTable):
    counter = 0.0
    probabilityTable = {}
    for token in frequencyTable:
        counter += frequencyTable[token]
    for token in frequencyTable:
        probabilityTable[token] = frequencyTable[token]/counter
    return probabilityTable 



def createCumulativeTable(probabilityTable):
    probatility = 0.0
    counter = 0
    cumulativeTable = []
    for token in probabilityTable:
        counter += 1
        if counter != len(probabilityTable):
            probatility += probabilityTable[token]
            cumulativeTable.append((token, probatility))
        else:
            cumulativeTable.append((token, 1.0))

    return cumulativeTable

frequencyTable = {'a':1, 'b':2, 'c':3, 'd':4}
probabilityTable = createProbabilityTable(frequencyTable)
cumulativeTable = createCumulativeTable(probabilityTable)
print probabilityTable
print cumulativeTable
