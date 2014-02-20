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


def createBigramProbabilityTable(bigramFrequencyTable):
    bigramProbabilityTable = {}
    for token in bigramFrequencyTable:
        bigramProbabilityTable[token] = createProbabilityTable(bigramFrequencyTable[token])
    return bigramProbabilityTable


def createBigramCumulativeTable(bigramProbabilityTable):
    bigramCumulativeTable = {}
    for token in bigramProbabilityTable:
        bigramCumulativeTable[token] = createCumulativeTable(bigramProbabilityTable[token])
    return bigramCumulativeTable


