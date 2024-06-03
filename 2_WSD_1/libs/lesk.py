import string
import random
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import google.generativeai as genai

##GEMINI SET-UP
genai.configure(api_key="AIzaSyBjFgxtyUvVOt8SXOGlX2vRCogyYfxm4Ik")
generation_config = {
  "temperature": 0.3,
  "top_p": 0.9,
  "top_k": 70
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]
model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)



lemmatizer = WordNetLemmatizer()
PUNCTUATION = string.punctuation
#STOPWORDS = set(line.strip() for line in open('data\\stop_words_FULL.txt'))
STOPWORDS = set(stopwords.words('english'))


def lesk_algorithm(word, sentence):
    best_sense = wn.synsets(word)[0]
    max_overlap = 0
    context = cleaning(sentence)
    for sense in wn.synsets(word):
        #signature = get_signature(sense)
        signature = get_signature(sense)
        overlap = get_overlap(signature, context) 
        if overlap>max_overlap:
            max_overlap=overlap
            best_sense=sense
    return best_sense


# clean the sentence from punctuation and stopwords
def cleaning(sentence):
    sentence = sentence.lower()
    for p in PUNCTUATION:
        sentence = sentence.replace(p, ' ')
    sentence = sentence.split()
    sentence=[i for i in sentence if i not in STOPWORDS]
    lemmatized_sentece=[lemmatizer.lemmatize(i) for i in sentence]
    #lemmatizazione
    return lemmatized_sentece


#get all the set of words in the gloss and examples of sense
def get_signature(sense):
     return cleaning(sense.definition())

#counting the number of shared words
def get_overlap(signature,context):
 sig=set(signature)
 con=set(context)
 intersection = con.intersection(sig)
 return len(intersection)

def gemini_get_signature(word, sense):
  prompt_parts = ["Can you write some examples which contains the word ", word," defined as ", sense.definition()]
  response = model.generate_content(prompt_parts)
  text_response=''
  for candidate in response.candidates:
            text_response= ' '.join([part.text for part in candidate.content.parts])
  print(text_response)
  print('----------------')
  return text_response
  




def gemini_lesk_algorithm(word, sentence):
    best_sense = wn.synsets(word)[0]
    max_overlap = 0
    context = cleaning(sentence)
    for sense in wn.synsets(word):
        print("passo")
        signature = gemini_get_signature(word,sense)
        overlap = get_overlap(signature, context) 
        if overlap>max_overlap:
            max_overlap=overlap
            best_sense=sense
    return best_sense


