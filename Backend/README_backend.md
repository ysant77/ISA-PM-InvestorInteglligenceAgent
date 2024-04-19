gemma_inference.py:

1. This file integrates the Gemma-2B LLM to the system. Right now only integration with neuro fuzzy model is completed.
2. For more information on the dataset used for fine tuning and how to integrate with rest of system, this dataset can be referred to: yatharth97/isa_gemma
3. Brief note on dataset/model responses:
  stock_info:Boeing:6m, summarizes the stock info for a company Boeing for 6months
  latest_news:Boeing, gets the latest news for Boeing
  stock_risk:Boeing, integrates with neuro fuzzy model
  esg_ratings:Boeing, integrates with esg rating computation for Boeing
  employee_reviews:Boeing, gets the employee reviews for Boeing
  competitors:Boeing, gets competitor information for Boeing
