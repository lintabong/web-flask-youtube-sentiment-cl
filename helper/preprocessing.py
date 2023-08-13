import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()
listStopword =  set(stopwords.words('indonesian'))


def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r"[!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]", "", text)
    text = " ".join(text.split())
    text = stemmer.stem(text)
    return text

def tokenize(text):
    token = word_tokenize(text)
    return token

def remove_stopwords(token):
    removed = []
    for t in token:
        if t not in listStopword:
            removed.append(t)

    return removed

def build_text(token):
    return ''.join(token)

def run(text):
    text = clean_text(text)
    token = tokenize(text)
    token = remove_stopwords(token)
    return build_text(token)