import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import sqlite3
from constants import db_path, selected_industries, cols_to_select
from utils import find_best_match, compute_derived_features

def get_recent_stock_data(industry, ticker_symbol):
    end_date = datetime.now().date()
    days_back = 40  # Start with more days back to ensure we cover 7 trading days
    start_date = end_date - timedelta(days=days_back)
    ticker = yf.Ticker(ticker_symbol)
    while True:
    # Fetch stock data from start_date to end_date
        stock_data = ticker.history(start=start_date, end=end_date)

        stock_data = stock_data[stock_data.index.dayofweek < 5]  

        if len(stock_data) >= 26:
            break  
        else:
            start_date = end_date - timedelta(days=days_back)

    if len(stock_data) > 26:
        stock_data = stock_data[-26:]
    currency = ticker.info['currency']
    sector = ticker.info['sector']
    stock_data['stock'] = ticker.info['symbol']
    stock_data['company'] = ticker.info['shortName']
    stock_data['industry'] = industry
    stock_data['currency'] = currency
    stock_data['sector'] = sector
    stock_data['country'] = ticker.info.get('country')
    stock_data = stock_data.rename(columns={'Stock Splits': 'Stock_Splits'})
    stock_data.reset_index(inplace=True)

    stock_data['Date'] = stock_data['Date'].dt.strftime('%Y-%m-%d')
    return stock_data
def get_main_dataset(company_name):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("select * from stock_prices", conn)
    df = df[df['Industry'].isin(selected_industries)]
    company, ticker_symbol, industry, _ = find_best_match(df, company_name)
    print("in func main dataset ", company, ticker_symbol, industry)
    stock_data = get_recent_stock_data(industry, ticker_symbol)
    #print(stock_data)
    df_tmp = compute_derived_features(stock_data)
    df_tmp = df_tmp[cols_to_select]
    df_tmp.dropna(inplace=True)
    return df_tmp, industry



