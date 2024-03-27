
# Native Libraries
from datetime import datetime, timedelta
import random
import time
import copy
from pathlib import Path
import ast

# Third-party libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

# Python Files
from Company_Scrapping import scrape_n_return

################################## FIXED PATHS FOR DISPLAYING WEBPAGE ##################################
# Get the current working directory
current_dir = Path.cwd()

finanalysis_history_dir = current_dir / 'history'
finanalysis_history_dir.mkdir(exist_ok=True)  # exist_ok=True prevents errors if it exists

csv_path_1 = finanalysis_history_dir / 'latest_company_info.csv'

################################## STATIC PROPERTIES ##################################
# Set page title and favicon
st.set_page_config(page_title="FinAnalysis", page_icon="🌌", layout="wide")

# Define colors
primary_background_color = "#FAF1E4" # beige
# color_2 = "#CEDEBD" # pale green
color_2 = "#1f5e47" # dark green
color_3 = "#9EB384" # green
color_4 = "#435334" # dark dark green

# Define font
font = "Roboto"

# Set the style of the app
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun&display=swap');

    html, body, [class*="st-"] {{
        font-family: 'Sarabun', sans-serif;
    }}

    /* Webpage background color */
    .stApp {{
        background-color: {primary_background_color};
    }}
    /* Sidebar background color */
    #root div.st-emotion-cache-6qob1r.eczjsme3{{
        background-color: {color_3}; /* Example: Set to dark green */
    }}
    #root div.st-emotion-cache-6qob1r.eczjsme3 h2 {{
      font-size: 30px;
    }}
    /* Sidebar Header Input Text */
    #root div.st-emotion-cache-6qob1r.eczjsme3 p {{
        font-size:20px;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{
        font-size: 25px;
    }}
    .reportview-container .main .block-container{{
        max-width: 1200px;
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }}
    .reportview-container .main {{
        color: {color_4};
        background-color: {primary_background_color};
        font-family: '{font}';
    }}
    .reportview-container .main h1{{
        color: {color_4};
        font-size: 48px;
    }}
    .reportview-container .main h2{{
        color: {color_4};
        font-size: 32px;
    }}
    .reportview-container .main h3{{
        color: {color_4};
        font-size: 24px;
    }}
    .reportview-container .main h4{{
        color: {color_4};
        font-size: 16px;
    }}
    .reportview-container .main p{{
        color: {color_4};
        font-size: 14px;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


########### SIDEBAR: CHATBOT INTERFACE ###########
# Add a sidebar
sidebar = st.sidebar
sidebar.header("FinAnalysis 🌌")


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


with sidebar:

    st.title("Simple chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask here"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator())
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    



########### OUTPUTS ###########
def display_webpage(company_info, stock_data):
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


    # Create a DataFrame with sample information for the news/highlights
    news_titles = [
        "Apple launches new iPhone 13 with improved camera and battery life",
        "Apple faces antitrust lawsuit over App Store practices",
        "Apple reports record revenue and profit in Q4 2020",
        "Apple acquires AI startup for $1 billion",
        "Apple announces new MacBooks with M1 chip"
    ]

    news_summaries = [
        "Apple unveiled its latest flagship smartphone, the iPhone 13, which features a redesigned camera system, a longer battery life, and a faster processor.",
        "A group of app developers filed a class-action lawsuit against Apple, alleging that the company abuses its monopoly power over the App Store and charges excessive fees.",
        "Apple posted its best quarterly results ever, with revenue of $111.4 billion and profit of $28.8 billion, driven by strong demand for its products and services amid the pandemic.",
        "Apple confirmed that it has acquired an AI startup called Lattice Data, which specializes in turning unstructured data into structured data.",
        "Apple introduced its new line of MacBooks, which are powered by its own M1 chip, which promises faster performance, better battery life, and improved security."
    ]

    # Generate sample dates for each news item
    sample_dates = [(datetime.now() - timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(len(news_titles))]

    # Combine the titles, summaries, and dates into a DataFrame
    news = pd.DataFrame({
        "Date": sample_dates,
        "Title": news_titles,
        "Summary": news_summaries
    })

    ############ STATIC DESIGN ##############

    # # Create tabs for the webpage
    tab1, tab2 = st.tabs(["Profile", "Analysis"])


    # Create the Profile tab
    # with tabs.beta_expander("Profile"):
    with tab1:
        # Create columns for the tab
        col1, col2 = st.columns([0.66, 0.33])

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
            for index, row in news.iterrows():
                # st.markdown(f"<div style='border: 1px solid {color_2}; margin-bottom: 10px; padding: 10px; border-radius: 10px;'>", unsafe_allow_html=True)
                # st.markdown(f"<h4 style='color: {color_3};'>{row['Date']} - {row['Title']}</h4>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='color: {color_2};'>{row['Title']}</h4> - {row['Date']}", unsafe_allow_html=True)
                st.markdown(f"<p>{row['Summary']}</p>", unsafe_allow_html=True)
                # st.markdown("</div>", unsafe_allow_html=True)


    # ======================================================================


    # Create the Analysis tab
    with tab2:

        # Create a title for the tab
        st.title("Analysis")

        # Create a DataFrame with sample information for the ESG rating
        esg_rating = pd.Series([50, 40, 60], index=["Environment", "Social", "Governance"])

        # Show the ESG rating in a pie chart
        st.markdown(f"<h3>ESG Spotlight</h3>", unsafe_allow_html=True)
        esg_chart = px.pie(esg_rating, names=esg_rating.index, values=esg_rating.values, title="ESG Rating")
        esg_chart.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(esg_chart, use_container_width=True, height=600)

        # Create a DataFrame with sample information for the employees' feedback
        employees_feedback = pd.DataFrame({
            "Feedback": ["Buy", "Overweight", "Hold", "Underweight", "Sell"],
            "Count": [30, 20, 10, 5, 5],
            "Percentage": [0.5, 0.33, 0.17, 0.08, 0.08]
        })

        # Show the employees' feedback in a bar chart
        st.markdown(f"<h3>Employees' Feedback</h3>", unsafe_allow_html=True)
        feedback_chart = px.bar(employees_feedback, x="Feedback", y="Percentage", title="Employees' Feedback")
        feedback_chart.update_layout(yaxis_title="Percentage (%)")
        st.plotly_chart(feedback_chart, use_container_width=True, height=600)

        # Create a DataFrame with sample information for the top 3 competitors of the company
        competitors_data = [
            ("Microsoft Corporation", pd.DataFrame({
                "Feedback": ["Buy", "Overweight", "Hold", "Underweight", "Sell"],
                "Count": [25, 15, 15, 10, 5],
                "Percentage": [0.42, 0.25, 0.25, 0.17, 0.08]
            })),
            ("Amazon.com, Inc.", pd.DataFrame({
                "Feedback": ["Buy", "Overweight", "Hold", "Underweight", "Sell"],
                "Count": [20, 20, 10, 5, 5],
                "Percentage": [0.33, 0.33, 0.17, 0.08, 0.08]
            })),
            ("Samsung Electronics Co., Ltd.", pd.DataFrame({
                "Feedback": ["Buy", "Overweight", "Hold", "Underweight", "Sell"],
                "Count": [15, 15, 15, 10, 5],
                "Percentage": [0.25, 0.25, 0.25, 0.17, 0.08]
            }))
        ]

        # Show the competitors' feedback in a bar chart
        st.markdown(f"<h3>Competitors' Feedback</h3>", unsafe_allow_html=True)
        for competitor_name, competitor_rating in competitors_data:
            st.markdown(f"<h4>{competitor_name}</h4>", unsafe_allow_html=True)
            competitor_chart = px.bar(competitor_rating, x="Feedback", y="Percentage", title=f"{competitor_name}'s Feedback")
            competitor_chart.update_layout(yaxis_title="Percentage (%)")
            st.plotly_chart(competitor_chart, use_container_width=True, height=600)

        # Create a DataFrame with sample information for the financial ratios
        financial_ratios = pd.DataFrame({
            "Ratio": ["Gross Margin", "Operating Margin", "Net Margin", "Return on Equity", "Return on Assets", "Debt to Equity", "Current Ratio", "Price to Book", "Price to Sales", "Price to Earnings"],
            "Value": [0.4, 0.25, 0.2, 0.15, 0.1, 0.5, 1.5, 10, 5, 20]
        })

        # Show the financial ratios in a table
        st.markdown(f"<h3>Financial Analysis</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4>Financial Ratios</h4>", unsafe_allow_html=True)
        st.table(financial_ratios)

        
        # Create a DataFrame with sample information for the overall recommendation
        overall_recommendation = pd.DataFrame({
            "Feedback": ["Buy", "Overweight", "Hold", "Underweight", "Sell"],
            "Count": [30, 20, 10, 5, 5],
            "Percentage": [0.5, 0.33, 0.17, 0.08, 0.08]
        })

        # Show the overall recommendation in a pie chart
        st.markdown(f"<h4>Overall Recommendation</h4>", unsafe_allow_html=True)
        recommendation_chart = px.pie(overall_recommendation, names="Feedback", values="Percentage", title="Overall Recommendation")
        recommendation_chart.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(recommendation_chart, use_container_width=True, height=600)



########### EXPANDER: USER INPUTS (ensure chatbot does not affect webpage) ###########
# Expander
expander = st.expander('User Inputs')
with expander:
    username = st.text_input('User', value='')
    company_name = st.text_input('Company Name', value='')
    start_date = st.date_input('Start Date', value=pd.to_datetime('2023-01-01'))
    end_date = st.date_input('End Date', value=pd.to_datetime('today'))
    submit_button = expander.button("Submit")

if submit_button:
    # display_webpage(username, company_name, start_date, end_date)
    company_info = scrape_n_return(username, company_name)
    # Download the stock data from Yahoo Finance
    stock_data = yf.download(company_info[-1], start=start_date, end=end_date, progress=False)

    # save (rewrite) latest company info out
    company_info_df = pd.DataFrame(company_info)
    company_info_df.to_csv(csv_path_1.as_posix(), index=False, header=False)
 

try:
    # Read the CSV file
    company_info_df = pd.read_csv(csv_path_1.as_posix(), header=None)
    company_info = tuple(company_info_df[0])

    # Download the stock data from Yahoo Finance
    stock_data = yf.download(company_info[-1], start=start_date, end=end_date, progress=False)

    print('b')
    display_webpage(company_info, stock_data)
    print('c')
except:
    st.markdown(f"<h3>Welcome to FinAnalysis! 🌌 Give some inputs on your left to begin <-</h3>", unsafe_allow_html=True) # DONE
