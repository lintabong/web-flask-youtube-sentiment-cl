from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from threading import Thread

from helper import formatter
from helper import predict
from helper import crawl_dataset
from helper import train_nb
from helper import train_svm
from lib.database import Database

database = Database()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_id = request.form.get("fname")

        p = Thread(target=predict.run, args=(video_id))
        p.start()

    return render_template("index.html")


@app.route("/list_video")
def list_video():
    return render_template("list_video.html", 
                           all_video=database.get_all_video())


@app.route("/result/<video_id>")
def result(video_id):
    video_detail = database.get_video(video_id)

    if video_detail is None:
        return redirect(url_for("list_video"))
    
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
    args   = request.args
    offset = int(args["offset"]) if "offset" in args else 0

    comments      = database.get_dataset((offset-1))
    max_page      = database.get_max_dataset_page()
    neg, neu, pos = database.count_labeled_dataset()
    result        = database.get_result_model()

    pagination = formatter.pagination(offset, max_page)

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
                            positive=pos,
                            result=result)


@app.route("/labeling")
def labeling():    
    args = request.args
    database.update_dataset(args["commentId"], int(args["label"]))
    return redirect(url_for("dataset", offset=args["current"]))


@app.route("/train_nb", methods=["GET", "POST"])
def trainnb():
    if request.method == "POST":
        test_data = request.form.get("percentage-test-data")
        try:
            p = Thread(target=train_nb.run, args=(int(test_data),))
            p.start()

        except Exception as error:
            print(error)

    return redirect(url_for("dataset", offset=1))

@app.route("/train_svm", methods=["GET", "POST"])
def trainsvm():
    if request.method == "POST":
        test_data = request.form.get("percentage-test-data")
        try:
            p = Thread(target=train_svm.run, args=(int(test_data),))
            p.start()

        except Exception as error:
            print(error)

    return redirect(url_for("dataset", offset=1))


if __name__ == "__main__":
    app.run(debug=True)
