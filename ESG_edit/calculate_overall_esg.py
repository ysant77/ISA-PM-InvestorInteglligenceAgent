class ESGScoreCalculator:
    @staticmethod
    def calculate_weighted_score(weights, scores):
        return sum(weight * score for weight, score in zip(weights, scores))

    @staticmethod
    def calculate_overall_esg_score(environmental_score, social_score, governance_score):
        # Define the weights for each ESG component based on the three different approaches.
        backtested_weights = [0.25, 0.05, 0.70]  # Backtested Weights: Best performance - Rank 1
        equal_weights = [1/3, 1/3, 1/3]          # Equal Weights: Second-best performance - Rank 2
        industry_weights = [0.30, 0.39, 0.31]    # Industry-Specific Weights: Third-best performance - Rank 3

        # Calculate the overall ESG score for each approach.
        backtested_score = ESGScoreCalculator.calculate_weighted_score(
            backtested_weights, [environmental_score, social_score, governance_score]
        )
        equal_weight_score = ESGScoreCalculator.calculate_weighted_score(
            equal_weights, [environmental_score, social_score, governance_score]
        )
        industry_specific_score = ESGScoreCalculator.calculate_weighted_score(
            industry_weights, [environmental_score, social_score, governance_score]
        )

        # Create a dictionary to store the scores along with an explanation.
        scores = {
            'Backtested Weights Score (Rank 1 - Best Performance)': backtested_score,
            'Equal Weight Score (Rank 2 - Second Best Performance)': equal_weight_score,
            'Industry-Specific Weights Score (Rank 3 - Third Best Performance)': industry_specific_score,
        }

        # Return the dictionary containing the scores and the associated approach.
        return scores

    # # Example ESG scores for demonstration purposes.
    # environmental_score = 0.85
    # social_score = 0.65
    # governance_score = 0.75

    # # Calculate and print overall ESG scores using different approaches.
    # overall_esg_scores = ESGScoreCalculator.calculate_overall_esg_score(
    #     environmental_score, social_score, governance_score
    # )

    # # Print the scores with a description.
    # for description, score in overall_esg_scores.items():
    #     print(f"{description}: {score:.2f}")