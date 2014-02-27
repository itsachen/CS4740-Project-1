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
    frequencyTable, wordSet = create_ngram_frequency_table(outList, 2, True)
    frequencyTable, prob = smooth_bigram_frequency_table(frequencyTable, wordSet)
    probabilityTable = normalize_bigram_probability_table(createBigramProbabilityTable(frequencyTable), prob, wordSet)
    return probabilityTable, prob, wordSet
    
def normalize_bigram_probability_table(probabilityTable, prob, wordSet):
    for token in probabilityTable :
        totalProb = prob
        for token2 in probabilityTable[token] :
            totalProb += probabilityTable[token][token2]
        for token2 in probabilityTable[token] :
            probabilityTable[token][token2] /= totalProb
    return probabilityTable
    
def predict_sentence_list():
    output_list = []
    train_sentence_list = parse_hotel_reviews_for_truthfulness()
    test_sentence_list = parse_kaggle_hotel_reviews("HotelReviews/kaggle_data_file.txt")

    truthful_bigram, probUnkTruthful, wordSetTruthful = create_smoothed_bigram_probability_table(train_sentence_list["truthful"])
    untruthful_bigram, probUnkUntruthful, wordSetUntruthful = create_smoothed_bigram_probability_table(train_sentence_list["untruthful"])
    counter = 0

    for review in test_sentence_list:
        truthfulPerplexity = 1.0
        untruthfulPerplexity = 1.0
        for tokenList in review:
            
            truthfulPerplexity *= bigram_perplexity(truthful_bigram, probUnkTruthful, tokenList)
            untruthfulPerplexity *= bigram_perplexity(untruthful_bigram, probUnkUntruthful, tokenList)
            
        if truthfulPerplexity < untruthfulPerplexity :
            output_list.append(str(counter) + ",1")
        else:
            output_list.append(str(counter) + ",0")      
        counter += 1     
    return output_list
    
def bigram_perplexity(probabilityTable, unkProbability, outList):
    perplexity = 1.0
    length = 0
    for token_list in outList :
        token_list_length = len(token_list)
        length += token_list_length
    for token_list in outList :
        token_list_length = len(token_list)
        for i in range(token_list_length):
            if i < token_list_length - 1:
                current_word = token_list[i]
                next_word = token_list[i+1]
                prob = 1.0
                if current_word in probabilityTable and next_word in probabilityTable[current_word] :
                    prob = probabilityTable[current_word][next_word]
                elif '<UNK>' in probabilityTable and next_word in probabilityTable['<UNK>']:
                    prob = probabilityTable['<UNK>'][next_word]
                elif '<UNK>' in probabilityTable and '<UNK>' in probabilityTable['<UNK>']:
                    prob = probabilityTable['<UNK>']['<UNK>']
                else :
                    prob = unkProbability
                perplexity = perplexity * pow(1.0 / prob, 1.0 / length)
    return perplexity



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
                previous_tokenT = '<UNK>'
                if previous_tokenT in truthful_bigram and tokenT in truthful_bigram[previous_tokenT]:
                    probability_truthful = probability_truthful * truthful_bigram[previous_tokenT][tokenT]
                else :
                    tokenT = '<UNK>'
                    if previous_tokenT in truthful_bigram and tokenT in truthful_bigram[previous_tokenT]:
                        probability_truthful = probability_truthful * truthful_bigram[previous_tokenT][tokenT]
                    else: 
                        probability_truthful = probability_truthful * probUnkTruthful/ len(truthfulWordList)

            if previous_tokenUT in untruthful_bigram and tokenUT in untruthful_bigram[previous_tokenUT]:
                probability_untruthful = probability_untruthful * untruthful_bigram[previous_tokenUT][tokenUT]
            else :
                previous_tokenUT = '<UNK>'
                if previous_tokenUT in untruthful_bigram and tokenUT in untruthful_bigram[previous_tokenUT]:
                    probability_untruthful = probability_untruthful * untruthful_bigram[previous_tokenUT][tokenUT]
                else :
                    tokenUT = '<UNK>'
                    if previous_tokenUT in untruthful_bigram and tokenUT in untruthful_bigram[previous_tokenUT]:
                        probability_untruthful = probability_untruthful * untruthful_bigram[previous_tokenUT][tokenUT]
                    else: 
                        probability_untruthful = probability_untruthful * probUnkUntruthful/ len(untruthfulWordList)

            previous_token = token
    return [probability_truthful, probability_untruthful]

def writeToFile(filename, lst):
    file_object = open(filename, 'w+')
    file_object.write('Id,Label\n')
    for line in lst:
        file_object.write(line + '\n')
    file_object.close()

    
def test_perplexity():
    probabilityTable, prob, wordList = create_smoothed_bigram_probability_table(parse_all_hotel_reviews())
    print bigram_perplexity(probabilityTable, prob, parse_all_hotel_reviews("HotelReviews/reviews.test"))
    
test_perplexity()
#predict_sentence_list()
#print create_ngram_frequency_table(parse_all_hotel_reviews(), 1, True)
#print get_ngram_counts(create_ngram_frequency_table(parse_all_hotel_reviews(), 2, True), {}, 0, 2)
#predictions = predict_sentence_list()
#writeToFile("predictions.out", predictions)
