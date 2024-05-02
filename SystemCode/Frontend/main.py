# Native Libraries
from datetime import datetime, timedelta
import random
import time
import copy
from pathlib import Path
import ast
import sys
from io import BytesIO, StringIO
import zipfile
import uuid
import json
import subprocess
import sys

# # def install(package):
# subprocess.check_call([sys.executable, "-m", "pip", "install", 'transformers==4.38.0'])


# Third-party libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import altair as alt
import nltk
from PIL import Image
# nltk.download('vader_lexicon')

# Python Files
sys.path.insert(1, 'Backend')

from Company_Scrapping import scrape_n_return, performance_analysis, news_scrape_API, news_scrape_rpa, interpret_sentiment_v2
from GD_SentimentAnalysis import glassdoor_analysis
from Neuro_Fuzzy.gemma_inference import gemma_respond
from ESG.ESG_main import esg_main


# Get the current working directory
current_dir = Path.cwd()
backend_dir = current_dir / 'Backend'
frontend_dir = current_dir / 'Frontend'

# Set page configuration
st.set_page_config(page_title="FinAnalysis", page_icon="📊", layout="wide")

# Cover image and title
image = Image.open((frontend_dir / 'Cover.jpg').as_posix())
st.image(image, use_column_width=True)
st.title("IMMI Your All in One FinAnalysis 🧭")

# Local CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css((frontend_dir / "style.css").as_posix())


################################## FIXED PATHS FOR DISPLAYING WEBPAGE ##################################

finanalysis_history_dir = backend_dir / 'history'
finanalysis_history_dir.mkdir(exist_ok=True)  # exist_ok=True prevents errors if it exists

csv_path_1_1 = finanalysis_history_dir / 'latest_company_info.csv'
csv_path_2_1 = finanalysis_history_dir / 'latest_company_news.csv'
csv_path_3_1 = finanalysis_history_dir / 'latest_company_sentiment.csv'
csv_path_4_1 = finanalysis_history_dir / 'latest_glassdoor_scrape.csv'
csv_path_5_1 = finanalysis_history_dir / 'latest_esg_stats.csv'


scraped_data_dir = backend_dir / 'Neuro_Fuzzy' / 'scraped_data'
scraped_data_dir.mkdir(exist_ok=True)

esg_articles_json_path = finanalysis_history_dir / 'esg_articles.json'
zip_path_dl = Path(r'FinAnalysis Report.zip')



################################## STATIC PROPERTIES ##################################

# Define colors
primary_background_color = "#f6f6f6" # beige
color_2 = "#CEDEBD" # pale green
color_3 = "#9EB384" # green
color_4 = "#435334" # dark green



