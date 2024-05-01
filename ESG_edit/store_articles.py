import os
import json

class ArticleStore:
    @staticmethod
    def save_articles_to_file(articles, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_articles_from_file(filename):
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                articles = json.load(f)
                return articles
        return []