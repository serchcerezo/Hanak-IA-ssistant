import openai
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Usar la clave API de una variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    if user_message:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        return jsonify(response['choices'][0]['message']['content'])
    return jsonify({"error": "No message provided"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
