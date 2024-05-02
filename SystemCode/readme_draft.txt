SystemCode
    - requirements_2.txt
    - Frontend
        - main.py
        - style.css
        - Cover.jpg
    - Backend
        - .Neuro_Fuzzy/
        - .ESG/
        - Company_Scrapping.py
        - GD_SentimentAnalysis.py
        - .history/
        - constant_api_key.py

Brief Description (How does it work?)
main.py serves as the main script as well as the webpage design. Toggling with \
user inputs/ feeding user prompt to the chatbot will trigger web scrapping \
(Company_Scrapping.py, GD_SentimentAnalysis.py) as well as model inferencing \
(ESG_main.py, gemma_inference.py). 


Instructions on how to run the code
1. 'cd .SystemCode/'
2. 'pip install -r requirements_2.txt'
3. (optional) set up EventRegistry (https://eventregistry.org/) and NewsApi (https://newsapi.org/register) respective tokens in Backend/.env
3. 'streamlit run Frontend/main.py'


System Challenges
- need to have chrome browser
- need to have minimum ram of 32GB to run Gemma model