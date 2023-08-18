import os
import re
import sys
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

sys.path.insert(1, os.path.abspath(os.path.join(os.getcwd())))
from lib.database import Database

database = Database()

factory   = StemmerFactory()
stemmer   = factory.create_stemmer()


def clean_text(text):
    text = text.lower()
    text = re.sub(r"(?:((?<=[\s\W])|^)[#](\w+|[^#]|$)|((?<=[\s\W])|^)[@]([a-zA-Z0-9_]+|$))", "", text)
    text = re.sub(r"([a-zA-Z0-9])\1", "", text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r"[!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]", "", text)
    text = " ".join(text.split())
    text = stemmer.stem(text)
    return text

def tokenize(text):
    return word_tokenize(text)

def remove_stopwords(token):
    return [word for word in token if word not in database.get_instance()]

def build_text(token):
    return "".join(token)

def run(text):
    text = clean_text(text)
    token = tokenize(text)
    token = remove_stopwords(token)
    return build_text(token)
