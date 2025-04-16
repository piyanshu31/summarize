from flask import Flask, render_template, request
from newspaper import Article
from bs4 import BeautifulSoup
import nltk

nltk.download('punkt')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    url = request.form['url']
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    return render_template('index.html', summary=article.summary, title=article.title)

if __name__ == '__main__':
    app.run(debug=True)
