from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

 # Put your API key here or use an environment variable

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    headers = {
        "Authorization": f"Bearer",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    print(response.status_code, response.text)  # <--- Add this line
    if response.status_code == 200:
        result = response.json()
        return jsonify({'response': result['choices'][0]['message']['content']})
    else:
        return jsonify({'error': 'OpenAI API error', 'details': response.text}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)