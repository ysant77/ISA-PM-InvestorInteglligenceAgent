import torch
from transformers import AutoModelForCausalLM, AutoTokenizer#, BitsAndBytesConfig, AutoConfig
import pandas as pd

from constants import modelName, base_dir
from utils import extract_model_responses
from neuro_fuzzy_inference import get_prediction_label

import os
import ast

# bnbConfig = BitsAndBytesConfig(
#     load_in_4bit = True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_compute_dtype=torch.bfloat16,
# )

model = AutoModelForCausalLM.from_pretrained(
    modelName
    #quantization_config=bnbConfig
)

model.eval() 

tokenizer = AutoTokenizer.from_pretrained(modelName)

system_prompt = """
As a highly intelligent assistant and successor of google gemma model, your primary goal is to provide accurate, relevant, and context-aware responses to
user queries based on the provided information. Ensure your answers are factual, free from bias, and avoid promoting violence, hate speech, or any form
of discrimination. Focus on assisting the user effectively and safely. Also do not include user's query in response again
"""

def get_completion(query: str, model, tokenizer) -> str:
  device = torch.device("cpu")  # Set device to CPU

  prompt_template = """
  <start_of_turn>user
  {system_prompt}
  {query}
  <end_of_turn>\n<start_of_turn>model
  """
  prompt = prompt_template.format(system_prompt=system_prompt, query=query)

  encodeds = tokenizer(prompt, return_tensors="pt", add_special_tokens=True)
  model_inputs = encodeds.to(device)

  generated_ids = model.generate(**model_inputs, early_stopping=True, max_new_tokens=400, do_sample=False, pad_token_id=tokenizer.eos_token_id)
  decoded = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
  model_response = decoded.split("<start_of_turn>model\n\n")[-1].strip()

  return model_response

# user_input = "What are the risks of investing in Apple's stock?"#str(input('Enter your query '))

def get_from_scraped_info(company_name, base_dir=base_dir):
  try:
    # print(os.path.join(base_dir, f'{company_name}_info.csv'))
    company_info_df = pd.read_csv(os.path.join(base_dir, f'{company_name}_info.csv'), header=None)
    company_info = tuple(company_info_df[0])

    (
        live_price, stock_market, ticker, currency, prev_close, open_price, trade_daily_volume, day_price_range, \
        day_low, day_high, market_cap, pe_ratio_ttm, eps_ttm, company_name_full, company_industry, employee_count, \
        fwd_ann_div_rate, fwd_ann_div_yield, trail_ann_div_rate, trail_ann_div_yield, company_description, \
        roe, roa, net_profit_margin, p_s_ratio_ttm, d_e_ratio, current_ratio, p_b_ratio, key_personnel, \
        ticker_yf
    )= company_info

    response = f"""
    Current Live Stock Price: {float(live_price):.2f} {currency}\n
    Open Market Stock Price: {open_price} {currency}\n
    Previous Day Close Price: {prev_close} {currency}\n
    Trade Daily Volume: { (float(trade_daily_volume.replace(',','')) / 1e6):.2f} M\n
    Market Capacity: {market_cap}\n
    PE Ratio (TTM): {pe_ratio_ttm}\n
    Earnings Per Share (TTM): {eps_ttm}\n
    Forward Annual Dividend Rate: {fwd_ann_div_rate}\n
    Forward Annual Dividend Yield: {fwd_ann_div_yield}\n
    Trailing Annual Dividend Rate: {trail_ann_div_rate}\n
    Trailing Annual Dividend Yield: {trail_ann_div_yield}\n
    Return on Equity: {roe}\n
    Return on Assets: {roa}\n
    Profit Margin: {net_profit_margin}\n
    Price/ Sales Ratio (TTM): {p_s_ratio_ttm}\n
    Total Debt/ Equity Ratio: {d_e_ratio}\n
    Current Ratio: {current_ratio}\n
    Price/ Book Ratio: {p_b_ratio}\n
    """

    return response

  except:
    print(f'check if file exists...')

    return 'Please scrape for this company\'s data first. Else check if file exists first.'


def get_from_scraped_review(company_name, home_dir):
  try:
    # print(os.path.join(home_dir, f'{company_name}_glassdoor_scrape.csv'))
    glassdoor_df = pd.read_csv(os.path.join(home_dir, f'{company_name}_glassdoor_scrape.csv'), header=None)
    company_rating, job_recommendation, ceo_approval, pros_header, pros_description, cons_header, cons_description, comp_rating, comp_job_rec, comp_ceo_approval, top_competitors, company_rating_rank, company_job_rec_rank, company_ceo_app_rank = glassdoor_df[0]

    pros_desc_str = ''
    for i in ast.literal_eval(pros_description):
      pros_desc_str += "- " + i + "\n"
    cons_desc_str = ''
    for i in ast.literal_eval(cons_description):
      cons_desc_str += "- " + i + "\n"

    response=f"""
    Company\'s Rating (based on employees): {company_rating} out of 5.0\n
    Likelihood of recommendation of company: {job_recommendation}\n
    Employees\' Approval of CEO: {ceo_approval}\n

    Employees praised that:\n
    {pros_desc_str}

    But employees also complained that:\n
    {cons_desc_str}
    """

    return response
  except:
    print(f'check if file exists...')

    return 'Please scrape for this company\'s data first. Else check if file exists first.'


