import os
import math
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv("DB_CLIENT"))
        self.db     = self.client[os.getenv("DB_NAME")]

        self.limit = int(os.getenv("LIMIT_OFFSET_DATASET"))
        self.instances_person = ["ahy", "rocky", "gerung", "jokowi", "abud", 
                                 "anies", "moeldoko", "sandiaga", "rokki", "garong",
                                 "khofifah", "yenni", "moeldoko", "roki", "widodo",
                                 "pranowo", "ganjar", "prabowo", "denny", "siregar",
                                 "mahfud", "mahfudmd", "ahok", "puan", "maharani",
                                 "megawati", "andika"]
        
        self.instances_organization = ["pdi", "bmkg", "pdip", "golkar", "pks", "gerindra",
                                      "nasdem", "pkb", "partai buruh", "psi"]
        
        self.instances_nation = ["indo", "indonesia", "indonesian", "inggris", "amerika",
                                 "china", "malaysia", "arab"]

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

        return list(self.db["dataset2"].find(query))

    def get_dataset(self, offset=0):
        return list(self.db["dataset"].find({}).limit(self.limit).skip(int(offset)*self.limit))
    
    def get_max_dataset_page(self):
        end = self.db["dataset"].count_documents({})
        return math.floor(end/self.limit) + 1 if end%self.limit > 0 else math.floor(end/self.limit)

    def count_labeled_dataset(self):
        negative = self.db["dataset"].count_documents({"sentiment": 1})
        neutral  = self.db["dataset"].count_documents({"sentiment": 2})
        positive = self.db["dataset"].count_documents({"sentiment": 3})
        return negative, neutral, positive

    def update_dataset(self, comment_id, sentiment):
        self.db["dataset"].update_one({"commentId": comment_id}, {"$set": {"sentiment": sentiment}})

    def get_all_video(self):
        return list(self.db["youtube_videos"].find())

    def get_video(self, video_id):
        return self.db["youtube_videos"].find_one({"videoId":video_id})

    def init_instance(self):
        if self.db["instance"].find_one({}) is None:
            for instance in self.instances_person:
                self.db["instance"].insert_one({"name": instance, "type": "person"})

            for instance in self.instances_nation:
                self.db["instance"].insert_one({"name": instance, "type": "nation"})

            for instance in self.instances_organization:
                self.db["instance"].insert_one({"name": instance, "type": "organization"})

    def insert_instance(self, instance):
        if not self.db["instance"].find_one({"name":instance["name"]}):
            self.db["instance"].insert_one(instance)
            return

    def get_instance(self):
        return list(self.db["instance"].find({}))

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

    def upsert_result(self, nb=None, svm=None, test_size=10):
        if self.db["result"].find_one({"result": 1}) is not None:
            if svm is not None:
                self.db["result"].update_one({"result": 1}, {"$set": {"svm": svm, "testSize": test_size}})
            if nb is not None:
                self.db["result"].update_one({"result": 1}, {"$set": {"nb": nb, "testSize": test_size}})
            
            return

        if svm is not None:
            self.db["result"].insert_one({
                "result": 1,
                "testSize": test_size,
                "svm": svm
            })

        if nb is not None:
            self.db["result"].insert_one({
                "result": 1,
                "testSize": test_size,
                "nb": nb,
            })

    def get_result_model(self):
        result = self.db["result"].find_one({"result": 1})

        if result is None:
            result = {
                "nb": {
                    "accuracy": 0,
                    "precission": 0,
                    "recall": 0
                },
                "svm": {
                    "accuracy": 0,
                    "precission": 0,
                    "recall": 0
                }
            }

        if "svm" not in result:
            result["svm"] = {
               "accuracy": 0,
                "precission": 0,
                "recall": 0 
            }
        
        if "nb" not in result:
            result["nb"] = {
               "accuracy": 0,
                "precission": 0,
                "recall": 0 
            }

        return result