from flask import Flask, request
from mainFunction import main


app = Flask(__name__)

@app.route('/')
def index():
    return "API Working"



@app.route('/getHeadline',methods = ['POST'])
def getHeadline():
    try:
        url = request.json['url']
        return main(url)
    except:
        return 'Invalid Input Formate'

if __name__ == '__main__':
    app.run(debug=True)