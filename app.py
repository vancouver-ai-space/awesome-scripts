from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key="")


@app.route("/")
def home():
    return app.send_static_file("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    user_info = request.json["userInfo"]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a well-being assistant. Always respond with exactly 3 bullet points. Keep each point concise and practical.
                    User Information:
                    - Age: {user_info['age']}
                    - Location: {user_info['location']}
                    - Occupation: {user_info['occupation']}
                    
                    Tailor your responses considering this user context.""",
                },
                {"role": "user", "content": user_message},
            ],
        )

        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
