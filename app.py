from flask import Flask, jsonify
from GoogleNews import GoogleNews

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Google News API"

@app.route('/news/<string:headline>', methods=['GET'])
def get(headline):
    googlenews = GoogleNews()
    googlenews.set_lang('en')
    googlenews.set_period('7d')
    googlenews.set_encode('utf-8')
    googlenews.search(headline)
    return jsonify(googlenews.result())


if __name__ == '__main__':
    app.run(debug=True)