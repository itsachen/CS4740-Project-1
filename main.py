from Parser import *
from probabilityTable import *
from frequencyTable import *
import random
import sys

#hotel and unigram are boolean, n is the number of sentences
def write_sentences(hotel, unigram, n):
    if hotel :
        outList = parse_all_hotel_reviews()
    else :
        outList = parse_bible()
    if unigram :
        for i in range(n):
            cumulativeTable = createCumulativeTable(createProbabilityTable(create_unigram_frequency_table(outList, False)))
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
            frequencyTable, wordSet = create_bigram_frequency_table(outList, False)
            cumulativeTable = createBigramCumulativeTable(createBigramProbabilityTable(frequencyTable))

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
#arg1 = hotel, arg2 = unigram, arg3 = number of sentences      
#write_sentences(sys.argv[1] == 'True', sys.argv[2] == 'True', int(sys.argv[3]))

def create_smoothed_bigram_probability_table(outList):
    frequencyTable, wordSet = create_bigram_frequency_table(outList, True)
    frequencyTable, prob = smooth_bigram_frequency_table(frequencyTable)
    probabilityTable = createBigramProbabilityTable(frequencyTable)
    return probabilityTable, prob, wordSet

def predict_sentence_list():
    output_list = []
    train_sentence_list = parse_hotel_reviews_for_truthfulness()
    test_sentence_list = parse_kaggle_hotel_reviews("HotelReviews/kaggle_data_file.txt")

    truthful_bigram, probUnkTruthful, wordSetTruthful = create_smoothed_bigram_probability_table(train_sentence_list["truthful"])
    untruthful_bigram, probUnkUntruthful, wordSetUntruthful = create_smoothed_bigram_probability_table(train_sentence_list["untruthful"])
    counter = 0

    for review in test_sentence_list:
        probability_truthful = 0.0
        probability_untruthful = 0.0
        for tokenList in review:
            truthful_tuple = isTruthful(tokenList, truthful_bigram, untruthful_bigram, probUnkTruthful, probUnkUntruthful, wordSetTruthful, wordSetUntruthful)
            probability_truthful = probability_truthful + truthful_tuple[0]
            probability_untruthful = probability_untruthful + truthful_tuple[1]
        if probability_truthful >= probability_untruthful:
                output_list.append(str(counter) + ",1")
        else:
            output_list.append(str(counter) + ",0")      
        counter += 1     
    return output_list


def isTruthful(tokenList, truthful_bigram, untruthful_bigram, probUnkTruthful, probUnkUntruthful, truthfulWordList, untruthfulWordList):
    probability_truthful = 1.0
    probability_untruthful = 1.0
    previous_token = None
    for token in tokenList:
        if previous_token is None:
            previous_token = token
        else:
            tokenT = token
            previous_tokenT = previous_token
            tokenUT = token
            previous_tokenUT = previous_token
            
            if token not in truthfulWordList:
                tokenT = '<UNK>'
            if previous_token not in truthfulWordList:
                previous_tokenT = '<UNK>'
            if token not in untruthfulWordList:
                tokenUT = '<UNK>'
            if previous_token not in untruthfulWordList:
                previous_tokenUT = '<UNK>'
            
            
            if previous_tokenT in truthful_bigram and tokenT in truthful_bigram[previous_tokenT]:
                probability_truthful = probability_truthful * truthful_bigram[previous_tokenT][tokenT]
            else :
                probability_truthful = probability_truthful * probUnkTruthful
            if previous_tokenUT in untruthful_bigram and tokenUT in untruthful_bigram[previous_tokenUT]:
                probability_untruthful = probability_untruthful * untruthful_bigram[previous_tokenUT][tokenUT]
            else:
                probability_truthful = probability_truthful * probUnkUntruthful
            previous_token = token
    return [probability_truthful, probability_untruthful]

def writeToFile(filename, lst):
    file_object = open(filename, 'w+')
    file_object.write('Id,Label\n')
    for line in lst:
        file_object.write(line + '\n')
    file_object.close()

#predict_sentence_list()
predictions = predict_sentence_list()
writeToFile("predictions.out", predictions)
