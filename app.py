from flask import Flask, jsonify
import numpy as np
import GoogleNews
from GoogleNews import GoogleNews
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/paraphrase-distilroberta-base-v2')

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Google News API"

@app.route('/<string:headline>', methods=['GET'])
def get(headline):
    v1 = model.encode(headline).reshape(-1,1)
    googlenews = GoogleNews()
    googlenews.set_lang('en')
    googlenews.set_period('1d')
    googlenews.set_encode('utf-8')
    googlenews.get_news(headline)
    res = googlenews.result()
    embeds = model.encode(res)

    req_news = []
    for i in range(len(embeds)):
        v2 = embeds[i].reshape(-1,1)
        cos_sim = np.dot(v1.T, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
        if cos_sim>0.5 and cos_sim<0.95:
            req_news.append(res[i])
        if len(req_news)>2:
            break

    return jsonify(req_news)


if __name__ == '__main__':
    app.run(debug=True)