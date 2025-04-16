import tkinter as tk
from tkinter import Text
from textblob import TextBlob
from newspaper import Article
from bs4 import BeautifulSoup
import requests

def summarize():
    url = utext.get('1.0', "end").strip()

    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        title_text = article.title
        authors_text = ', '.join(article.authors)
        publication_text = str(article.publish_date)
        summary_text = article.summary
        analysis = TextBlob(article.text)

    except:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            content = ' '.join(p.get_text() for p in paragraphs)

            title_text = soup.title.string if soup.title else "N/A"
            authors_text = "N/A"
            publication_text = "N/A"
            summary_text = content[:500] + "..." if len(content) > 500 else content
            analysis = TextBlob(content)

        except Exception as e:
            summary_text = f"Failed to summarize. Error: {e}"
            analysis = TextBlob("")

    title.config(state='normal')
    author.config(state='normal')
    publication.config(state='normal')
    summary.config(state='normal')
    sentiment.config(state='normal')

    title.delete('1.0', 'end')
    title.insert('1.0', title_text)

    author.delete('1.0', 'end')
    author.insert('1.0', authors_text)

    publication.delete('1.0', 'end')
    publication.insert('1.0', publication_text)

    summary.delete('1.0', 'end')
    summary.insert('1.0', summary_text)

    sentiment_text = f"Polarity: {analysis.polarity}, Sentiment: "
    sentiment_text += "positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"
    sentiment.delete('1.0', 'end')
    sentiment.insert('1.0', sentiment_text)

    title.config(state='disabled')
    author.config(state='disabled')
    publication.config(state='disabled')
    summary.config(state='disabled')
    sentiment.config(state='disabled')


# GUI
root = tk.Tk()
root.title("Universal URL Summarizer - Dark Mode")
root.geometry("1200x600")
root.configure(bg='black')  # Set window background

def label_and_text(label_name, height=1):
    label = tk.Label(root, text=label_name, fg='white', bg='black', font=("Arial", 10, "bold"))
    label.pack()
    text_box = tk.Text(root, height=height, width=140, bg='black', fg='white', insertbackground='white')
    text_box.config(state='disabled')
    text_box.pack()
    return text_box

title = label_and_text("Title")
author = label_and_text("Author")
publication = label_and_text("Publication Date")
summary = label_and_text("Summary", height=20)
sentiment = label_and_text("Sentiment")

ulabel = tk.Label(root, text="Enter URL", fg='white', bg='black', font=("Arial", 10, "bold"))
ulabel.pack()
utext = tk.Text(root, height=1, width=140, bg='black', fg='white', insertbackground='white')
utext.pack()

btn = tk.Button(root, text="Summarize", command=summarize, bg="#444444", fg="white", font=("Arial", 10, "bold"))
btn.pack(pady=10)

root.mainloop()
