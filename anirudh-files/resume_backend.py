import os, json
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Set up your API key securely
API_KEY = 'AIzaSyC_iJ_seRtx_OtEJO6rKYuuyOv8HrcQmvo'

# Configure the Generative AI client
genai.configure(api_key=API_KEY)

# Initialize the Generative Model
config = {
    'temperature': 0,
    'top_k': 20,
    'top_p': 0.9,
    'max_output_tokens': 500
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
    }
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=config,
    safety_settings=safety_settings
)

def format_prompt(prompt, prompt_type):
    """Format the prompt based on the type of input to ensure professional responses."""
    prompt_engineering = {
    'overall': "Please read the input carefully and format the following text professionally for a resume. Extract the main contents, keep the formatting simple, and structure the response as a clean JSON object without any additional labels or escape sequences. and remove '''json ''' and all dont give it in the response",
    'name_contact': "Please format the following name and contact details professionally for a resume. Structure it clearly as a clean JSON object, without any additional labels or escape sequences:",
    'schooling_marks': "Please organize the following education details level-wise, starting with school and then college. Include CGPAs and percentiles where applicable, and format them professionally for a resume. Return the response as a clean JSON object, without any additional labels or escape sequences:",
    'experience': "Present the following experience details in a polished and professional manner suitable for a resume. Structure it as a clean JSON object, without any additional labels or escape sequences:",
    'projects': "Please structure the following project details in a professional and easy-to-read format appropriate for a resume. Return the response as a clean JSON object, without any additional labels or escape sequences:",
    'publications': "Please organize and format the following publication details in a professional manner suitable for a resume. Structure the response as a clean JSON object, without any additional labels or escape sequences:",
    'certificates': "Please structure the following certificate details in a professional and polished format suitable for a resume. Ensure clarity and return the response as a clean JSON object, without any additional labels or escape sequences:",
    'description': "Creatively express the individual's name and summarize their professional persona using the available data. Make it engaging and suitable for a personal description section in a resume. Structure the response as a clean JSON object, without any additional labels or escape sequences:",
    }

    
    overall_prompt = prompt_engineering.get('overall', '')
    specific_prompt = prompt_engineering.get(prompt_type, '')
    formatted_prompt = overall_prompt + specific_prompt + prompt

    return formatted_prompt

def preprocess(response_text):
    try:
        response_json = json.loads(response_text)
        # print(response_json)
        return response_json
    except json.JSONDecodeError:
        print("Error decoding JSON. The input text might be improperly formatted.")
        return None
    
    
def generate_response(prompt, prompt_type):
    """Generate a response from the model with additional formatting instructions."""
    formatted_prompt = format_prompt(prompt, prompt_type)

    # print(f"Sending to model: {formatted_prompt}")

    response = model.generate_content(formatted_prompt)

    # print(f"Model Response: {response.text}")

    return response.text

@app.route('/process_name_contact', methods=['POST'])
def process_name_contact():
    data = request.json
    prompt = data.get('name_contact')
    if not prompt:
        return jsonify({"error": "Missing 'name_contact' field"}), 400

    response_text = generate_response(prompt, 'name_contact')
    response_text = preprocess(response_text)
    # print(response_text)
    return jsonify({"response": response_text})

@app.route('/process_schooling_marks', methods=['POST'])
def process_schooling_marks():
    data = request.json

    # print(f"Received data: {data}")

    prompt = data.get('schooling_marks')
    if not prompt:
        return jsonify({"error": "Missing 'schooling_marks' field"}), 400

    response_text = generate_response(prompt, 'schooling_marks')
    response_text = preprocess(response_text)
    return jsonify({"response": response_text})

@app.route('/process_experience', methods=['POST'])
def process_experience():
    data = request.json
    prompt = data.get('experience')
    if not prompt:
        return jsonify({"error": "Missing 'experience' field"}), 400

    response_text = generate_response(prompt, 'experience')
    response_text = preprocess(response_text)
    return jsonify({"response": response_text})

@app.route('/process_projects', methods=['POST'])
def process_projects():
    data = request.json
    prompt = data.get('projects')
    if not prompt:
        return jsonify({"error": "Missing 'projects' field"}), 400

    response_text = generate_response(prompt, 'projects')
    response_text = preprocess(response_text)
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
