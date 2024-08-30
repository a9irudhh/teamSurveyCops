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
        'overall': "Please read the input carefully and format the following text professionally for a resume. Extract the main contents and keep the formatting simple. The input will include other prompts specifying which field it corresponds to, such as 'description,' 'experience,' etc. Return the output in a proper JSON format to facilitate front-end integration.",
        'name_contact': "Please format the following name and contact details professionally for a resume. Structure it clearly and return it in a proper JSON format for front-end use: ",
        'schooling_marks': "Please organize the following education details level-wise, starting with school and then college. Include CGPAs and percentiles where applicable, and format them professionally for a resume. Return the output in a proper JSON format for front-end use: ",
        'experience': "Present the following experience details in a polished and professional manner suitable for a resume. Ensure clarity and proper structuring, and return it in a proper JSON format for front-end use: ",
        'projects': "Please structure the following project details in a professional and easy-to-read format appropriate for a resume. Beautify the content for better readability and return it in a proper JSON format for front-end use: ",
        'publications': "Please organize and format the following publication details in a professional manner suitable for a resume. Ensure clarity and proper structuring, and return it in a proper JSON format for front-end use: ",
        'certificates': "Please structure the following certificate details in a professional and polished format suitable for a resume. Ensure clarity and return it in a proper JSON format for front-end use: ",
        'description': "Creatively express the individual's name and summarize their professional persona using the available data. Make it engaging and suitable for a personal description section in a resume. Return the output in a proper JSON format for front-end use: ",
    }
    
    overall_prompt = prompt_engineering.get('overall', '')
    specific_prompt = prompt_engineering.get(prompt_type, '')
    formatted_prompt = overall_prompt + specific_prompt + prompt
    return formatted_prompt




# def generate_response(prompt, prompt_type):
#     """Generate a response from the model with additional formatting instructions."""
#     formatted_prompt = format_prompt(prompt, prompt_type)

#     # print(f"Sending to model: {formatted_prompt}")

#     response = model.generate_content(formatted_prompt)

#     # print(f"Model Response: {response.text}")

#     return response.text

import json

def generate_response(prompt, prompt_type):
    """Generate a response from the model with additional formatting instructions."""
    formatted_prompt = format_prompt(prompt, prompt_type)

    response = model.generate_content(formatted_prompt)
    
    # Parse the model's response as JSON
    try:
        # Assuming the response is wrapped in a code block, we need to extract the JSON part
        response_text = response.text.strip("```json\n").strip("```").strip()
        response_json = json.loads(response_text)
    except (json.JSONDecodeError, AttributeError):
        return {"error": "Failed to parse the model's response as JSON"}

    return response_json



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

@app.route('/process_publications', methods=['POST'])
def process_publications():
    data = request.json
    prompt = data.get('publications')
    if not prompt:
        return jsonify({"error": "Missing 'publications' field"}), 400

    response_text = generate_response(prompt, 'publications')
    return jsonify({"response": response_text})

@app.route('/process_certificates', methods=['POST'])
def process_certificates():
    data = request.json
    prompt = data.get('certificates')
    if not prompt:
        return jsonify({"error": "Missing 'certificates' field"}), 400

    response_text = generate_response(prompt, 'certificates')
    return jsonify({"response": response_text})

@app.route('/process_description', methods=['POST'])
def process_description():
    data = request.json
    prompt = data.get('description')
    if not prompt:
        return jsonify({"error": "Missing 'description' field"}), 400

    response_text = generate_response(prompt, 'description')
    return jsonify({"response": response_text})


if __name__ == '__main__':
    app.run(debug=True)
