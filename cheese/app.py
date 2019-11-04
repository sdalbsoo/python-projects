import os

from werkzeug import secure_filename
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import g
from flask import abort
import yaml
import pymysql

from cheese import SrtParser


UPLOAD_FOLDER = "../cheese/files"
ALLOWED_EXTENSIONS = set(["srt", "smi"])


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("./contact.html")


@app.route("/subtitle")
def subtitle_dictionary():
    subtitle_path = request.args.get("path", None)
    word_meanings = None
    if subtitle_path is not None:
        with app.app_context():
            con_db = get_db()
            srt = SrtParser(subtitle_path, con_db)
            sentences = srt.extract_sentences()
            extracted_words = srt.extract_words(sentences)
            word_meanings = srt.dict_parser.search_dict(extracted_words, con_db)  # noqa
    return render_template(
        "subtitle.html",
        path=subtitle_path,
        word_meanings=word_meanings,
    )


@app.route("/upload_file", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            return redirect(url_for("subtitle_dictionary", path=path))
        else:
            return page_not_found("unuseful file!")
    else:
        return page_not_found("request method error!")


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error("page not found: %s", (e))
    return render_template("404.html"), 404


def get_db():
    db = getattr(g, '_database', None)
    print("connect db!")
    with open("./config.yml", "r") as f:
        data_map = yaml.load(f)
        host = data_map["database"]["host"]
        user = data_map["database"]["user"]
        pw = data_map["database"]["password"]
    if db is None:
        db = g._database = pymysql.connect(
            host=host, user=user, password=pw
        )
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        print("db close")
        db.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
