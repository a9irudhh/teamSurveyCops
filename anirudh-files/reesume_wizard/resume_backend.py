import os, json
import markdown2
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
    'overall': "Please read the input carefully and format the following text professionally for a resume. Extract the main contents, keep the formatting simple, and structure the response as a clean JSON object. Ensure that the response does not include 'json' or any additional labels or escape sequences. If you find null objects then dont generate them in the response.",
    
    'name_contact': "Dont add unnecessary details. Please format the following name and contact details professionally for a resume. Structure it clearly as a clean JSON object with the following keys: email, linkedin, name, phone and other cpntact details that you find. Exclude 'json' and any additional labels or escape sequences:",
    
    'schooling_marks': "Dont add unnecessary details. Calculate overall grade .Please organize the following education details level-wise, starting with school and then college. Include CGPAs and percentiles where applicable in new fields, and format them professionally for a resume. Structure the response as a clean JSON object with the following keys: Education. Exclude 'json' and any additional labels or escape sequences:",
    
    'experience': "Dont add unnecessary details. Present the following experience details in a polished and professional manner suitable for a resume. Structure it as a clean JSON object with the following keys: experience. Exclude 'json' and any additional labels or escape sequences:",
    
    'projects': "Dont add unnecessary details. Include techstack that has been used in the projects, if tehy are less in number think and add what are the pre requisites for it also. Please structure the following project details in a professional and easy-to-read format appropriate for a resume. Return the response as a clean JSON object with the following keys: projects. Exclude 'json' and any additional labels or escape sequences:",
    
    'publications': "Dont add unnecessary details. Please organize and format the following publication details in a professional manner suitable for a resume. Structure the response as a clean JSON object with the following keys: publications. Exclude 'json' and any additional labels or escape sequences:",
    
    'certificates': "Dont add unnecessary details. Please structure the following certificate details in a professional and polished format suitable for a resume. Ensure clarity and return the response as a clean JSON object with the following keys: certificates. Exclude 'json' and any additional labels or escape sequences:",
    
    'description': "Dont add unnecessary details. Creatively express the individual's name and summarize their professional persona using the available data. Make it engaging and suitable for a personal description section in a resume. Structure the response as a clean JSON object with the following keys: description. Exclude 'json' and any additional labels or escape sequences:",
    }

    overall_prompt = prompt_engineering.get('overall', '')
    specific_prompt = prompt_engineering.get(prompt_type, '')
    formatted_prompt = overall_prompt + specific_prompt + prompt

    return formatted_prompt

def preprocess(response_text):
    try:
        response_json = json.loads(response_text)
        return response_json
    except json.JSONDecodeError:
        print("Error decoding JSON. The input text might be improperly formatted.")
        return None

def convert_to_markdown(json_data):
    """Convert JSON data into a Markdown formatted string."""
    markdown = ""
    for key, value in json_data.items():
        if isinstance(value, list):
            markdown += f"**{key.capitalize()}**:\n"
            for item in value:
                markdown += f"- {item}\n"
        else:
            markdown += f"**{key.capitalize()}**: {value}\n"
        markdown += "\n"
    return markdown2.markdown(markdown)

def generate_response(prompt, prompt_type):
    """Generate a response from the model with additional formatting instructions."""
    formatted_prompt = format_prompt(prompt, prompt_type)
    response = model.generate_content(formatted_prompt)
    return response.text

@app.route('/process_name_contact', methods=['POST'])
def process_name_contact():
    data = request.json
    prompt = data.get('name_contact')
    if not prompt:
        return jsonify({"error": "Missing 'name_contact' field"}), 400

    response_text = generate_response(prompt, 'name_contact')
    response_json = preprocess(response_text)
    if response_json:
        markdown_response = convert_to_markdown(response_json)
        return jsonify({"response": markdown_response})
    return jsonify({"error": "Failed to process response"}), 500

@app.route('/process_schooling_marks', methods=['POST'])
def process_schooling_marks():
    data = request.json
    prompt = data.get('schooling_marks')
    if not prompt:
        return jsonify({"error": "Missing 'schooling_marks' field"}), 400

    response_text = generate_response(prompt, 'schooling_marks')
    response_json = preprocess(response_text)
    if response_json:
        markdown_response = convert_to_markdown(response_json)
        return jsonify({"response": markdown_response})
    return jsonify({"error": "Failed to process response"}), 500

@app.route('/process_experience', methods=['POST'])
def process_experience():
    data = request.json
    prompt = data.get('experience')
    if not prompt:
        return jsonify({"error": "Missing 'experience' field"}), 400

    response_text = generate_response(prompt, 'experience')
    response_json = preprocess(response_text)
    if response_json:
        markdown_response = convert_to_markdown(response_json)
        return jsonify({"response": markdown_response})
    return jsonify({"error": "Failed to process response"}), 500

@app.route('/process_projects', methods=['POST'])
def process_projects():
    data = request.json
    prompt = data.get('projects')
    if not prompt:
        return jsonify({"error": "Missing 'projects' field"}), 400

    response_text = generate_response(prompt, 'projects')
    response_json = preprocess(response_text)
    if response_json:
        markdown_response = convert_to_markdown(response_json)
        return jsonify({"response": markdown_response})
    return jsonify({"error": "Failed to process response"}), 500

if __name__ == '__main__':
    app.run(debug=True)