########### OUTPUTS ###########
def display_webpage(buf, company_info, stock_data, company_news_df, company_sentiment_df, glassdoor_df, esg_stats_df):
    (
        live_price, stock_market, ticker, currency, prev_close, open_price, trade_daily_volume, day_price_range, \
        day_low, day_high, market_cap, pe_ratio_ttm, eps_ttm, company_name_full, company_industry, employee_count, \
        fwd_ann_div_rate, fwd_ann_div_yield, trail_ann_div_rate, trail_ann_div_yield, company_description, \
        roe, roa, net_profit_margin, p_s_ratio_ttm, d_e_ratio, current_ratio, p_b_ratio, key_personnel, \
        ticker_yf
    )= company_info

    key_personnel = ast.literal_eval(key_personnel)
    key_personnel_df = pd.DataFrame(key_personnel, columns=['Name', 'Position', f'Salary ({currency})', 'Year of Birth', 'Age'])
    key_personnel_df = key_personnel_df.astype(str)
    key_personnel_df.index += 1

    financial_ratios = performance_analysis([roe, roa, net_profit_margin, p_s_ratio_ttm, d_e_ratio, current_ratio, p_b_ratio, pe_ratio_ttm], buy_threshold=18, sell_threshold=12)
    company_rating, job_recommendation, ceo_approval, pros_header, pros_description, cons_header, cons_description, comp_rating, comp_job_rec, comp_ceo_approval, top_competitors, company_rating_rank, company_job_rec_rank, company_ceo_app_rank = glassdoor_df[0]


    st.download_button(label='Download Report', data=buf.getvalue(), file_name=zip_path_dl.as_posix(), mime="application/zip") # , data=total_df.to_csv(index=False).encode('utf-8')
    # Create tabs for the webpage
    tab1, tab2, tab3 = st.tabs(["Profile", "Analysis", "Chatbot"])


    # Create the Profile tab
    with tab1:
        # Create columns for the tab
        col1, col2 = st.columns((2, 1), gap="large")

        # Show the company description in the first column
        with col1:
            # Show the company name and industry below the logo
            st.markdown(f"<h1>{company_name_full} ({ticker})</h1>", unsafe_allow_html=True) # DONE
            st.markdown(f"<h4>Industry: {company_industry}</h4>", unsafe_allow_html=True) # DONE

            st.markdown(f"<h3>About</h3>", unsafe_allow_html=True)

            st.markdown(f"<style>p {{text-align: justify}}</style><p>{company_description}</p>", unsafe_allow_html=True) # DONE

            st.markdown(f"<p><b>Number of Employees:</b> {employee_count}</p>", unsafe_allow_html=True) # DONE


        # Show the financial information in the first column
        with col1:
            st.markdown(f"<h3>Financial Information</h3>", unsafe_allow_html=True)
            st.markdown(f"<h4>Stock Price Trend</h4>", unsafe_allow_html=True)

            fig = go.Figure(data=[go.Candlestick(
                x=stock_data.index,
                open=stock_data['Open'],
                high=stock_data['High'],
                low=stock_data['Low'],
                close=stock_data['Close']
            )])
            fig.update_layout(yaxis_title=f"Price ({currency})")
            st.plotly_chart(fig, use_container_width=True, height=600)


            st.markdown(f"<p><b>Current Live Stock Price:</b> {float(live_price):.2f} {currency}</p>", unsafe_allow_html=True) # current_price:.2f; DONE
            st.markdown(f"<p><b>Day's Price Range:</b> {day_low} - {day_high} {currency}</p>", unsafe_allow_html=True) # {day_low:.2f} - {day_high:.2f}; DONE
            st.markdown(f"<p><b>Open Market Stock Price:</b> {open_price} {currency}</p>", unsafe_allow_html=True) # open_price:.2f; DONE
            st.markdown(f"<p><b>Previous Day Close Price:</b> {prev_close} {currency}</p>", unsafe_allow_html=True) # previous_close:.2f; DONE


        # Show the financial information in the first column
        with col1:
            # Create a chart object for the volume
            volume_chart = alt.Chart(stock_data.reset_index()).mark_line().encode(
                x="Date",
                y=alt.Y("Volume", title="Volume")
            )
            # Display the chart using the st.altair_chart function
            st.altair_chart(volume_chart, use_container_width=True)

            st.markdown(f"<p><b>Trade Daily Volume:</b> { (float(trade_daily_volume.replace(',','')) / 1e6):.2f} M</p>", unsafe_allow_html=True) # volume; DONE
            st.markdown(f"<p><b>Market Capacity:</b> {market_cap}</p>", unsafe_allow_html=True) # {market_cap / 1e9:.2f} B; DONE
            st.markdown(f"<p><b>PE Ratio (TTM):</b> {pe_ratio_ttm}</h4>", unsafe_allow_html=True) # pe_ratio_ttm; DONE
            st.markdown(f"<p><b>Earnings Per Share (TTM):</b> {eps_ttm}</p>", unsafe_allow_html=True) # {eps:.2f} {currency}; DONE
            st.markdown(f"<p><b>Forward Annual Dividend Rate:</b> {fwd_ann_div_rate}</p>", unsafe_allow_html=True) # {forward_dividend_rate:.2f} {currency}; DONE
            st.markdown(f"<p><b>Forward Annual Dividend Yield:</b> {fwd_ann_div_yield}</p>", unsafe_allow_html=True) # {forward_dividend_yield:.2%}; DONE
            st.markdown(f"<p><b>Trailing Annual Dividend Rate:</b> {trail_ann_div_rate}</p>", unsafe_allow_html=True) # {trailing_dividend_rate:.2f} {currency}; DONE
            st.markdown(f"<p><b>Trailing Annual Dividend Yield:</b> {trail_ann_div_yield}</p>", unsafe_allow_html=True) # {trailing_dividend_yield:.2%}; DONE
            st.markdown(f"<p><b>Return on Equity:</b> {roe}</p>", unsafe_allow_html=True) # DONE
            st.markdown(f"<p><b>Return on Assets:</b> {roa}</p>", unsafe_allow_html=True) # DONE
            st.markdown(f"<p><b>Profit Margin:</b> {net_profit_margin}</p>", unsafe_allow_html=True) # DONE
            st.markdown(f"<p><b>Price/ Sales Ratio (TTM):</b> {p_s_ratio_ttm}</p>", unsafe_allow_html=True) # DONE
            st.markdown(f"<p><b>Total Debt/ Equity Ratio:</b> {d_e_ratio}</p>", unsafe_allow_html=True) # DONE
            st.markdown(f"<p><b>Current Ratio:</b> {current_ratio}</p>", unsafe_allow_html=True) # DONE
            st.markdown(f"<p><b>Price/ Book Ratio:</b> {p_b_ratio}</p>", unsafe_allow_html=True) # DONE



        # Show the key personnel in the first column
        with col1:
            st.markdown(f"<h3>Leadership Snippet</h3>", unsafe_allow_html=True)
            st.table(key_personnel_df) # DONE


        # Display the news/highlights with dates in the Streamlit app
        with col2:
            st.markdown(f"<h3>News/Highlights</h3>", unsafe_allow_html=True)
            for index, row in company_news_df.iterrows():
                st.markdown(f"<h4 style='color: {color_3};'>{row['Title']}</h4>", unsafe_allow_html=True)
                st.markdown(f"<b>{row['Date']}</b>", unsafe_allow_html=True)
                st.markdown(f"<p2>{row['Summary']}</p2>", unsafe_allow_html=True)


    # ======================================================================


    # Create the Analysis tab
    with tab2:

        # Create a title for the tab
        st.title("Analysis")

        e_score, s_score, g_score = esg_stats_df['E_score'].item(), esg_stats_df['S_score'].item(), esg_stats_df['G_score'].item()
        backtested_weights, equal_weights, industry_specific_weights = esg_stats_df['Backtested Weights Score (Rank 1 - Best Performance)'].item(), \
        esg_stats_df['Equal Weight Score (Rank 2 - Second Best Performance)'].item(), \
        esg_stats_df['Industry-Specific Weights Score (Rank 3 - Third Best Performance)'].item()

        # Show ESG Stats
        st.markdown(f"<h3>ESG Results</h3>", unsafe_allow_html=True)
        fig = go.Figure(layout_yaxis_range=[0,1])
        fig.add_trace(go.Bar(x=['Environmental', 'Social', 'Governance'],
                             y=[e_score, s_score, g_score],
                             marker_color=['green', 'red', 'blue'],
                             text= [e_score, s_score, g_score],
                             textposition='auto'
                             ))
        fig.update_layout(xaxis_tickfont=dict(size=14))
        st.plotly_chart(fig, use_container_width=True)


        # Plot for ESG average methods
        avg_methods = ['Backtested Weights', 'Equal Weights', 'Industry-Specific Weights']
        scores = [backtested_weights, equal_weights, industry_specific_weights]
    
        fig_avg = go.Figure()
        fig_avg.add_trace(go.Bar(x=avg_methods,
                                 y=scores,
                                 text= scores,
                                 textposition='auto'
                                ))
        fig_avg.update_layout(xaxis_tickfont=dict(size=14))
        st.plotly_chart(fig_avg, use_container_width=True)


        # Show the financial ratios in a table
        st.markdown(f"<h3>Financial Analysis</h3>", unsafe_allow_html=True)
        st.table(pd.DataFrame(financial_ratios))

        
        # Sentiment Analysis
        st.markdown(f"<h3>Sentiment Analysis of News (API and RPA)</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Total Number of Positive-Sentiment Articles:</b> {company_sentiment_df.iloc[0,0]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Total Number of Negative-Sentiment Articles:</b> {company_sentiment_df.iloc[1,0]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Total Number of Neutral-Sentiment Articles:</b> {company_sentiment_df.iloc[2,0]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Total Number of Articles:</b> {company_sentiment_df.iloc[3,0]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Sentiment Interpretation:</b> {company_sentiment_df.iloc[4,0]}</p>", unsafe_allow_html=True)


        # GLASSDOOR SCRAPPED INFO
        st.markdown(f'<h3>Company Review</h3>', unsafe_allow_html=True)
        st.markdown(f'<h4>Overall</h4>', unsafe_allow_html=True)

        fig_overall_review = make_subplots(rows=1, cols=3) # , subplot_titles=("Company's Rating (based on employees)", \

        # Add traces to each subplot
        fig_overall_review.add_trace(go.Bar(x=["Company's Rating (based on employees)"], y=[float(company_rating)], text=[float(company_rating)], textposition='auto'), row=1, col=1) # , name='Data 1'
        fig_overall_review.add_trace(go.Bar(x=["Likelihood of Recommendation of Company"], y=[int(job_recommendation.split('%')[0])], text=[job_recommendation], textposition='auto'), row=1, col=2)
        fig_overall_review.add_trace(go.Bar(x=["Employees' Approval of CEO"], y=[int(ceo_approval.split('%')[0])], text=[ceo_approval], textposition='auto'), row=1, col=3)

        # Update y-axis ranges independently
        fig_overall_review.update_yaxes(range=[0, 5], row=1, col=1)
        fig_overall_review.update_yaxes(range=[0, 100], title_text='Percentage', row=1, col=2)
        fig_overall_review.update_yaxes(range=[0, 100], title_text='Percentage', row=1, col=3)

        fig_overall_review.update_layout(height=500, width=900, xaxis_tickfont=dict(size=14), showlegend=False)

        st.plotly_chart(fig_overall_review, use_container_width=True)


        header_dic = {}
        header_dic['Pros'] = [pro for pro in ast.literal_eval(pros_header)]
        header_dic['Cons'] = [con for con in ast.literal_eval(cons_header)]
        review_header_df = pd.DataFrame(header_dic)
        review_header_df.index += 1

        desc_dic = {}
        desc_dic['Pros'] = [pro for pro in ast.literal_eval(pros_description)]
        desc_dic['Cons'] = [con for con in ast.literal_eval(cons_description)]
        review_desc_df = pd.DataFrame(desc_dic)
        review_desc_df.index += 1

        st.markdown(f'<h4>Pros & Cons (by employees) </h4>', unsafe_allow_html=True)

        st.markdown(f'<b>Headers</b>', unsafe_allow_html=True)
        st.table(review_header_df)

        st.markdown(f'<b>Description</b>', unsafe_allow_html=True)
        st.table(review_desc_df)


        top_competitors = ast.literal_eval(top_competitors)
        n = len(top_competitors)
        st.markdown(f'<h4>Comparison against Competitors</h4>', unsafe_allow_html=True)
        st.markdown(f"<b>Top {n} competitors assessed are: {top_competitors[0]}, {top_competitors[1]}, {top_competitors[2]}</b>", unsafe_allow_html=True)
        st.markdown(f"<b>Company's ratings ranks {company_rating_rank} out of {n+1}</b>", unsafe_allow_html=True)
        st.markdown(f"<b>Company's job recommendation rating ranks {company_job_rec_rank} out of {n+1}</b>", unsafe_allow_html=True)
        st.markdown(f"<b>Company's ceo approval rating ranks {company_ceo_app_rank} out of {n+1}</b>", unsafe_allow_html=True)

    # Chatbot
    with tab3:
        st.title("Ask me anything")

        if 'question_state' not in st.session_state:
            st.session_state.question_state = False

        if 'fbk' not in st.session_state:
            st.session_state.fbk = str(uuid.uuid4())


        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []


        # Starts here.
        question = st.chat_input(placeholder="Type here")
        bot_response = gemma_respond(question)
        if question:
            message_id = len(st.session_state.chat_history)
            st.session_state.chat_history.append({
                "question": question,
                "answer": bot_response,
                "message_id": message_id,
                })
            for entry in st.session_state.chat_history:
                with st.chat_message("human"):
                    st.write(entry["question"])
                with st.chat_message("ai"):
                    st.write(entry["answer"])

                    # # Chat History is saved
                    # test_df = pd.DataFrame(st.session_state.chat_history)
                    # test_df.dropna(inplace=True,how='any')
                    # test_df.to_csv('chat_history.csv',index=False)



