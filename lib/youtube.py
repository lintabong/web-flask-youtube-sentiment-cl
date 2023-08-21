import os
from datetime import datetime

import yt_dlp as youtube_dl
from itertools import islice
from youtubesearchpython import *
from youtube_comment_downloader import *
from dotenv import load_dotenv

load_dotenv()


class Youtube():
    def __init__(self):
        self.url = os.getenv("YOUTUBE_URL")

    def list_video(self, keyword, limit:int=20):
        videos = CustomSearch(keyword, VideoSortOrder.uploadDate, limit=limit)

        return [x["id"] for x in videos.result()["result"]]

    @staticmethod
    def get_detail(url):
        return Video.get(url, mode=ResultMode.json, get_upload_date=True)
    
    @staticmethod
    def get_detail_dl(url):
        with youtube_dl.YoutubeDL({}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info

    @staticmethod
    def get_comments_only(url, total:int=1000):
        downloader = YoutubeCommentDownloader()
        comments   = downloader.get_comments_from_url(url, sort_by=SORT_BY_POPULAR)

        return [x for x in islice(comments, total)]
    
    def get_comments(self, video_id:str):
        url       = self.url + video_id
        detail    = self.get_detail(url)
        detail_dl = self.get_detail_dl(url)
        comments  = self.get_comments_only(url)

        formated_comments = []
        for comment in comments:
            formated_comments.append({
                "commentId": comment["cid"],
                "text": comment["text"],
                "author": {
                    "name": comment["author"],
                    "avatar": comment["photo"],
                },
                "createdAt": datetime.fromtimestamp(int(comment["time_parsed"]))
            })

        result = {
            "videoId": detail["id"],
            "title": detail["title"],
            "viewCount": detail["viewCount"]["text"],
            "channel": detail["channel"],
            "thumbnail": detail_dl["thumbnail"],
            "createdAt": datetime.strptime(detail["uploadDate"], "%Y-%m-%d"),
            "crawledAt": datetime.utcnow().replace(microsecond=0),
            "description": detail["description"],
            "comments": formated_comments
        }

        return result
