from flask import Flask, request
from nlp import analyze as nlp


app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to the NLP TextAnalyzer..."

@app.route("/analyze", methods=['POST'])
def analyze():
    return nlp(request.data.decode('utf-8'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("8085"), debug=True)
