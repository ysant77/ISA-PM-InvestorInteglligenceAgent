from flask import Flask, render_template
from fetch_articles import ArticleFetcher
from analyze_articles import ArticleAnalyzer

app = Flask(__name__)

@app.route('/')
def home():
    company_name = 'Your Company Name'  # Replace with your actual company name
    api_key = 'Your API Key'  # Replace with your actual API key

    fetcher = ArticleFetcher(api_key)
    articles = fetcher.retrieve_articles(company_name)

    analyzer = ArticleAnalyzer()
    results = [analyzer.analyze(article['content']) for article in articles]

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)