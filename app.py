from flask_cors import CORS
from flask import Flask, request,  redirect
from flask import jsonify, render_template
import google.generativeai as genai
app = Flask(__name__)
CORS(app)
genai.configure(api_key="AIzaSyB-eHew6FQX9d1tVd-OITJ3_x2U2LJOzGE")

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

model = genai.GenerativeModel(model_name="MyPromptModelName",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

solutions = [];

@app.route('/save-solution/<solution>')
def save_solution(solution):
    solutions.append(solution);

@app.route('/solutions')
def get_solutions():
    return jsonify(solutions);

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
