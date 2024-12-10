import random
from typing import List, Dict, Optional


class QuizAgent:
    def __init__(self):
        self.questions = []

    def generate_questions(self, text_path: str, num_questions: int = 4) -> List[Dict]:
        """
        Generates multiple choice questions from a text file.

        Args:
            text_path (str): Path to the text file
            num_questions (int): Number of questions to generate (default: 4)

        Returns:
            List[Dict]: List of dictionaries containing questions, options, and correct answers
        """
        # Read the text file
        with open(text_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Generate questions (this is a simple implementation - you might want to use
        # more sophisticated NLP techniques in a production environment)
        sentences = [s.strip() for s in text.split(".") if s.strip()]

        quiz_questions = []
        for _ in range(min(num_questions, len(sentences))):
            # Select a random sentence for the question
            sentence = random.choice(sentences)
            sentences.remove(sentence)  # Avoid duplicate questions

            # Create a question by removing a key word
            words = sentence.split()
            target_word = random.choice([w for w in words if len(w) > 3])
            question = sentence.replace(target_word, "_____")

            # Generate incorrect options
            all_words = [w for w in text.split() if len(w) > 3]
            wrong_options = random.sample([w for w in all_words if w != target_word], 3)

            # Create options and shuffle them
            options = wrong_options + [target_word]
            random.shuffle(options)

            # Create question dictionary
            quiz_question = {
                "question": question,
                "options": options,
                "correct_answer": target_word,
            }

            quiz_questions.append(quiz_question)
        # Format the questions as a string
        return self.format_quiz(quiz_questions)

    def format_quiz(self, questions: List[Dict]) -> str:
        """
        Formats the quiz questions into a readable string.
        """
        formatted_quiz = ""
        for i, q in enumerate(questions):
            formatted_quiz += f"Question {i}: {q['question']}\n"
            for j, option in enumerate(q["options"]):
                formatted_quiz += f"{chr(97 + j)}) {option}\n"
            formatted_quiz += f"\nCorrect answer: {q['correct_answer']}\n\n"
        return formatted_quiz

    def generate_questions_with_openai(
        self, text_path: str, num_questions: int = 4, api_key: Optional[str] = None
    ) -> List[Dict]:
        import openai

        """
        Generates multiple choice questions using OpenAI's API.

        Args:
            text_path (str): Path to the text file
            num_questions (int): Number of questions to generate (default: 4)
            api_key (Optional[str]): OpenAI API key. If None, uses environment variable.

        Returns:
            List[Dict]: List of dictionaries containing questions, options, and correct answers
        """
        # Set up OpenAI client
        if api_key:
            openai.api_key = api_key

        # Read the text file
        with open(text_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Create the prompt for OpenAI
        prompt = f"""
        Create {num_questions} multiple choice questions based on this text:
        {text}

        Format each question as a JSON object with these fields:
        - question: the question text
        - options: array of 4 possible answers
        - correct_answer: the correct answer (must be one of the options)

        Return only a JSON array of these question objects.
        """

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that creates quiz questions.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            # Parse the response
            import json

            questions = json.loads(response.choices[0].message.content)

            return questions

        except Exception as e:
            print(f"Error generating questions with OpenAI: {e}")
            return []


if __name__ == "__main__":
    import os
    from pathlib import Path

    # Test file path - create a sample text file
    test_text = """
    The Python programming language was created by Guido van Rossum.
    Python is known for its simple and readable syntax.
    The language was named after Monty Python's Flying Circus.
    Python supports multiple programming paradigms including procedural, object-oriented, and functional programming.
    """

    test_file = Path("test_text.txt")
    test_file.write_text(test_text)

    # Create quiz agent
    agent = QuizAgent()

    print("=== Testing basic question generation ===")
    questions = agent.generate_questions(test_file)
    print(questions)

    print("\n=== Testing OpenAI question generation ===")
    # Only run OpenAI test if API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        ai_questions = agent.generate_questions_with_openai(test_file)
        print(ai_questions)
    else:
        print("Skipping OpenAI test - no API key found in environment variables")

    # Clean up test file
    test_file.unlink()
