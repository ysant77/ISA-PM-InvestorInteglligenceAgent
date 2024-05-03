
# SystemCode Structure

## Directory Layout
```
SystemCode/
│
├── requirements_2.txt
│
├── Frontend/
│   ├── main.py
│   ├── style.css
│   ├── Cover.jpg
│
├── Backend/
│   ├── .Neuro_Fuzzy/
│   ├── .ESG/
│   ├── Company_Scrapping.py
│   ├── GD_SentimentAnalysis.py
│   ├── .history/
│   ├── constant_api_key.py
│
└── Model_training/
    ├── Clustering.ipynb
    ├── generate_training_data_gemma.ipynb
    ├── neuro_fuzzy.ipynb
    ├── fine_tune_gemma.ipynb

```

## Brief Description
The `main.py` in the Frontend directory serves as both the main script and the webpage design. Interactions with user inputs or prompts to the chatbot trigger web scraping (`Company_Scrapping.py`, `GD_SentimentAnalysis.py`) and model inferencing (`ESG_main.py`, `gemma_inference.py`).

## Instructions on How to Run the Code

1. Navigate to the SystemCode directory:
   ```bash
   cd SystemCode/
   ```
2. Install required packages:
   ```bash
   pip install -r requirements_2.txt
   ```
3. (Optional) Set up EventRegistry and NewsApi respective tokens in `Backend/.env`:
   - [EventRegistry Setup](https://eventregistry.org/)
   - [NewsApi Registration](https://newsapi.org/register)
4. Run the application:
   ```bash
   streamlit run Frontend/main.py
   ```

## System Requirements

- **Browser**: Google Chrome
- **RAM**: Minimum of 32GB required to run the Gemma model

## Additional Resources

- **Gemma Model**: Check out the Gemma model [here](https://huggingface.co/yatharth97/yatharth-gemma-2b-it-isa-v2).
- **Dataset**: The dataset used to fine-tune the Gemma model is available [here](https://huggingface.co/datasets/yatharth97/isa_gemma).

