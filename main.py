import argparse
import json
from src import utils as ut

from src import agents
from pathlib import Path


def main(datadir, output="results"):
    # Create output directory if it doesn't exist
    output_dir = Path(output)
    output_dir.mkdir(exist_ok=True)

    # Load the input and output data
    input_file = Path(datadir) / "input_1.txt"
    expected_output = Path(datadir) / "output_1.txt"
    expected_text = expected_output.read_text()

    if not input_file.exists():
        print(f"Error: Input file {input_file} not found")
        return

    if not expected_output.exists():
        print(f"Warning: Expected output file {expected_output} not found")

    # Load the agent
    agent = agents.QuizAgent()

    # Generate quizzes
    generated_text = agent.generate_questions(text_path=input_file, num_questions=3)

    print("Expected Output:")
    print(expected_text)
    print("\n==============\nGenerated Questions:")
    print(generated_text)

    # Compare results
    score = ut.compare_outputs(generated_text, expected_text)
    print(f"\n==============\nROUGE-1 F1 score: {score:.4f}")

    # Save results
    results = {
        "rouge_score": float(score),
        "generated_text": generated_text,
        "expected_text": expected_text,
    }

    output_file = output_dir / "pred_1.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quiz Generator")
    parser.add_argument(
        "-d",
        "--datadir",
        type=str,
        default="data",
        help="Directory containing input data",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="results",
        help="Output directory (default: results)",
    )

    args = parser.parse_args()
    main(args.datadir, args.output)
