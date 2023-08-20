import os
import sys
from datetime import datetime

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

sys.path.insert(1, os.path.abspath(os.path.join(os.getcwd())))
from lib.database import Database
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

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size/100, random_state=0)

    classifier = MultinomialNB()
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    print(report)

    result = {
        "trained": datetime.utcnow(),
        "testSize": size,
        "accuracy": report["accuracy"],
        "precission": report["macro avg"]["precision"],
        "recall": report["macro avg"]["recall"],
        "confussionMatrix": []
    }

    for i in ["1", "2", "3"]:
        if i in report:
            result["confussionMatrix"].append({
                "class": i,
                "result": report[i]
            })

    db.upsert_result(nb=result, svm=None, test_size=size)
