import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv("DB_CLIENT"))
        self.db     = self.client[os.getenv("DB_NAME")]

    def upsert_video(self, video_detail:dict):
        product = self.db["youtube_videos"].find_one({"videoId": video_detail["videoId"]})
        if product is None:
            self.db["youtube_videos"].insert_one(video_detail)
            return

    def upsert_dataset(self, comment_detail:dict):
        product = self.db["dataset"].find_one({"commentId": comment_detail["commentId"]})
        if product is None:
            self.db["dataset"].insert_one(comment_detail)
            return
        
    def get_labeled_dataset(self):
        query = {
            "$or":[
                {"sentiment":1}, 
                {"sentiment":2},
                {"sentiment":3}
            ]
        }

        return list(self.db["dataset"].find(query))

    def insert_instance(self, instance):
        if not self.db["instance"].find_one({"name":instance["name"]}):
            self.db["instance"].insert_one(instance)
            return
        
    def get_instance_text(self):
        all_instance = list(self.db["instance"].find({}))
        text = "("
        for i, x in enumerate(all_instance):
            text += x["name"]
            if i < len(all_instance)-1:
                text += "|"
            else:
                text += ")"
        return text
