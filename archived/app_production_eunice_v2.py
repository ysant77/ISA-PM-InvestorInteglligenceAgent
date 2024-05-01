from datetime import datetime, timedelta
import random
import time
import copy
from pathlib import Path
import ast
import sys
from io import BytesIO
import zipfile

# Third-party libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import nltk
from PIL import Image
# nltk.download('vader_lexicon')

# Python Files
from Company_Scrapping import scrape_n_return, performance_analysis, news_scrape_API, news_scrape_rpa, interpret_sentiment_v2
from GD_SentimentAnalysis import glassdoor_analysis
#sys.path.insert(1, 'chatbot_neuro_fuzzy/')
#from gemma_inference import gemma_respond
sys.path.insert(1, 'ESG_edit/')
from ESG_main import esg_main


# Set page configuration
st.set_page_config(page_title="FinAnalysis", page_icon="📊", layout="wide")


# Cover image and title
image = Image.open('Cover2.jpg')
st.image(image, use_column_width=True)
st.title("IMMI Your All in One FinAnalysis 🧭", anchor='top')

# Local CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Helper function to load data
def load_data(company_name):
    company_info = scrape_n_return(company_name)
    stock_data = yf.download(company_info['ticker'], start="2023-01-01", end=datetime.now())
    glassdoor_data = glassdoor_analysis(company_name)
    esg_data = esg_main(company_name)
    return company_info, stock_data, glassdoor_data, esg_data

# Sidebar for user inputs
with st.sidebar:
    st.header("Give me a company name")
    company_name = st.text_input("Enter Company Name", "AAPL")
    start_date = st.date_input("Start Date", datetime(2023, 1, 1))
    end_date = st.date_input("End Date", datetime.today())
    if st.button("Load Data"):
        company_info, stock_data, glassdoor_data, esg_data = load_data(company_name)








# Main area
tab1, tab2, tab3 = st.tabs(["Profile", "Analysis", "Ask me anything"])

with tab1:
    st.subheader("Company Profile")
    if 'company_info' in locals():
        st.write("Industry:", company_info.get('industry', 'N/A'))
        st.write("Description:", company_info.get('description', 'No description available.'))

