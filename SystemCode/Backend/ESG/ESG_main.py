# Native Library
import os

# Third-party Library
import dotenv

# Python files
from ESG.fetch_articles import ArticleFetcher
from ESG.store_articles import ArticleStore
from ESG.analyze_esg import EnvironmentalAnalyzer, SocialAnalyzer, GovernanceAnalyzer
from ESG.calculate_overall_esg import ESGScoreCalculator
# need one more api_key file to contain eventregistry and newsapi (directory at backend)

dotenv.load_dotenv(r'Backend/.env')
# dotenv.load_dotenv(r'RAG/.env')

def esg_main(company_name, esg_file_name):
    # Fetch company and related news articles
    
    # fetch_articles = ArticleFetcher('ac5e2da3-0cad-4d4a-b9d3-53e7a86525c8')
    event_reg_api_key = os.environ.get("EVENT_REG_API_KEY")
    fetch_articles = ArticleFetcher(event_reg_api_key)
    articles = fetch_articles.retrieve_articles(company_name)

    if articles:
        # Store articles for later analysis
        store_articles = ArticleStore()
        store_articles.save_articles_to_file(articles, esg_file_name)
        storage_success = store_articles.load_articles_from_file(esg_file_name)

    # # Analyze articles
    article_title_arr = [article['title'] for article in articles]
    env_analyzer = EnvironmentalAnalyzer()
    social_analyzer = SocialAnalyzer()
    governance_analyzer = GovernanceAnalyzer()
    e_output_arr = env_analyzer.analyze(article_title_arr)
    s_output_arr = social_analyzer.analyze(article_title_arr)
    g_output_arr = governance_analyzer.analyze(article_title_arr)


    environmental_score_arr = [output['score'] for output in e_output_arr]
    social_score_arr = [output['score'] for output in s_output_arr]
    governance_score_arr = [output['score'] for output in g_output_arr]

    environmental_score = round(sum(environmental_score_arr)/ float(len(environmental_score_arr)), 3)
    social_score = round(sum(social_score_arr)/ float(len(social_score_arr)), 3)
    governance_score = round(sum(governance_score_arr)/ float(len(governance_score_arr)), 3)


    # Calculate and print overall ESG scores using different approaches.
    overall_esg_scores = ESGScoreCalculator.calculate_overall_esg_score(
        environmental_score, social_score, governance_score
    )
    overall_esg_scores['E_score'] = environmental_score
    overall_esg_scores['S_score'] = social_score
    overall_esg_scores['G_score'] = governance_score


    return storage_success, overall_esg_scores