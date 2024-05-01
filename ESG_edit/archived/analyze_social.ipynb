{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "c:\\Users\\ganji\\esg\\Lib\\site-packages\\tqdm\\auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html\n",
      "  from .autonotebook import tqdm as notebook_tqdm\n",
      "c:\\Users\\ganji\\esg\\Lib\\site-packages\\huggingface_hub\\file_download.py:148: UserWarning: `huggingface_hub` cache-system uses symlinks by default to efficiently store duplicated files but your machine does not support them in C:\\Users\\ganji\\.cache\\huggingface\\hub\\models--ESGBERT--SocialBERT-social. Caching files will still work but in a degraded version that might require more space on your disk. This warning can be disabled by setting the `HF_HUB_DISABLE_SYMLINKS_WARNING` environment variable. For more details, see https://huggingface.co/docs/huggingface_hub/how-to-cache#limitations.\n",
      "To support symlinks on Windows, you either need to activate Developer Mode or to run Python as an administrator. In order to see activate developer mode, see this article: https://docs.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development\n",
      "  warnings.warn(message)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[{'label': 'social', 'score': 0.9998106360435486}]\n"
     ]
    }
   ],
   "source": [
    "from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline\n",
    "\n",
    "class SocialAnalyzer:\n",
    "    def __init__(self):\n",
    "        model_name = \"ESGBERT/SocialBERT-social\"\n",
    "        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)\n",
    "        self.tokenizer = AutoTokenizer.from_pretrained(model_name, max_len=512)\n",
    "        self.pipe = pipeline(\"text-classification\", model=self.model, tokenizer=self.tokenizer)\n",
    "\n",
    "    def analyze(self, text):\n",
    "        results = self.pipe(text, padding=True, truncation=True)\n",
    "        return results\n",
    "\n",
    "# Example usage\n",
    "if __name__ == \"__main__\":\n",
    "    social_analyzer = SocialAnalyzer()\n",
    "    example_text = \"The company has a strong commitment to improving working conditions and ensuring equal opportunities for all employees.\"\n",
    "    analysis_results = social_analyzer.analyze(example_text)\n",
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
