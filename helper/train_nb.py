import os
import sys

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer


sys.path.insert(1, os.path.abspath(os.path.join(os.getcwd())))
from lib.database import Database
from lib.youtube import Youtube
from helper import preprocessing


def run(size):
    print("run naive bayes training")
    cv      = CountVectorizer(max_features=1500)
    db      = Database()

    X, y = [], []
    dataset = db.get_labeled_dataset()
    for post in dataset:
        t = preprocessing.run(post["text"])
        X.append(t)
        y.append(post["sentiment"])

    X = cv.fit_transform(X).toarray()

    classifier = MultinomialNB()
    classifier.fit(X[:len(dataset)-1], y[:len(dataset)-1])

    classes = ["negative", "neutral", "positive"]

    y_pred = classifier.predict(X[len(dataset):])
    print(y_pred)