with tab2:
    st.subheader("Company Analysis")
    if 'stock_data' in locals():
        #fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                             #open=stock_data['Open'],
                                             #high=stock_data['High'],
                                             #low=stock_data['Low'],
                                             #close=stock_data['Close'])])
        #fig.update_layout(xaxis_rangeslider_visible=False)
        #st.plotly_chart(fig, use_container_width=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=['Environmental', 'Social', 'Governance'],
                             y=[esg_stats_df['E_score'].item(), esg_stats_df['S_score'].item(), esg_stats_df['G_score'].item()]))
    
        st.plotly_chart(fig, use_container_width=True)
    
        # Plot for ESG average methods
        avg_methods = ['Backtested Weights', 'Equal Weights', 'Industry-Specific Weights']
        scores = [esg_stats_df['Backtested Weights Score (Rank 1 - Best Performance)'].item(), \
        esg_stats_df['Equal Weight Score (Rank 2 - Second Best Performance)'].item(), \
        esg_stats_df['Industry-Specific Weights Score (Rank 3 - Third Best Performance)'].item()]
    
        fig_avg = go.Figure()
        fig_avg.add_trace(go.Bar(x=avg_methods, y=scores))
    
        st.plotly_chart(fig_avg, use_container_width=True)

        st.markdown(f"<h3>ESG Results</h3>", unsafe_allow_html=True)
        st.markdown(f"<b>Environmental Score: </b>{esg_stats_df['E_score'].item()}" , unsafe_allow_html=True)
        st.markdown(f"<b>Social Score: </b>{esg_stats_df['S_score'].item()}", unsafe_allow_html=True)
        st.markdown(f"<b>Governmental Score: </b>{esg_stats_df['G_score'].item()}", unsafe_allow_html=True)
        st.markdown(f"<b>Backtested Weights Score (Rank 1 - Best Performance):</b> {esg_stats_df['Backtested Weights Score (Rank 1 - Best Performance)'].item()}", unsafe_allow_html=True)
        st.markdown(f"<b>Equal Weight Score (Rank 2 - Second Best Performance):</b> {esg_stats_df['Equal Weight Score (Rank 2 - Second Best Performance)'].item()}", unsafe_allow_html=True)
        st.markdown(f"<b>Industry-Specific Weights Score (Rank 3 - Third Best Performance):</b> {esg_stats_df['Industry-Specific Weights Score (Rank 3 - Third Best Performance)'].item()}", unsafe_allow_html=True)


        # Show the financial ratios in a table
        st.markdown(f"<h3>Financial Analysis</h3>", unsafe_allow_html=True)
        # st.markdown(f"<h4>Financial Ratios</h4>", unsafe_allow_html=True)
        st.table(pd.DataFrame(financial_ratios))

        
        # Sentiment Analysis
        st.markdown(f"<h3>Sentiment Analysis of News</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Total Number of Positive-Sentiment Articles:</b> {company_sentiment_df.iloc[0,0]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Total Number of Negative-Sentiment Articles:</b> {company_sentiment_df.iloc[1,0]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Total Number of Neutral-Sentiment Articles:</b> {company_sentiment_df.iloc[2,0]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Total Number of Articles:</b> {company_sentiment_df.iloc[3,0]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Sentiment Interpretation:</b> {company_sentiment_df.iloc[4,0]}</p>", unsafe_allow_html=True)


        # GLASSDOOR SCRAPPED INFO
        st.markdown(f'<h3>Company Review</h3>', unsafe_allow_html=True)
        st.markdown(f'<h4>Overall</h4>', unsafe_allow_html=True)
        st.markdown(f'<p><b>Company\'s Rating (based on employees):</b> {company_rating} out of 5.0</p>', unsafe_allow_html=True)
        st.markdown(f'<p><b>Likelihood of recommendation of company:</b> {job_recommendation}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><b>Employees\' Approval of CEO:</b> {ceo_approval}</p>', unsafe_allow_html=True)

        pros_header_str = ''
        for i in ast.literal_eval(pros_header):
            pros_header_str += "- " + i + "\n"
        pros_desc_str = ''
        for i in ast.literal_eval(pros_description):
            pros_desc_str += "- " + i + "\n"
        st.markdown(f'<h4>Pros</h4>', unsafe_allow_html=True)
        st.markdown(f'<b>Headers:</b>\n{pros_header_str}', unsafe_allow_html=True)
        st.markdown(f'<b>Description:</b>\n{pros_desc_str}', unsafe_allow_html=True)

        cons_header_str = ''
        for i in ast.literal_eval(cons_header):
            cons_header_str += "- " + i + "\n"
        cons_desc_str = ''
        for i in ast.literal_eval(cons_description):
            cons_desc_str += "- " + i + "\n"
        st.markdown(f'<h4>Cons</h4>', unsafe_allow_html=True)
        st.markdown(f'<b>Headers:</b>\n{cons_header_str}', unsafe_allow_html=True)
        st.markdown(f'<b>Description:</b>\n{cons_desc_str}', unsafe_allow_html=True)

        # print(f'Top Competitors: {top_competitors[0]}, {top_competitors[1]}, {top_competitors[2]}')
        top_competitors = ast.literal_eval(top_competitors)
        n = len(top_competitors)
        st.markdown(f'<h4>Comparison against Competitors</h4>', unsafe_allow_html=True)
        st.markdown(f"<b>Top {n} competitors assessed are: {top_competitors[0]}, {top_competitors[1]}, {top_competitors[2]}</b>", unsafe_allow_html=True)
        st.markdown(f"<b>Company's ratings ranks {company_rating_rank} out of {n+1}</b>", unsafe_allow_html=True)
        st.markdown(f"<b>Company's job recommendation rating ranks {company_job_rec_rank} out of {n+1}</b>", unsafe_allow_html=True)
        st.markdown(f"<b>Company's ceo approval rating ranks {company_ceo_app_rank} out of {n+1}</b>", unsafe_allow_html=True)

with tab3:
    st.subheader("Ask Me Anything")
    user_input = st.text_input("Type your question here:")
    if user_input:
        response = "Responding to: " + user_input  # Placeholder for bot logic
        st.text_area("Bot says:", value=response, height=300)

if 'company_info' not in locals():
    st.info("Enter a company name and press 'Load Data' to display information.")

# Download report button
if 'stock_data' in locals():
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("stock_data.csv", stock_data.to_csv())
    st.download_button(label="Download Report", data=buffer, file_name="Financial_Report.zip", mime="application/zip")
