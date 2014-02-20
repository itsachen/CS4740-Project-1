def create_unigram_frequency_table(parsed_list):
    frequencyTable = {}
    for token_list in parsed_list:
        for token in token_list:
            if token in frequencyTable:
                frequencyTable[token] += 1
            else:
                frequencyTable[token] = 1
    return frequencyTable

def create_bigram_frequency_table(parsed_list):
    frequencyTable = {}
    for token_list in parsed_list:
        token_list_length = len(token_list)
        for i in range(token_list_length):
            if i < token_list_length - 1:
                current_word = token_list[i]
                next_word = token_list[i+1]
                if current_word in frequencyTable:
                    if next_word in frequencyTable[current_word]:
                        frequencyTable[current_word][next_word] += 1
                    else:
                        frequencyTable[current_word][next_word] = 1
                else:
                    frequencyTable[current_word] = {next_word:1}
    return frequencyTable