########### EXPANDER: USER INPUTS (ensure chatbot does not affect webpage) ###########
# Expander
sidebar = st.sidebar
with sidebar:
    st.header('User Inputs')
    company_name = st.text_input('Company Name', value='')
    start_date = st.date_input('Start Date', value=pd.to_datetime('2023-01-01'))
    end_date = st.date_input('End Date', value=pd.to_datetime('today'))
    submit_button = sidebar.button("Submit")

if submit_button:
    # # display_webpage(username, company_name, start_date, end_date)
    company_info = scrape_n_return(company_name)
    # Download the stock data from Yahoo Finance
    stock_data = yf.download(company_info[-1], start=start_date, end=end_date, progress=False)

    # save (rewrite) latest company info out
    company_info_df = pd.DataFrame(company_info)
    company_info_df.to_csv(csv_path_1_1.as_posix(), index=False, header=False)

    start_date_arr = str(start_date).split('-')
    end_date_arr = str(end_date).split('-')
    start_date_str = start_date_arr[1]+'/'+start_date_arr[2]+'/'+start_date_arr[0] # MM/DD/YYYY
    end_date_str = end_date_arr[1]+'/'+end_date_arr[2]+'/'+end_date_arr[0] # MM/DD/YYYY

    # SAVE NEWS RELATED DATA
    end_date_ytd = str(end_date - pd.Timedelta(1, unit='D')) # get yesterday in case not enough
    _, _, API_articles = news_scrape_API(company_name, end_date_ytd)
    news_titles, news_summaries, news_dates, RPA_articles = news_scrape_rpa(start_date_str,end_date_str,company=company_name)
    sentiment_arr = interpret_sentiment_v2(API_articles, RPA_articles, 0.9)
    # save (rewrite) latest company's news section out
    company_news_df = pd.DataFrame({'Title':news_titles,'Summary':news_summaries,'Date':news_dates,'Articles':RPA_articles})
    company_news_df.to_csv(csv_path_2_1.as_posix(),index=False)
    
    company_sentiment_df = pd.DataFrame(sentiment_arr)
    company_sentiment_df.to_csv(csv_path_3_1.as_posix(),index=False, header=False)

    # SAVE GLASSDOOR REVIEW
    company_rating, job_recommendation, ceo_approval, pros_header, pros_description, cons_header, cons_description, comp_rating, comp_job_rec, comp_ceo_approval, top_competitors, company_rating_rank, company_job_rec_rank, company_ceo_app_rank = glassdoor_analysis(company_name)
    glassdoor_df = pd.DataFrame([company_rating, job_recommendation, ceo_approval, pros_header, pros_description, cons_header, cons_description, comp_rating, comp_job_rec, comp_ceo_approval, top_competitors, company_rating_rank, company_job_rec_rank, company_ceo_app_rank])
    glassdoor_df.to_csv(csv_path_4_1.as_posix(), index=False, header=False)

    # SAVE ESG DATA
    _, overall_esg_scores = esg_main(company_name, esg_articles_json_path)
    esg_stats_df = pd.DataFrame(overall_esg_scores, index=[0])
    esg_stats_df.to_csv(csv_path_5_1.as_posix(), index=False)


    # === Accumulated data for chatbot ===
    company_name_cap = company_name.title().replace(' ', '_')
    csv_path_1_2 = scraped_data_dir / f'{company_name_cap}_info.csv'

    scraped_news_dir = scraped_data_dir / 'collated_news'
    scraped_news_dir.mkdir(exist_ok=True)
    csv_path_2_2 = scraped_news_dir / f'{company_name_cap}_news.csv'

    csv_path_3_2 = scraped_data_dir / f'{company_name_cap}_sentiment.csv'
    csv_path_4_2 = scraped_data_dir / f'{company_name_cap}_glassdoor_scrape.csv'
    csv_path_5_2 = scraped_data_dir / f'{company_name_cap}_esg_stats.csv'

    company_info_df.to_csv(csv_path_1_2.as_posix(), index=False, header=False)
    company_news_df.to_csv(csv_path_2_2.as_posix(),index=False)
    company_sentiment_df.to_csv(csv_path_3_2.as_posix(),index=False, header=False)
    glassdoor_df.to_csv(csv_path_4_2.as_posix(), index=False, header=False)
    esg_stats_df.to_csv(csv_path_5_2.as_posix(), index=False)


