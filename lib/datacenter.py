import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv("DC_CLIENT"))
        self.dc     = self.client[os.getenv("DC_NAME")]

    def upsert_video(self, video_detail:dict):
        product = self.dc["youtube_videos"].find_one({"videoId": video_detail["videoId"]})
        if product is None:
            self.dc["youtube_videos"].insert_one(video_detail)
            return
        
    def upsert_datacenter(self, video_detail:dict):
        product = self.dc["youtube_video_raw"].find_one({"videoId": video_detail["videoId"]})
        if product is None:
            self.dc["youtube_video_raw"].insert_one(video_detail)
            return