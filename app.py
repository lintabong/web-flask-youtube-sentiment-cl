import math
from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from threading import Thread

from helper import formatter
from helper import predict
from helper import crawl_dataset
from lib.database import Database

database = Database()


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        video_id = request.form.get("fname")

        p = Thread(target=predict.run, args=(video_id,))
        p.start()

        render_template("index.html")
    return render_template("index.html")


@app.route("/list_video")
def list_video():
    return render_template("list_video.html", all_video=database.get_all_video())


@app.route("/result/<video_id>")
def result(video_id):
    video_detail = database.get_video(video_id)

    if video_detail is None:
        return redirect(url_for("result"))
    
    neg, neu, pos = database.count_labeled_dataset()

    if len(video_detail["description"]) >= 200:
        description = f'{video_detail["description"][:200]}... '
    else:
        description = video_detail["description"]

    return render_template("result.html", 
                            video_detail=video_detail, 
                            video_comments=video_detail["comments"],
                            image_url=video_detail["thumbnail"],
                            description=description,
                            negative=neg,
                            neutral=neu,
                            positive=pos)


@app.route("/dataset", methods=["GET", "POST"])
def dataset():
    args     = request.args
    offset   = int(args["offset"]) if "offset" in args else 0

    comments = database.get_dataset((offset-1))
    end      = database.get_max_dataset_page()

    pagination = formatter.pagination(offset, end)

    neg, neu, pos = database.count_labeled_dataset()

    if request.method == "POST":
        video_id = request.form.get("fname")

        p = Thread(target=crawl_dataset.run, args=(video_id,))
        p.start()
        
    return render_template("dataset.html", 
                            comments=comments, 
                            offset=offset, 
                            pagination=pagination,
                            negative=neg,
                            neutral=neu,
                            positive=pos)


@app.route("/labeling")
def labeling():    
    args = request.args
    database.update_dataset(args["commentId"], int(args["label"]))
    return redirect(url_for("dataset", offset=args["current"]))


if __name__ == "__main__":
    app.run(debug=True)
