import os
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
        'overall': "Please format the following text professionally for a resume, like get the main contents and keep it simple. ",
        'name_contact': "Please format the following name and contact details professionally for a resume: ",
        'schooling_marks': "Organize these schooling marks and CGPA in a professional resume format: ",
        'experience': "Present this experience detail in a polished and professional manner suitable for a resume: ",
        'projects': "Structure these project details in a professional format appropriate for a resume: "
    }
    
    overall_prompt = prompt_engineering.get('overall', '')
    specific_prompt = prompt_engineering.get(prompt_type, '')
    formatted_prompt = overall_prompt + specific_prompt + prompt
    # print(f"Formatted Prompt: {formatted_prompt}")

    return formatted_prompt

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
    return jsonify({"response": response_text})

@app.route('/process_schooling_marks', methods=['POST'])
def process_schooling_marks():
    data = request.json

    # Debugging line to print the received data
    # print(f"Received data: {data}")

    prompt = data.get('schooling_marks')
    if not prompt:
        return jsonify({"error": "Missing 'schooling_marks' field"}), 400

    response_text = generate_response(prompt, 'schooling_marks')
    return jsonify({"response": response_text})

@app.route('/process_experience', methods=['POST'])
def process_experience():
    data = request.json
    prompt = data.get('experience')
    if not prompt:
        return jsonify({"error": "Missing 'experience' field"}), 400

    response_text = generate_response(prompt, 'experience')
    return jsonify({"response": response_text})

@app.route('/process_projects', methods=['POST'])
def process_projects():
    data = request.json
    prompt = data.get('projects')
    if not prompt:
        return jsonify({"error": "Missing 'projects' field"}), 400

    response_text = generate_response(prompt, 'projects')
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
