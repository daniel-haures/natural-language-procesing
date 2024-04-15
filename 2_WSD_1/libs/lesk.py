import string
import random
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


PUNCTUATION = string.punctuation
STOPWORDS = set(line.strip() for line in open('data\\stop_words_FULL.txt'))


def lesk_algorithm(word, sentence):
    best_sense = wn.synsets(word)[0]
    max_overlap = 0
    context = cleaning(sentence)
    #print(context)
    for sense in wn.synsets(word):
        signature = get_signature(sense)
        #print(signature)
        overlap = get_overlap(signature, context) 
        if overlap>max_overlap:
            max_overlap=overlap
            best_sense=sense
    return best_sense


# clean the sentence from punctuation and stopwords
#eliminare i nomi propri
def cleaning(sentence):
    sentence = sentence.lower()
    for p in PUNCTUATION:
        sentence = sentence.replace(p, ' ')
    sentence = sentence.split()
    sentence=[i for i in sentence if i not in STOPWORDS]
    lemmatized_sentece=[lemmatizer.lemmatize(i) for i in sentence]
    #lemmatizazione
    return sentence


#get all the set of words in the gloss and examples of sense
def get_signature(sense):
     return cleaning(sense.definition())

#counting the number of shared words
def get_overlap(signature,context):
 sig=set(signature)
 con=set(context)
 intersection = con.intersection(sig)
 return len(intersection)


#print(cleaning("foxes and Juliet I'm hoping to go jogging I haven't eaten in a while where is everybody going"))
#print(lesk_algorithm("bed","love to bed"))