from flask import Flask, request, render_template
from fetch_articles import ArticleFetcher
from store_articles import ArticleStore
from analyze_environmental import EnvironmentalAnalyzer
from analyze_social import SocialAnalyzer
from analyze_governance import GovernanceAnalyzer
from calculate_overall_esg import ESGScoreCalculator

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Assume we have a form field for company name and API key
        company_name = request.form.get('company_name')
        api_key = request.form.get('api_key')

        # Fetch and store articles
        fetcher = ArticleFetcher(api_key)
        articles = fetcher.retrieve_articles(company_name)
        ArticleStore.save_articles_to_file(articles, f'{company_name}_articles.json')

        # Load articles for analysis
        stored_articles = ArticleStore.load_articles_from_file(f'{company_name}_articles.json')
        
        # Perform ESG analysis
        env_analyzer = EnvironmentalAnalyzer()
        soc_analyzer = SocialAnalyzer()
        gov_analyzer = GovernanceAnalyzer()

        # Analyze each article for its ESG components and aggregate the scores
        env_scores = [env_analyzer.analyze(article['text']) for article in stored_articles]
        soc_scores = [soc_analyzer.analyze(article['text']) for article in stored_articles]
        gov_scores = [gov_analyzer.analyze(article['text']) for article in stored_articles]

        env_score = sum(score['score'] for score in env_scores) / len(env_scores)
        soc_score = sum(score['score'] for score in soc_scores) / len(soc_scores)
        gov_score = sum(score['score'] for score in gov_scores) / len(gov_scores)

        # Calculate the overall ESG scores using different approaches
        overall_esg_scores = ESGScoreCalculator.calculate_overall_esg_score(env_score, soc_score, gov_score)

        # Return the rendered template with ESG scores
        return render_template('results.html', 
                               company_name=company_name, 
                               environmental_score=env_score, 
                               social_score=soc_score, 
                               governance_score=gov_score,
                               overall_scores=overall_esg_scores)

    # GET request just renders the form for input
    return render_template('index.html')  # Assuming 'index.html' is the main form template

if __name__ == '__main__':
    app.run(debug=True)
