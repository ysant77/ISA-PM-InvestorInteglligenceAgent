{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[{'label': 'environmental', 'score': 0.9789981245994568}]\n"
     ]
    }
   ],
   "source": [
    "from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline\n",
    "\n",
    "class EnvironmentalAnalyzer:\n",
    "    def __init__(self):\n",
    "        # Load pre-trained model and tokenizer from Hugging Face Model Hub\n",
    "        model_name = \"ESGBERT/EnvRoBERTa-environmental\"\n",
    "        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)\n",
    "        self.tokenizer = AutoTokenizer.from_pretrained(model_name, max_len=512)\n",
    "        \n",
    "        # Initialize pipeline for text classification\n",
    "        self.pipe = pipeline(\"text-classification\", model=self.model, tokenizer=self.tokenizer)\n",
    "        # If you have a GPU, you can enable it by adding the argument device=0 in the pipeline:\n",
    "        # self.pipe = pipeline(\"text-classification\", model=self.model, tokenizer=self.tokenizer, device=0)\n",
    "\n",
    "    def analyze(self, text):\n",
    "        # Use the pipeline to classify text\n",
    "        results = self.pipe(text, padding=True, truncation=True)\n",
    "        return results\n",
    "\n",
    "# Example usage:\n",
    "if __name__ == \"__main__\":\n",
    "    # Instantiate the analyzer\n",
    "    env_analyzer = EnvironmentalAnalyzer()\n",
    "    \n",
    "    # Example text to analyze\n",
    "    example_text = \"Scope 1 emissions are reported here on a like-for-like basis against the 2013 baseline and exclude emissions from additional vehicles used during repairs.\"\n",
    "    \n",
    "    # Perform analysis\n",
    "    analysis_results = env_analyzer.analyze(example_text)\n",
    "    \n",
    "    # Print results\n",
    "    print(analysis_results)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "esg",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
