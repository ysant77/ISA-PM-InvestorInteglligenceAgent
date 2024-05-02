import os
import sys

sys.path.insert(1, 'Backend')

from Company_Scrapping import scrape_n_return, performance_analysis, news_scrape_API, news_scrape_rpa, interpret_sentiment_v2
from GD_SentimentAnalysis import glassdoor_analysis

from Neuro_Fuzzy.gemma_inference import gemma_respond
from ESG.ESG_main import esg_main