def create_unigram_frequency_table(parsed_list, unk):
    frequencyTable = {}
    wordSet = set()
    for token_list in parsed_list:
        for token in token_list:
            if unk and token not in wordSet:
                wordSet.add(token)
                token = 'UNK'
            if token in frequencyTable:
                frequencyTable[token] += 1
            else:
                frequencyTable[token] = 1
    return frequencyTable

def create_bigram_frequency_table(parsed_list, unk):
    frequencyTable = {}
    wordSet = set()
    unigramFreqTable = {}
    if unk :
        unigramFreqTable = create_unigram_frequency_table(parsed_list, False)
        for token in unigramFreqTable :
            if unigramFreqTable[token] == 1 :
                wordSet.add(token)
    
    for token_list in parsed_list:
        token_list_length = len(token_list)
        for i in range(token_list_length):
            if i < token_list_length - 1:
                current_word = token_list[i]
                next_word = token_list[i+1]
                if unk and current_word in wordSet:
                    current_word = 'UNK'
                if unk and next_word in wordSet :
                    next_word = 'UNK'
                if current_word in frequencyTable:
                    if next_word in frequencyTable[current_word]:
                        frequencyTable[current_word][next_word] += 1
                    else:
                        frequencyTable[current_word][next_word] = 1
                else:
                    frequencyTable[current_word] = {next_word:1}
    return frequencyTable, wordSet

#Returns the new frequency table and an "unknown" probability
def smooth_bigram_frequency_table(frequencyTable):
    counts = {}
    totalBigrams = 0
    #Get counts for N1, N2, etc.
    for token in frequencyTable :
        for token2 in frequencyTable[token] :
            freq = frequencyTable[token][token2]
            if frequencyTable[token][token2] in counts :
                counts[freq] += 1
                totalBigrams += 1
            else :
                counts[freq] = 1
                totalBigrams += 1
    #Determine what frequency counts to smooth
    i = 1
    while i in counts :
        maxCount = i-1
        i += 1
    
    #Smooth frequencies
    for token in frequencyTable :
        for token2 in frequencyTable[token] :
            freq = frequencyTable[token][token2]
            if freq < maxCount :
                frequencyTable[token][token2] = float(freq + 1) * counts[freq + 1] / counts[freq]
    return frequencyTable, float(counts[1]) / totalBigrams