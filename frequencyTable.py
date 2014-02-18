def create_frequency_table(parsed_list):
    frequencyTable = {}
    for token_list in parsed_list:
        for token in token_list:
            if token in frequencyTable:
                frequencyTable[token] += 1
            else:
                frequencyTable[token] = 1
    print(frequencyTable['<e>'])
    return frequencyTable
