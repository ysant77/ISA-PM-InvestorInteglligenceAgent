import pandas as pd
import os
import sqlite3
import yfinance as yf
from datetime import datetime, timedelta
from fuzzywuzzy import process, fuzz
import numpy as np
import json
from scipy.stats import mode
from constants import json_mapping_path
import re


def find_best_match(df, user_input):
    # Extract the list of company names from the database
    df['Company'] = df['Company'].apply(lambda x: x.lower().replace("inc", "").replace("inc.", "").strip())
    company_names = list(set(df['Company'].tolist()))
    #print("apple" in company_names)
    #company_names = [company_name.lower().replace("Inc", "").replace("Inc.", "") for company_name in company_names]
    #print(company_names)

    # Use fuzzy matching to find the best match for the user_input
    best_match, score = process.extractOne(user_input.lower(), company_names)
    #print(best_match, score)
    # Retrieve the corresponding ticker symbol from the database
    ticker_symbol = df.loc[df['Company'] == best_match, 'Stock'].iloc[0]

    # You can also retrieve the industry if needed
    industry = df.loc[df['Company'] == best_match, 'Industry'].iloc[0]

    return best_match, ticker_symbol, industry, score

# def find_best_match(df, user_input, score_cutoff=85):
#     # Convert to lowercase and strip spaces
#     user_input = user_input.lower().strip()

#     # Extract the list of company names from the database and preprocess them
#     company_names = list(set(df['Company'].str.lower().str.strip().tolist()))

#     # Use fuzzy matching to find the best match for the user_input
#     # You can try different scorers like fuzz.token_sort_ratio, fuzz.token_set_ratio, etc.
#     best_match, score = process.extractOne(user_input, company_names, scorer=fuzz.token_set_ratio)

#     print(best_match, score)

#     # Check if the score meets the minimum threshold
#     if score < score_cutoff:
#         return None, None, None, score

#     # Retrieve the best match in its original form
#     best_match_original = df.loc[df['Company'].str.lower().str.strip() == best_match, 'Company'].iloc[0]

#     # Retrieve the corresponding ticker symbol and industry from the database
#     ticker_symbol = df.loc[df['Company'] == best_match_original, 'Stock'].iloc[0]
#     industry = df.loc[df['Company'] == best_match_original, 'Industry'].iloc[0]

#     return best_match_original, ticker_symbol, industry, score

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, slow=26, fast=12):
    ema_fast = data.ewm(span=fast, adjust=False).mean()
    ema_slow = data.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def calculate_bollinger_bands(data, window=20):
    sma = data.rolling(window=window).mean()
    std = data.rolling(window=window).std()
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    return upper_band, sma, lower_band

def compute_derived_features(df_tech):
  df_tech['Price_Range'] = df_tech['High'] - df_tech['Low']

  # Calculate daily percentage change
  df_tech['Pct_Change'] = df_tech['Close'].pct_change() * 100

  # Calculate a simple moving average (SMA) over a 7-day window
  df_tech['SMA_7'] = df_tech['Close'].rolling(window=7).mean()

  # Calculate exponential moving average (EMA) for a faster response to recent price changes, over a 7-day window
  df_tech['EMA_7'] = df_tech['Close'].ewm(span=7, adjust=False).mean()

  # Calculate volatility (standard deviation of daily price change)
  df_tech['Volatility'] = df_tech['Pct_Change'].rolling(window=7).std()

  #df_tech.dropna(inplace=True)

  df_tech['RSI'] = calculate_rsi(df_tech['Close'], window=7)

  df_tech['MACD'], df_tech['MACD_Signal'] = calculate_macd(df_tech['Close'], slow=13, fast=6)

  df_tech['BB_Upper'], df_tech['BB_Middle'], df_tech['BB_Lower'] = calculate_bollinger_bands(df_tech['Close'], window=7)

  df_tech['VWAP'] = (df_tech['Volume'] * (df_tech['High'] + df_tech['Low'] + df_tech['Close']) / 3).cumsum() / df_tech['Volume'].cumsum()

  df_tech['RiskAdjustedReturn'] = df_tech['Pct_Change'] / df_tech['Volatility']

  df_tech['IndustryRankRSI'] = df_tech['RSI'].rank(pct=True)

  df_tech['CloseToVWAPRatio'] = df_tech['Close'] / df_tech['VWAP']

  df_tech['MACDSignalDiff'] = df_tech['MACD'] - df_tech['MACD_Signal']

  df_tech['Percentage_Bandwidth'] = (df_tech['BB_Upper'] - df_tech['BB_Lower']) / df_tech['BB_Middle']

  df_tech.drop(columns=['BB_Upper', 'BB_Lower', 'BB_Middle'], inplace=True)

  df_tech = df_tech.dropna()
  return df_tech

def get_majority_label(model, df, industry):
    predictions = model.predict(df)
    predicted_indices = np.argmax(predictions, axis=1)
    most_common_prediction, count = mode(predicted_indices)
    majority_prediction = -1
    if isinstance(most_common_prediction, list):
        majority_prediction = most_common_prediction[0]
    else:
        majority_prediction = most_common_prediction
    
    json_mappings_file_path = f'{json_mapping_path}/{industry}.json'
    with open(json_mappings_file_path, 'r') as f:
        encoded_columns = json.load(f)
    
    categories = [col.split('_')[-1] for col in encoded_columns]
    predicted_label = categories[majority_prediction]
    
    return predicted_label

def extract_model_responses(text: str) -> list:
    # Pattern to match everything after "model" till it potentially hits another "user" or end of string
    pattern = r"model(.*?)(?=user|$)"
    matches = re.findall(pattern, text, flags=re.DOTALL)
    
    # Clean and return the matches
    return [match.strip() for match in matches if match.strip()]