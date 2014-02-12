import re
import nltk.data

sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
dataset = 'HotelReviews/reviews.train'

output_list = []

with open(dataset) as f:
    next(f) # Skip the first line
    for line in f:
        review_text = line[4:]
        sentences = sentence_tokenizer.tokenize(review_text)
        for sentence in sentences:
            tokenized_sentence = nltk.word_tokenize(sentence)
            tokenized_sentence.insert(0, '<s>')
            tokenized_sentence.append('<e>')
            output_list.append(tokenized_sentence)
