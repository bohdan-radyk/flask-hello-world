from flask_cors import CORS
from flask import Flask, jsonify, render_template, request
import google.generativeai as genai
app = Flask(__name__)
CORS(app)

SCOPES = ['https://www.googleapis.com/auth/generative-language.retriever']

from google.oauth2.credentials import Credentials
creds = Credentials.from_authorized_user_file('/etc/secrets/token.json', SCOPES)
genai.configure(credentials=creds)
print('Available base models:', [m.name for m in genai.list_models()])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="tunedModels/newmodel-bdt8syh85744",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


messages = []

@app.route('/askQuestion', methods=['POST'])
def ask_question():
    message = request.get_json()
    response_text = process_message(message)
    return jsonify({'response': response_text}), 200

def process_message(message):
    response = model.generate_content(message)
    return response.text
@app.route('/saveMessage', methods=['POST'])
def save_message():
    message = request.get_json()
    messages.append(message)
    return 'Message saved successfully', 200

@app.route('/getMessages', methods=['GET'])
def get_messages():
    return jsonify(messages), 200

@app.route('/deleteMessage', methods=['POST'])
def delete_message():
    data = request.get_json()
    index = data.get('index')
    if index is not None and 0 <= index < len(messages):
        messages.pop(index)
        return 'Message removed successfully', 200
    return 'Invalid index', 400

@app.route('/<prompt>')
def genai_prompt(prompt):
    response = model.generate_content(prompt)
    print(response.text)
    return jsonify(response.text);

@app.route('/')
def hello_world():
    return render_template("home.html")


if __name__ == "__main__":
    app.run();
