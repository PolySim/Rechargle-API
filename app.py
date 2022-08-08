import flask
from flask_cors import CORS 
import os
import sys
from flask import Flask, request, send_file, render_template
import json
from datetime import datetime, timedelta
from pytz import timezone
import pytz
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Relative path setup
cur_path = os.path.abspath(".")
sys.path.append(cur_path)

# Setup paths to the metadata and images directories
META_IMGS_PATH = os.path.abspath("./metadata")
IMGS_PATH = os.path.abspath("./images")

@app.route('/')
def index():
    return "<h1>Hello World</h1>"

@app.route('/hello')
def say_hello_world():
    return flask.jsonify({'result': "Hello Connected React World!!!"})


@app.route('/api/info')
def get_information():
    try:
        meta_files = os.listdir(META_IMGS_PATH)
        for meta_file in meta_files:
            if meta_file == "info.json":
                meta_fpath = os.path.join(META_IMGS_PATH, meta_file)
                with open(meta_fpath, 'r') as meta_file:
                    meta_data = json.load(meta_file)
                    return flask.jsonify(meta_data)
    except Exception as e:
        print(f"Failed with message: {str(e)}")
        response = flask.make_response(
            "Dataset screen display unsuccessful...", 403)
        return response


@app.route('/api/images')
def get_images():
    try:
        args = request.args.to_dict()
        numero = args['num']
        meta_files = os.listdir(META_IMGS_PATH)
        for meta_file in meta_files:
            if meta_file == str(numero) + ".json":
                meta_fpath = os.path.join(META_IMGS_PATH, meta_file)
                with open(meta_fpath, 'r') as meta_file:
                    meta_data = json.load(meta_file)
                    return flask.jsonify(meta_data)
        response = flask.make_response(
            "Dataset screen display unsuccessful...", 403)
        return response
    except Exception as e:
        print(f"Failed with message: {str(e)}")
        response = flask.make_response(
            "Dataset screen display unsuccessful...", 403)
        return response


@app.route('/api/image1/<num>', methods=['GET'])
def load_image1(num):
    meta_path = os.path.join(META_IMGS_PATH, num+".json")
    with open(meta_path, 'r') as meta_file:
        meta_data = json.load(meta_file)
    fpath = os.path.join(IMGS_PATH, str(num) + '/' + meta_data["img1"])
    return "<h1>OK</h1>"

    return send_file(fpath)


@app.route('/api/image2/<num>', methods=['GET'])
def load_image2(num):
    meta_path = os.path.join(META_IMGS_PATH, num+".json")
    with open(meta_path, 'r') as meta_file:
        meta_data = json.load(meta_file)
    fpath = os.path.join(IMGS_PATH, str(num) + '/' + meta_data["img2"])
    if not os.path.isfile(fpath) or not os.path.exists(fpath):
        raise ValueError(f"No file found: {fpath}")

    return send_file(fpath)


@app.route("/api/update", methods=["PUT"])
def update_info():
    try:
        values = request.json
        paris_day = datetime.now(pytz.timezone('Europe/Paris')).day
        if str(paris_day) != values["jour"]:
            values = {"jour" : str(paris_day), "win" : "0", "lose" : "0", "numero" : str(int(values["numero"]))}
            # values = {"jour" : str(paris_day), "win" : "0", "lose" : "0", "numero" : str(int(values["numero"]) + 1)}
        meta_fpath = os.path.join(META_IMGS_PATH, "info.json")
        with open(meta_fpath, 'w') as meta_filee:
            json.dump(values, meta_filee)

        response = flask.jsonify({"success": True})
    except Exception as e:
        print(f"Failed with message: {str(e)}")
        response = flask.make_response(
            "Dataset screen display unsuccessful...", 403)
    return response


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
