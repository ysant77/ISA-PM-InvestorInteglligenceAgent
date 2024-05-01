from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

class EnvironmentalAnalyzer:
    def __init__(self):
        # Load pre-trained model and tokenizer from Hugging Face Model Hub
        model_name = "ESGBERT/EnvRoBERTa-environmental"
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, max_len=512)
        
        # Initialize pipeline for text classification
        self.pipe = pipeline(task="text-classification", model=self.model, tokenizer=self.tokenizer)
        # If you have a GPU, you can enable it by adding the argument device=0 in the pipeline:
        # self.pipe = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer, device=0)

    def analyze(self, text):
        # Use the pipeline to classify text
        # print(f'text:{text}')
        results = self.pipe(text, padding=True, truncation=True)
        return results

    # env_analyzer = EnvironmentalAnalyzer()
    # example_text = "Scope 1 emissions are reported here on a like-for-like basis against the 2013 baseline and exclude emissions from additional vehicles used during repairs."
    # analysis_results = env_analyzer.analyze(example_text)
    # print(analysis_results)


class SocialAnalyzer:
    def __init__(self):
        model_name = "ESGBERT/SocialBERT-social"
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, max_len=512)
        self.pipe = pipeline(task="text-classification", model=self.model, tokenizer=self.tokenizer)

    def analyze(self, text):
        results = self.pipe(text, padding=True, truncation=True)
        return results

#     social_analyzer = SocialAnalyzer()
    # example_text = "The company has a strong commitment to improving working conditions and ensuring equal opportunities for all employees."
    # analysis_results = social_analyzer.analyze(example_text)
    # print(analysis_results)


class GovernanceAnalyzer:
    def __init__(self):
        model_name = "ESGBERT/GovRoBERTa-governance"
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, max_len=512)
        self.pipe = pipeline(task="text-classification", model=self.model, tokenizer=self.tokenizer)

    def analyze(self, text):
        results = self.pipe(text, padding=True, truncation=True)
        return results


    # governance_analyzer = GovernanceAnalyzer()
    # example_text = "The board of directors has approved a new policy to enhance transparency and combat corruption."
    # analysis_results = governance_analyzer.analyze(example_text)
    # print(analysis_results)