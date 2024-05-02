from eventregistry import *

class ArticleFetcher:
    def __init__(self, api_key):
        self.er = EventRegistry(apiKey=api_key)

    def retrieve_articles(self, company_name):
        """
        Retrieve articles for a given company name.
        """
        q = QueryArticlesIter(
            conceptUri=self.er.getConceptUri(company_name),
            dataType=["news", "blog"],
            lang=["eng"]  # You can specify multiple languages e.g., ["eng", "deu", "fra"]
        )
        articles = []
        for article in q.execQuery(self.er, sortBy="date", maxItems=300):
            # Assume each article is a dictionary and we want to store the 'body' text.
            # You might want to store other details like title, url, etc.
            articles.append({
                'text': article.get('body', ''),  # Extract the text from the article body
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'date': article.get('date', ''),
                # Include any other fields you need
            })
        return articles