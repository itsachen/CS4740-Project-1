def create_unigram_frequency_table(parsed_list):
    frequencyTable = {}
    wordSet = set()
    for token_list in parsed_list:
        for token in token_list:
            if(token not in wordSet):
                wordSet.add(token)
                token = 'UNK'
            if token in frequencyTable:
                frequencyTable[token] += 1
            else:
                frequencyTable[token] = 1
    return frequencyTable

def create_bigram_frequency_table(parsed_list):
    frequencyTable = {}
    wordSet = set()
    for token_list in parsed_list:
        token_list_length = len(token_list)
        for i in range(token_list_length):
            if i < token_list_length - 1:
                current_word = token_list[i]
                next_word = token_list[i+1]
                if current_word not in wordSet:
                    wordSet.add(current_word)
                    current_word = 'UNK'
                if next_word not in wordSet :
                    wordSet.add(next_word)
                    next_word = 'UNK'
                if current_word in frequencyTable:
                    if next_word in frequencyTable[current_word]:
                        frequencyTable[current_word][next_word] += 1
                    else:
                        frequencyTable[current_word][next_word] = 1
                else:
                    frequencyTable[current_word] = {next_word:1}
    return frequencyTable

def create_ngram_frequency_table(parsed_list, n):
    frequencyTable = {}
    if n == 0:
        return frequencyTable
    for token_list in parsed_list:
        # Append additional sentence start symbols
        for _ in range(n-2):
            token_list.insert(0,'<s>')
        token_list_length = len(token_list)
        for i in range(token_list_length - n + 1):
            # Create the ngram
            ngram = []
            for j in range(i,i+n):
                ngram.append(token_list[j])
            update_frequency_table(ngram, frequencyTable)
    return frequencyTable

# Recursively update the frequency table
def update_frequency_table(ngram, frequency_table):
    if len(ngram) == 1:
        if ngram[0] in frequency_table:
            frequency_table[ngram[0]] += 1
        else:
            frequency_table[ngram[0]] = 1
    else:
        if ngram[0] not in frequency_table:
            frequency_table[ngram[0]] = {}
        update_frequency_table(ngram[1:], frequency_table[ngram[0]])
                