def get_from_scraped_competitors(company_name, home_dir):
  try:
    print(os.path.join(home_dir, f'{company_name}_glassdoor_scrape.csv'))
    glassdoor_df = pd.read_csv(os.path.join(home_dir, f'{company_name}_glassdoor_scrape.csv'), header=None)
    company_rating, job_recommendation, ceo_approval, pros_header, pros_description, cons_header, cons_description, comp_rating, comp_job_rec, comp_ceo_approval, top_competitors, company_rating_rank, company_job_rec_rank, company_ceo_app_rank = glassdoor_df[0]
    top_competitors = ast.literal_eval(top_competitors)
    n = len(top_competitors)

    response=f"""
    Top {n} competitors assessed are: {top_competitors[0]}, {top_competitors[1]}, {top_competitors[2]}\n
    Company's ratings ranks {company_rating_rank} out of {n+1}\n
    Company's job recommendation rating ranks {company_job_rec_rank} out of {n+1}\n
    Company's ceo approval rating ranks {company_ceo_app_rank} out of {n+1}\n
    """
    return response
  except:
    print(f'check if file exists...')

    return 'Please scrape for this company\'s data first. Else check if file exists first.'


def get_from_scraped_news(company_name, home_dir):
  try:
    # print(os.path.join(home_dir, f'collated_news/{company_name}_news.csv'))
    company_news_df = pd.read_csv(os.path.join(home_dir, f'collated_news/{company_name}_news.csv'))

    # company_str = ''
    # for index, row in company_news_df[:5].iterrows():
    #   company_str += f'Caption of news: {row["Title"]}\nFrom: {row["Date"]}\nSummary includes: {row["Summary"]}\n'

    # chose to hardcode since styling is not good
    response=f"""
    Some news include:\n\n
    Caption of news: {company_news_df.iloc[0]["Title"]}\n
    From: {company_news_df.iloc[0]["Date"]}\n
    Summary includes: {company_news_df.iloc[0]["Summary"]}\n\n
    Caption of news: {company_news_df.iloc[1]["Title"]}\n
    From: {company_news_df.iloc[1]["Date"]}\n
    Summary includes: {company_news_df.iloc[1]["Summary"]}\n\n
    Caption of news: {company_news_df.iloc[2]["Title"]}\n
    From: {company_news_df.iloc[2]["Date"]}\n
    Summary includes: {company_news_df.iloc[2]["Summary"]}\n\n
    Caption of news: {company_news_df.iloc[3]["Title"]}\n
    From: {company_news_df.iloc[3]["Date"]}\n
    Summary includes: {company_news_df.iloc[3]["Summary"]}\n\n
    Caption of news: {company_news_df.iloc[4]["Title"]}\n
    From: {company_news_df.iloc[4]["Date"]}\n
    Summary includes: {company_news_df.iloc[4]["Summary"]}
    """

    return response
  except:
    print(f'check if file exists...')

    return 'Please scrape for this company\'s data first. Else check if file exists first.'


def get_esg(company_name, home_dir):
  try:
    esg_stats_df = pd.read_csv(os.path.join(home_dir, f'{company_name}_esg_stats.csv'))

    response=f"""
    ESG Statistics:\n\n
    Environmental Score: {esg_stats_df['E_score'].item()}\n
    Social Score: {esg_stats_df['S_score'].item()}\n
    Governmental Score: {esg_stats_df['G_score'].item()}\n
    Backtested Weights Score (Rank 1 - Best Performance): {esg_stats_df['Backtested Weights Score (Rank 1 - Best Performance)'].item()}\n
    Equal Weight Score (Rank 2 - Second Best Performance): {esg_stats_df['Equal Weight Score (Rank 2 - Second Best Performance)'].item()}\n
    Industry-Specific Weights Score (Rank 3 - Third Best Performance): {esg_stats_df['Industry-Specific Weights Score (Rank 3 - Third Best Performance)'].item()}
    """

    return response
  except:
    print(f'check if file exists...')

    return 'Please scrape for this company\'s data first. Else check if file exists first.'


def gemma_respond(user_input):
  model_output = get_completion(user_input, model, tokenizer)

  responses = extract_model_responses(model_output)
  output = [res.strip() for res in responses if res.startswith("model")]
  output = [ele.replace("model", "").strip() for ele in output]
  response = output[0]
  query_args = response.strip().split(':')

  print(f'query_args: {query_args}')
  try: # stock info
    query_type, company, duration = query_args
    print(query_type, company, duration)
  except: # the stock_risk, employee_reviews, competitors
    query_type, company = query_args
    print(query_type, company)
  else: # only news
    _, _, query_type, company = query_args
    print(query_type, company)


  base_dir_2 = os.path.join(base_dir, 'scraped_data')
  print(base_dir_2)
  if query_type == 'stock_risk':
    label = get_prediction_label(company.strip())
  elif query_type == 'stock_info':
    label = get_from_scraped_info(company.strip(), base_dir_2)
  elif query_type == 'employee_reviews':
    label = get_from_scraped_review(company.strip(), base_dir_2)
  elif query_type == 'competitors':
    label = get_from_scraped_competitors(company.strip(), base_dir_2)
  elif query_type == 'latest_news':
    label = get_from_scraped_news(company.strip(), base_dir_2)
  elif query_type == 'esg_ratings':
    label = get_esg(company.strip(), base_dir_2)



  print(label)
  return label




# gemma_respond(user_input)