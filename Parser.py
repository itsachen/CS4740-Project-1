import xml.etree.ElementTree as ET
import nltk

sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

hotel_dataset = "HotelReviews/reviews.train"
bible_dataset = "bible_corpus/kjbible.train"

# TODO: Replace Windows 1252 characters for readability
def parse_all_hotel_reviews(filename=hotel_dataset):
    output_list = []

    with open(filename) as f:
        next(f) # Skip the first line that describes the columns
        for line in f:
            review_text = line[4:]
            sentences = sentence_tokenizer.tokenize(review_text)
            for sentence in sentences:
                tokenized_sentence = nltk.word_tokenize(sentence)
                tokenized_sentence.insert(0,'<s>')
                tokenized_sentence.append('<e>')
                output_list.append(tokenized_sentence)

    return output_list

def parse_hotel_reviews_for_truthfulness(filename=hotel_dataset):
    truthful_list = []
    untruthful_list = [] 

    with open(filename) as f:
        next(f) # Skip the first line that describes the columns
        for line in f:
            review_text = line[4:]
            sentences = sentence_tokenizer.tokenize(review_text)
            for sentence in sentences:
                tokenized_sentence = nltk.word_tokenize(sentence)
                tokenized_sentence.insert(0,'<s>')
                tokenized_sentence.append('<e>')
                if line[0] == 1:
                    truthful_list.append(tokenized_sentence)
                else:
                    untruthful_list.append(tokenized_sentence)

    return {"truthful": truthful_list, "untruthful": untruthful_list}

def parse_bible(filename=bible_dataset):
    output_list = []
    filetext = open(filename).read()
    root = ET.fromstring("<BIBLE>" + filetext + "</BIBLE>")

    for doc in root:
        for text in doc:
            sentences = sentence_tokenizer.tokenize(text.text) 
            for sentence in sentences:
                tokenized_sentence = nltk.word_tokenize(sentence)
                tokenized_sentence.insert(0,'<s>')
                tokenized_sentence.append('<e>')
                output_list.append(tokenized_sentence)

    return output_list
