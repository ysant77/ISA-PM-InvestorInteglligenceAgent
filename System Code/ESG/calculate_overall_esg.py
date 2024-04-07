{
 "cells": [
  {
   "cell_type": "code",
"execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "class ESGScoreCalculator:\n",
    "    @staticmethod\n",
    "    def calculate_weighted_score(weights, scores):\n",
    "        return sum(weight * score for weight, score in zip(weights, scores))\n",
    "\n",
    "    @staticmethod\n",
    "    def calculate_overall_esg_score(environmental_score, social_score, governance_score):\n",
    "        # Define the weights for each ESG component based on the three different approaches.\n",
    "        backtested_weights = [0.25, 0.05, 0.70]  # Backtested Weights: Best performance - Rank 1\n",
    "        equal_weights = [1/3, 1/3, 1/3]          # Equal Weights: Second-best performance - Rank 2\n",
    "        industry_weights = [0.30, 0.39, 0.31]    # Industry-Specific Weights: Third-best performance - Rank 3\n",
    "\n",
    "        # Calculate the overall ESG score for each approach.\n",
    "        backtested_score = ESGScoreCalculator.calculate_weighted_score(\n",
    "            backtested_weights, [environmental_score, social_score, governance_score]\n",
    "        )\n",
    "        equal_weight_score = ESGScoreCalculator.calculate_weighted_score(\n",
    "            equal_weights, [environmental_score, social_score, governance_score]\n",
    "        )\n",
    "        industry_specific_score = ESGScoreCalculator.calculate_weighted_score(\n",
    "            industry_weights, [environmental_score, social_score, governance_score]\n",
    "        )\n",
    "\n",
    "        # Create a dictionary to store the scores along with an explanation.\n",
    "        scores = {\n",
    "            'Backtested Weights Score (Rank 1 - Best Performance)': backtested_score,\n",
    "            'Equal Weight Score (Rank 2 - Second Best Performance)': equal_weight_score,\n",
    "            'Industry-Specific Weights Score (Rank 3 - Third Best Performance)': industry_specific_score,\n",
    "        }\n",
    "\n",
    "        # Return the dictionary containing the scores and the associated approach.\n",
    "        return scores\n",
    "\n",
    "# Example usage:\n",
    "if __name__ == \"__main__\":\n",
    "    # Example ESG scores for demonstration purposes.\n",
    "    environmental_score = 0.85\n",
    "    social_score = 0.65\n",
    "    governance_score = 0.75\n",
    "\n",
    "    # Calculate and print overall ESG scores using different approaches.\n",
    "    overall_esg_scores = ESGScoreCalculator.calculate_overall_esg_score(\n",
    "        environmental_score, social_score, governance_score\n",
    "    )\n",
    "\n",
    "    # Print the scores with a description.\n",
    "    for description, score in overall_esg_scores.items():\n",
    "        print(f\"{description}: {score:.2f}\")\n"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
