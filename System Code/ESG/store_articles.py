import json
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "\n",
    "class ArticleStore:\n",
    "    @staticmethod\n",
    "    def save_articles_to_file(articles, filename):\n",
    "        with open(filename, 'w', encoding='utf-8') as f:\n",
    "            json.dump(articles, f, ensure_ascii=False, indent=4)\n",
    "\n",
    "    @staticmethod\n",
    "    def load_articles_from_file(filename):\n",
    "        if os.path.exists(filename):\n",
    "            with open(filename, 'r', encoding='utf-8') as f:\n",
    "                articles = json.load(f)\n",
    "                return articles\n",
    "        return []"
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