try:
    #### RELOAD LAST FILE 
    # Read the CSV file
    company_info_df = pd.read_csv(csv_path_1_1.as_posix(), header=None)
    company_info = tuple(company_info_df[0])

    # Download the stock data from Yahoo Finance
    stock_data = yf.download(company_info[-1], start=start_date, end=end_date, progress=False)

    # Load latest news
    company_news_df = pd.read_csv(csv_path_2_1.as_posix())

    # Load sentiment analysis of news
    company_sentiment_df = pd.read_csv(csv_path_3_1.as_posix(), header=None)

    # Load data scraped from glassdoor
    glassdoor_df = pd.read_csv(csv_path_4_1.as_posix(), header=None)

    # Load ESG data
    esg_stats_df = pd.read_csv(csv_path_5_1.as_posix())

    buf = BytesIO()
    with zipfile.ZipFile(buf, "x") as csv_zip:
        csv_zip.writestr(f'{company_info[-1]}_info.csv', company_info_df.to_csv(index=False, header=False))
        csv_zip.writestr(f'{company_info[-1]}_news.csv', company_news_df.to_csv(index=False))
        csv_zip.writestr(f'{company_info[-1]}_sentiment.csv', company_sentiment_df.to_csv(index=False, header=False))
        csv_zip.writestr(f'{company_info[-1]}_glassdoor_scrape.csv', glassdoor_df.to_csv(index=False, header=False))
        csv_zip.writestr(f'{company_info[-1]}_esg_stats.csv', esg_stats_df.to_csv(index=False))


    display_webpage(buf, company_info, stock_data, company_news_df, company_sentiment_df, glassdoor_df, esg_stats_df)
except:
    st.markdown(f"<h3>Welcome to FinAnalysis! 🌌 Give some inputs at the top to begin!</h3>", unsafe_allow_html=True) # DONE
    pass
