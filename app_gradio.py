import gradio as gr
import os
from openai import OpenAI


def initialize_openai_client(api_key):
    return OpenAI(api_key=api_key)


def estimate_duration(items, api_key):
    if not api_key.strip():
        return "Please provide an OpenAI API key"

    client = initialize_openai_client(api_key)

    # Updated prompt to request justification
    prompt = """For each of the following action items:
    1. Estimate how long it would take to complete
    2. Add a brief one-line justification
    3. Format each line as: "Original task (Time estimate) - Justification"
    Be concise and realistic with estimates.
    
    Action items:
    {}""".format(
        "\n".join(items)
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides realistic task duration estimates with brief justifications.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        # Extract and process the response
        estimated_items = response.choices[0].message.content.strip().split("\n")
        # Remove any empty lines and leading/trailing whitespace
        estimated_items = [item.strip() for item in estimated_items if item.strip()]
        # Sort alphabetically
        sorted_items = sorted(estimated_items)

        return "\n".join(sorted_items)

    except Exception as e:
        return f"Error: {str(e)}"


def process_items(input_text, api_key):
    # Split the input text into lines and remove empty lines
    items = [line.strip() for line in input_text.split("\n") if line.strip()]

    if not items:
        return "Please enter some action items"

    return estimate_duration(items, api_key)


# Create the Gradio interface
demo = gr.Interface(
    fn=process_items,
    inputs=[
        gr.Textbox(
            lines=10,
            placeholder="""Enter your action items (one per line):
1. Buy groceries
2. Call dentist
3. Answer emails""",
        ),
        gr.Textbox(
            type="password",
            label="OpenAI API Key",
            placeholder="Enter your OpenAI API key",
        ),
    ],
    outputs=gr.Textbox(
        lines=10, label="Sorted Items with Time Estimates and Justifications"
    ),
    title="Action Item Duration Estimator",
    description="Enter your action items (one per line) and they will be sorted alphabetically with estimated durations and justifications.",
)

if __name__ == "__main__":
    demo.launch()
