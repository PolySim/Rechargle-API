import flask


app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/')
def index():
    return "<h1>Hello World</h1>"

@app.route('/hello')
def say_hello_world():
    return flask.jsonify({'result': "Hello Connected React World!!!"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6789)
