import os
import re
import sys

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

sys.path.insert(1, os.path.abspath(os.path.join(os.getcwd())))
from lib.database import Database
from lib.youtube import Youtube
from helper import preprocessing


def run(video_id):
    print(f'run scrape {video_id}')
    cv      = CountVectorizer(max_features=1500)
    db      = Database()
    youtube = Youtube()

    result   = youtube.get_comments(video_id)
    instance = db.get_instance_text()

    X, y = [], []
    dataset = db.get_labeled_dataset()
    for post in dataset:
        t = preprocessing.run(post["text"])
        t = re.sub(instance, "", t)
        X.append(t)
        y.append(post["sentiment"])

    for comment in result["comments"]:
        t = preprocessing.run(comment["text"])
        t = re.sub(instance, "", t)
        X.append(t)

    X = cv.fit_transform(X).toarray()

    classifier = MultinomialNB()
    classifier.fit(X[:len(dataset)-1], y[:len(dataset)-1])

    classes = ["negative", "neutral", "positive"]

    y_pred = classifier.predict(X[len(dataset):])

    for i in range(len(y_pred)):
        result["comments"][i]["sentiment"] = classes[(y_pred[i]-1)]

    db.upsert_video(result)
