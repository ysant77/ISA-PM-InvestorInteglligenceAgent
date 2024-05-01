# Python files
# from fetch_articles import fetch_articles
from fetch_articles import ArticleFetcher
from store_articles import ArticleStore
# from analyze_environmental import analyze_environmental
# from analyze_social import analyze_social
# from analyze_governance import analyze_governance
from analyze_esg import EnvironmentalAnalyzer, SocialAnalyzer, GovernanceAnalyzer
from calculate_overall_esg import ESGScoreCalculator



def esg_main(company_name, esg_file_name):
    # Fetch company and related news articles
    # articles = fetch_articles(company_name)
    fetch_articles = ArticleFetcher('ac5e2da3-0cad-4d4a-b9d3-53e7a86525c8')
    articles = fetch_articles.retrieve_articles(company_name)

    if articles:
        # Store articles for later analysis
        # storage_success = store_articles(articles)
        store_articles = ArticleStore()
        store_articles.save_articles_to_file(articles, esg_file_name)
        storage_success = store_articles.load_articles_from_file(esg_file_name)
    # if not storage_success:
    #     st.error("Failed to store articles for analysis.")
    #     st.stop()

    # # Analyze articles
    # environmental_score = analyze_environmental(articles)
    # social_score = analyze_social(articles)
    # governance_score = analyze_governance(articles)
    # print(f'articles:{articles}')
    article_title_arr = [article['title'] for article in articles]
    env_analyzer = EnvironmentalAnalyzer()
    social_analyzer = SocialAnalyzer()
    governance_analyzer = GovernanceAnalyzer()
    e_output_arr = env_analyzer.analyze(article_title_arr)
    s_output_arr = social_analyzer.analyze(article_title_arr)['score']
    g_output_arr = governance_analyzer.analyze(article_title_arr)['score']


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