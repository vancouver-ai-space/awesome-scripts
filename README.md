# Project Template

## Quick Start

## Setup

```bash
pip install -r requirements.txt
```

## Run

```python
python main.py -d data/ -o results/
```

```python
python app.py
```

```python
python app_gradio.py
```


## Overview for the quiz generation

This project is a simple implementation of a quiz generation system using a language model. The system takes an input text and generates a quiz based on the text. The quiz is then compared to an expected output to evaluate the performance of the system.

## 1. Input Data Used

The input data is a text file containing the text to be used for the quiz generation. The text is a Wikipedia article about Santa Claus.

## 2. Output Data

The output data is a JSON file containing the generated quiz, the expected output, and the ROUGE-1 F1 score.

## 3. Models Used

- OpenAI GPT-4o
- OpenAI GPT-4o-mini

## 4. Evaluation Method

The ROUGE-1 F1 score is used to evaluate the performance of the system. The score is calculated by comparing the generated quiz to the expected output.
