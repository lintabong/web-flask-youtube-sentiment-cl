import os
import sys

sys.path.insert(1, os.path.abspath(os.path.join(os.getcwd())))
from lib.youtube import Youtube
from lib.database import Database

youtube  = Youtube()
database = Database()

def run(video_id):
    print("start crawl", video_id)

    result = youtube.get_comments(video_id)
    result["totalComments"] = len(result["comments"])

    database.upsert_video(result)

    for comment in result["comments"]:
        comment.update({
            "videoId": result["videoId"],
            "title": result["title"],
            "sentiment": 0
        })

        database.upsert_dataset(comment)