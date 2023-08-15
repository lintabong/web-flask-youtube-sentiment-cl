import os
from threading import Thread
from flask import Flask, request, render_template
from dotenv import load_dotenv

from helper import predict
from lib.database import Database

database = Database()

load_dotenv()


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        video_id = request.form.get("fname")

        p = Thread(target=predict.run, args=(video_id,))
        p.start()

        render_template("index.html")
    return render_template("index.html")

@app.route("/list_video", methods=["GET", "POST"])
def list_video():
    if request.method == "POST":
        return render_template("list_video.html", all_video=all_video)
    
    all_video = [[y["videoId"], y["title"], len(y["comments"]), y["thumbnail"]] for y in database.get_all_video()]

    return render_template("list_video.html", all_video=all_video)

@app.route("/result/<video_id>")
def result(video_id):
    video_detail = database.get_video(video_id)

    if video_detail is not None:
        pos = 0
        neg = 0
        neu = 0

        for comment in video_detail["comments"]:
            if comment["sentiment"] == "negative":
                neg+=1
            if comment["sentiment"] == "neutral":
                neu+=1
            if comment["sentiment"] == "positive":
                pos+=1
        
        description = str(video_detail["description"][:200]) + " . . . " if len(video_detail["description"]) > 200 else video_detail["description"]
        return render_template("result.html", 
                               video_detail=video_detail, 
                               video_comments=video_detail["comments"],
                               image_url=video_detail["thumbnail"],
                               description=description,
                               negative=neg,
                               neutral=neu,
                               positive=pos)
    
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)