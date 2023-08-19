import os
import sys

from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(1, os.path.abspath(os.path.join(os.getcwd())))
from lib.database import Database
from helper import preprocessing


def run(size):
    db = Database()

    posts = db.get_labeled_dataset()
    print(len(posts))

    X = []
    y = []

    for post in posts:
        post["text"] = preprocessing.run(post["text"])

        X.append(post["text"])
        y.append(post["sentiment"])


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size/100, random_state=0)

    vectorizer = TfidfVectorizer(min_df=5, max_df=0.8, sublinear_tf=True, use_idf=True)

    train_vectors = vectorizer.fit_transform(X_train)
    test_vectors = vectorizer.transform(X_test)

    svm_classifier = svm.SVC(kernel='linear')
    svm_classifier.fit(train_vectors, y_train)

    y_pred = svm_classifier.predict(test_vectors)

    print(y_pred)

    report = classification_report(y_test, y_pred, output_dict=True)
    print(report)
