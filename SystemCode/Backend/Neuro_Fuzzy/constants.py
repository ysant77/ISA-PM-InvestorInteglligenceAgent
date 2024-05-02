import os

base_dir = os.getcwd() + '/Neuro_Fuzzy'
# base_dir = os.getcwd()
models_dir = f'{base_dir}/models'
db_path = f'{base_dir}/stock_data.db'
json_mapping_path = f'{base_dir}/json_mappings'

selected_industries = ['Banks—Regional', 'Software—Application', 'Software—Infrastructure', 'Information Technology Services',
                       'Capital Markets', 'Internet Content & Information', 'Electronic Components', 'Consumer Electronics',
                       'Entertainment', 'Medical Devices']

cols_to_select = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends',
       'Price_Range', 'Pct_Change', 'SMA_7', 'EMA_7', 'Volatility', 'RSI',
       'MACD', 'MACD_Signal', 'VWAP', 'RiskAdjustedReturn', 'IndustryRankRSI',
       'CloseToVWAPRatio', 'MACDSignalDiff', 'Percentage_Bandwidth']
modelName = "yatharth97/yatharth-gemma-2b-it-isa-v2"
