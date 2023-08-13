import os
import sys
import numpy

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

sys.path.insert(1, os.path.abspath(os.path.join(os.getcwd())))
from lib.database import Database
from lib.youtube import Youtube
from helper import preprocessing


def run(text):
    cv      = CountVectorizer(max_features=1500)
    db      = Database()
    youtube = Youtube()

    X = []
    y = []
    i = 0
    for i, post in enumerate(db.get_labeled_dataset()):
        X.append(preprocessing.run(post["text"]))
        y.append(post["sentiment"])

    X.append(text)
    y.append(3)
    X = cv.fit_transform(X).toarray()

    # X_train, X_test, y_train, _ = train_test_split(X, y, test_size=0.25, random_state=0)

    classifier = MultinomialNB()
    classifier.fit(X[:i], y[:i])

    classes = ["negative", "neutral", "positive"]
    
    # y_pred = classifier.predict([text].reshape(1, -1))
    y_pred = classifier.predict(X[i+1:])
    print(y_pred)
    # return classes[y_pred-1]


text ="sangat bagus"
text = preprocessing.run(text)

print(run(text))