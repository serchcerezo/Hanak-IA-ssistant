import openai
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Usar la clave API desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# Token de verificación para Meta
VERIFY_TOKEN = "HanakToken123"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    if user_message:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
            # Extrae el contenido del mensaje de la respuesta
            return jsonify({"response": response["choices"][0]["message"]["content"]})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No message provided"}), 400

# Endpoint para el webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verificación del token
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            return 'Verification failed', 403

    if request.method == 'POST':
        # Manejo de mensajes (aquí se procesarán mensajes entrantes de Meta)
        data = request.get_json()
        print(f"Received webhook data: {data}")
        return 'EVENT_RECEIVED', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
