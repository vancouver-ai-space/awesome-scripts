from rouge_score import rouge_scorer


def compare_outputs(generated_text, expected_text):
    """Compare generated output with expected output using ROUGE-1 overlap count"""

    # Initialize ROUGE scorer with only rouge1
    scorer = rouge_scorer.RougeScorer(["rouge1"], use_stemmer=True)

    # Calculate ROUGE scores
    scores = scorer.score(expected_text, generated_text)

    # Return the F1 score for ROUGE-1
    return scores["rouge1"].fmeasure
