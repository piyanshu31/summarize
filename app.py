from flask import Flask, render_template, request
from newspaper import Article
from textblob import TextBlob

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        url = request.form['url']
        article = Article(url)
        article.download()
        article.parse()

        blob = TextBlob(article.text)
        summary = blob.noun_phrases[:10]

        return render_template('index.html', summary=summary, url=url)

    except Exception as e:
        print(f"[ERROR] {e}")  # Shows in Render logs
        return render_template('index.html', summary=["❌ Internal Error: Could not summarize. Check URL or logs."], url="")
